# -------------------------------------------------------------------
# Copyright (C) 2018 Gopalakrishnan
#
# SPDX-License-Identifier: GPL-3.0-or-later
# See GPL-3.0-or-later in the Licenses folder for license information
# -------------------------------------------------------------------

from flask import Flask, g, render_template, request, flash, redirect, url_for, session
from flask_simpleldap import LDAP

# Flask Initialization
app = Flask(__name__)

# Include config from config.py
app.config.from_object('config')
group = app.config['GROUP_NAME']

from models import db
db.init_app(app)

from models import *
from specification import *
from utils import set_boolean_value, make_component_info, _monkey_patch_openldap_string_flask_simpleldap_1_2_0_issue_44, owner_or_group_required

ldap = _monkey_patch_openldap_string_flask_simpleldap_1_2_0_issue_44(LDAP(app))


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = ldap.get_object_details(user=session['user_id'])
        groups = ldap.get_user_groups(user=session['user_id'])
        if groups:
            g.ldap_groups = groups
        else:
            g.ldap_groups = list()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/component/')
def component():
    components = Component.query.all()
    return render_template('component.html', components=components)


@app.route('/license/')
def license():
    licenses = License.query.all()
    return render_template('license.html', licenses=licenses)


@app.route('/product/')
def product():
    products = Product.query.all()
    return render_template('product.html', products=products)


@app.route('/license/<int:id>')
def license_info(id):
    license = License.query.filter_by(id=id).first()
    return render_template('license-info.html', license=license)


@app.route('/component/<int:id>')
def component_info(id):
    component = Component.query.filter_by(id=id).first()
    return render_template('component-info.html', component=component)


@app.route('/product/<int:id>')
def product_info(id):
    product = Product.query.filter_by(id=id).first()
    return render_template('product-info.html', product=product)


@app.route('/component/create/', methods=['GET', 'POST'])
@ldap.group_required(groups=[group])
def create_component():
    if request.method == 'POST':
        name = request.form['name']
        version = request.form['version']
        license_expression = request.form['license_expression']
        created_by = session['user_id']
        origin = request.form['origin']
        source_url = request.form['source_url']
        ext_link = request.form['ext_link']
        components = request.form.getlist('components')
        pub_date = request.form['pub_date']

        # Validation
        is_valid, license_expression, pub_date = is_valid_component_info(
            license_expression, origin, source_url, ext_link, pub_date)

        if(is_valid is True):
            c = Component(name, version, created_by=created_by, pub_date=pub_date, origin=origin,
                          source_url=source_url, license_expression=license_expression, ext_link=ext_link)
            for component_name in components:
                comp = Component.query.filter_by(name=component_name).first()
                if(comp):
                    c.components.append(comp)

            try:
                db.session.add(c)
                db.session.commit()
                flash('Component created successfully', 'success')
            except:
                db.session.rollback()
                flash('Please try again', 'error')

    components = Component.query.all()
    licenses = License.query.all()
    return render_template('create-component.html', components=components, licenses=licenses, username=session['user_id'])


@app.route('/component/update/', methods=['GET', 'POST'])
@ldap.login_required
def update_component():
    if request.method == 'POST':
        component_name = request.form['component']
        component = Component.query.filter_by(name=component_name).first()
        if(component):
            return redirect(url_for('update_component_info', id=component.id))
    components = Component.query.all()
    return render_template('update-component.html', components=components)


@app.route('/component/update/<int:id>', methods=['GET', 'POST'])
@ldap.group_required(groups=[group])
def update_component_info(id):
    if request.method == 'POST':
        name = request.form['name']
        version = request.form['version']
        license_expression = request.form['license_expression']
        origin = request.form['origin']
        source_url = request.form['source_url']
        ext_link = request.form['ext_link']
        components = request.form.getlist('components')
        pub_date = request.form['pub_date']

        # Validation
        is_valid, license_expression, pub_date = is_valid_component_info(
            license_expression, origin, source_url, ext_link, pub_date)

        if(is_valid is True):
            c = Component.query.filter_by(id=id).first()
            if(c):
                c.name = name
                c.version = version
                c.license_expression = license_expression
                c.origin = origin
                c.source_url = source_url
                c.ext_link = ext_link
                c.pub_date = pub_date

                # Remove previously selected components
                for comp in c.components:
                    c.components.remove(comp)

                # Add the newly selected components
                for component_name in components:
                    comp = Component.query.filter_by(
                        name=component_name).first()
                    if(comp):
                        c.components.append(comp)

                try:
                    db.session.commit()
                    flash('Component updated successfully', 'success')
                except:
                    db.session.rollback()
                    flash('Please try again', 'error')

    component = Component.query.filter_by(id=id).first()
    # The permissible set of components should not contain itself
    components = Component.query.filter(Component.id != id).all()
    selected_components = [c.name for c in component.components.all()]
    licenses = License.query.all()
    return render_template('update-component-info.html', component=component, components=components, selected_components=selected_components, licenses=licenses)


@app.route('/license/create/', methods=['GET', 'POST'])
@ldap.group_required(groups=[group])
def create_license():
    if request.method == 'POST':
        full_name = request.form['full_name']
        identifier = request.form['identifier']
        license_category = request.form['license_category']
        fsf_free_libre = request.form.get('fsf_free_libre', None)
        osi_approved = request.form.get('osi_approved', None)
        license_text = request.form['license_text']

        fsf_free_libre = set_boolean_value(fsf_free_libre)
        osi_approved = set_boolean_value(osi_approved)

        l = License(full_name, identifier, fsf_free_libre,
                    osi_approved, license_category, license_text)
        try:
            db.session.add(l)
            db.session.commit()
            flash('License created successfully', 'success')
        except:
            db.session.rollback()
            flash('Please try again', 'error')

    return render_template('create-license.html')


@app.route('/license/update/', methods=['GET', 'POST'])
@ldap.login_required
def update_license():
    if request.method == 'POST':
        license_full_name = request.form['license']
        license = License.query.filter_by(full_name=license_full_name).first()
        if(license):
            return redirect(url_for('update_license_info', id=license.id))
    licenses = License.query.all()
    return render_template('update-license.html', licenses=licenses)


@app.route('/license/update/<int:id>', methods=['GET', 'POST'])
@ldap.group_required(groups=[group])
def update_license_info(id):
    if request.method == 'POST':
        full_name = request.form['full_name']
        identifier = request.form['identifier']
        license_category = request.form['license_category']
        fsf_free_libre = request.form.get('fsf_free_libre', None)
        osi_approved = request.form.get('osi_approved', None)
        license_text = request.form['license_text']

        fsf_free_libre = set_boolean_value(fsf_free_libre)
        osi_approved = set_boolean_value(osi_approved)

        l = License.query.filter_by(id=id).first()
        if(l):
            l.full_name = full_name
            l.identifier = identifier
            l.license_category = license_category
            l.fsf_free_libre = fsf_free_libre
            l.osi_approved = osi_approved
            l.license_text = license_text

            try:
                db.session.commit()
                flash('License updated successfully', 'success')
            except:
                db.session.rollback()
                flash('Please try again', 'error')

    license = License.query.filter_by(id=id).first()
    return render_template('update-license-info.html', license=license)


@app.route('/product/create/', methods=['GET', 'POST'])
@ldap.login_required
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        version = request.form['version']
        owner = session['user_id']
        license = request.form['license']
        approver = request.form['approver']
        approval_date = get_date(request.form['approval_date'])

        l = License.query.filter_by(identifier=license).first()
        p = Product(name, version, owner, approver, approval_date)
        p.license = l
        db.session.add(p)
        component_info = make_component_info(request.form)

        for info in component_info:
            c = Component.query.filter_by(name=info[0]).first()
            if(c):
                modification = set_boolean_value(info[3])
                pc = Product_Component_conn(
                    p, c, info[1], modification, info[2])
                db.session.add(pc)
        try:
            db.session.commit()
            flash('Product created successfully', 'success')
        except:
            db.session.rollback()
            flash('Please try again', 'error')

    components = Component.query.all()
    licenses = License.query.all()
    return render_template('create-product.html', relations=valid_relationship, valid_delivery=valid_delivery, licenses=licenses, components=components, owner=session['user_id'])


@app.route('/product/update/', methods=['GET', 'POST'])
@ldap.login_required
def update_product():
    if request.method == 'POST':
        product_name = request.form['product']
        product = Product.query.filter_by(name=product_name).first()
        if(product):
            return redirect(url_for('update_product_info', id=product.id))
    products = Product.query.all()
    return render_template('update-product.html', products=products)


@app.route('/product/update/<int:id>', methods=['GET', 'POST'])
@owner_or_group_required(groups=[group])
def update_product_info(id):
    if request.method == 'POST':
        name = request.form['name']
        version = request.form['version']
        license = request.form['license']
        approver = request.form['approver']
        approval_date = get_date(request.form['approval_date'])

        l = License.query.filter_by(identifier=license).first()
        p = Product.query.filter_by(id=id).first()
        if(p):
            p.name = name
            p.version = version
            p.approver = approver
            p.approval_date = approval_date
            p.license = l
            db.session.add(p)

            component_info = make_component_info(request.form)

            Product_Component_conn.query.filter_by(product_id=p.id).delete()

            for info in component_info:
                c = Component.query.filter_by(name=info[0]).first()
                if(c):
                    modification = set_boolean_value(info[3])
                    pc = Product_Component_conn(
                        p, c, info[1], modification, info[2])
                    db.session.add(pc)

            try:
                db.session.commit()
                flash('Product updated successfully', 'success')
            except:
                db.session.rollback()
                flash('Please try again', 'error')

    product = Product.query.filter_by(id=id).first()
    components = Component.query.all()
    licenses = License.query.all()
    return render_template('update-product-info.html', product=product, relations=valid_relationship, valid_delivery=valid_delivery, licenses=licenses, components=components)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        test = ldap.bind_user(username, password)
        if test is not None:
            session['user_id'] = request.form['username']
            return redirect(url_for('home'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(401)
def unauthorized_error(error):
    return render_template('401.html'), 401


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0')

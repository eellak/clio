# -------------------------------------------------------------------
# Copyright (C) 2018 Gopalakrishnan
#
# SPDX-License-Identifier: GPL-3.0-or-later
# See GPL-3.0-or-later in the Licenses folder for license information
# -------------------------------------------------------------------

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Flask Initialization
app = Flask(__name__)

# Include config from config.py
app.config.from_object('config')

# Create an instance of SQLAlchemy
db = SQLAlchemy(app)

from models import *
from specification import is_valid_component_info


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


@app.route('/create/component/', methods=['GET', 'POST'])
def create_component():
    if request.method == 'POST':
        name = request.form['name']
        version = request.form['version']
        license_expression = request.form['license_expression']
        created_by = request.form['created_by']
        origin = request.form['origin']
        source_url = request.form['source_url']
        ext_link = request.form['ext_link']
        components = request.form.getlist('components')
        pub_date = request.form['pub_date']

        # Validation
        is_valid, license_expression, pub_date = is_valid_component_info(
            license_expression, origin, source_url, ext_link, pub_date)

        if(is_valid is True):
            c = Component(name, version, pub_date=pub_date, origin=origin,
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
    return render_template('create-component.html', components=components)


@app.route('/update/component/', methods=['GET', 'POST'])
def update_component():
    if request.method == 'POST':
        component_name = request.form['component']
        component = Component.query.filter_by(name=component_name).first()
        if(component):
            return redirect(url_for('update_component_info', id=component.id))
    components = Component.query.all()
    return render_template('update-component.html', components=components)


@app.route('/update/component/<int:id>', methods=['GET', 'POST'])
def update_component_info(id):
    if request.method == 'POST':
        name = request.form['name']
        version = request.form['version']
        license_expression = request.form['license_expression']
        created_by = request.form['created_by']
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
                c.created_by = created_by
                c.origin = origin
                c.source_url = source_url
                c.ext_link = ext_link
                c.pub_date = pub_date

                # Remove previously selected components
                for comp in c.components:
                    c.components.remove(comp)

                # Add the newly selected components
                for component_name in components:
                    comp = Component.query.filter_by(name=component_name).first()
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
    return render_template('update-component-info.html', component=component, components=components, selected_components=selected_components)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0')

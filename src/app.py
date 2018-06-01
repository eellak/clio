# -------------------------------------------------------------------
# SPDX-License-Identifier: GPL-3.0-or-later
# See GPL-3.0-or-later in the Licenses folder for license information
# -------------------------------------------------------------------

from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Flask Initialization
app = Flask(__name__)

# Include config from config.py
app.config.from_object('config')

# Create an instance of SQLAlchemy
db = SQLAlchemy(app)

from models import *
from specification import *


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
        is_valid = True
        exp = is_valid_license_expression(license_expression)
        if(exp is None):
            is_valid = False
            flash('Invalid License Expression', 'error')
        else:
            license_expression = exp
        if(pub_date != ''):
            pub_date = datetime.strptime(pub_date, '%B %d, %Y')
            pub_date = pub_date.strftime('%Y-%m-%d')
        else:
            pub_date = None

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


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0')

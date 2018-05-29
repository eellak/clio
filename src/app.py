# -------------------------------------------------------------------
# SPDX-License-Identifier: GPL-3.0-or-later
# See GPL-3.0-or-later in the Licenses folder for license information
# -------------------------------------------------------------------

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Flask Initialization
app = Flask(__name__)

# Include config from config.py
app.config.from_object('config')

# Create an instance of SQLAlchemy
db = SQLAlchemy(app)

from models import *


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


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0')

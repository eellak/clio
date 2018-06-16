# -------------------------------------------------------------------
# Copyright (C) 2018 Gopalakrishnan
#
# SPDX-License-Identifier: GPL-3.0-or-later
# See GPL-3.0-or-later in the Licenses folder for license information
# -------------------------------------------------------------------

from license_expression import Licensing
import validators
from flask import flash
from datetime import datetime
import csv

valid_relationship = None
with open('valid-relationship.csv') as input_file:
    read_csv = csv.reader(input_file, delimiter=',')
    relations = list()
    for row in read_csv:
        relations.extend(row)
    valid_relationship = tuple(relations)

valid_delivery = None
with open('valid-delivery.csv') as input_file:
    read_csv = csv.reader(input_file, delimiter=',')
    delivery = list()
    for row in read_csv:
        delivery.extend(row)
    valid_delivery = tuple(delivery)


def is_valid_license_expression(expression):
    """Checks if the given string is a valid SPDX License Expression.

    >>> print(is_valid_license_expression('MIT or GPL-2.0'))
    MIT OR GPL-2.0

    :param expression: The expression that needs to be verified.
    :type expression: str
    :returns: str or None

    """
    licensing = Licensing()
    try:
        if(expression == ''):
            return expression
        else:
            parsed = licensing.parse(expression)
            return parsed.render('{symbol.key}')
    except:
        return None


def is_valid_url(url):
    """Checks if the given string is valid URL.

    >>> print(is_valid_url('https://github.com/eellak/clio'))
    True

    :param url: The URL that needs to be verified.
    :type url: str
    :returns: bool

    """
    return (url == '' or validators.url(url))


def is_valid_component_info(license_expression, origin, source_url, ext_link, pub_date):
    """Checks if information provided on components is valid.

    >>> print(is_valid_component_info('License', 'http://www.foo.bar/', 'http://www.foo.bar/download/version.tar.gz', 'https://www.foo.bar/information', 'January 1, 2000'))
    (True, 'License', '2000-01-01')

    :param license_expression: The License Expression that need to be verified.
    :type license_expression: str
    :param origin: The Origin URL that needs to be verified.
    :type origin: str
    :param source_url: The Source URL that needs to be verified.
    :type source_url: str
    :param ext_link: The External Link that needs to be verified.
    :type ext_link: str
    :param pub_date: The Publication Date that needs to be verified.
    :type pub_date: str

    """
    is_valid = True

    exp = is_valid_license_expression(license_expression)
    if(exp is None):
        is_valid = False
        flash('Invalid License Expression', 'error')
    else:
        license_expression = exp

    if(not is_valid_url(origin)):
        is_valid = False
        flash('Invalid Origin URL', 'error')

    if(not is_valid_url(source_url)):
        is_valid = False
        flash('Invalid Source URL', 'error')

    if(not is_valid_url(ext_link)):
        is_valid = False
        flash('Invalid External Link', 'error')

    if(pub_date != ''):
        pub_date = datetime.strptime(pub_date, '%B %d, %Y')
        pub_date = pub_date.strftime('%Y-%m-%d')
    else:
        pub_date = None

    return is_valid, license_expression, pub_date

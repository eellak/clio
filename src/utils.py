# -------------------------------------------------------------------
# Copyright (C) 2018 Gopalakrishnan
#
# SPDX-License-Identifier: GPL-3.0-or-later
# See GPL-3.0-or-later in the Licenses folder for license information
# -------------------------------------------------------------------

from functools import wraps
from flask import g, session, abort, redirect, url_for, current_app, request
from models import *


def set_boolean_value(status):
    """Sets boolean value based on the given string.

    >>> set_boolean_value('true')
    True

    :param status: Status string based on which the value has to be set.
    :type status: str
    :returns: bool

    """
    val = None
    if status == 'true':
        val = True
    elif status == 'false':
        val = False
    return val


def get_number_of_entries(data):
    """Evaluates the number of entries in the create/update Product form. The number of entries is evaluated based on the number of component fields.

    :param data: Form data based on which the number of entries is evaluated.
    :type data: werkzeug.datastructures.ImmutableMultiDict
    :returns: int

    """
    max_num = 0
    for key in data:
        if(key.startswith('component')):
            num = int(key.split('-')[1])
            if(num > max_num):
                max_num = num
    return max_num + 1


def make_component_info(data):
    """Format the given data to store in the database.

    :param data: Form data based on which the number of entries is evaluated.
    :type data: werkzeug.datastructures.ImmutableMultiDict
    :returns: tuple

    """
    index = 0
    component_info = list()
    max_entries = get_number_of_entries(data)
    while(index < max_entries):
        comp = list()
        comp.append(data['component-' + str(index)])
        comp.append(data['relation-' + str(index)])
        comp.append(data['delivery-' + str(index)])
        try:
            comp.append(data['modification-' + str(index)])
        except:
            comp.append('')
        component_info.append(tuple(comp))
        index += 1
    return tuple(component_info)


# This patch is borrowed from https://github.com/admiralobvious/flask-simpleldap/issues/44
def _monkey_patch_openldap_string_flask_simpleldap_1_2_0_issue_44(ldap_instance):
    import ldap

    def bind_user(self, username, password):
        user_dn = self.get_object_details(user=username, dn_only=True)

        if user_dn is None:
            return
        try:
            if type(user_dn) == bytes:
                user_dn = user_dn.decode('utf-8')

            conn = self.initialize
            conn.simple_bind_s(user_dn, password)
            return True
        except ldap.LDAPError:
            return

    import types
    ldap_instance.bind_user = types.MethodType(bind_user, ldap_instance)

    return ldap_instance


def owner_or_group_required(groups=None):
    """When applied to a view function, any unauthenticated requests will be redirected to the login view. Authenticated requests are only permitted if they either belong to one of the listed groups or if the user is the owner.

    :param groups: List of groups that should be able to access the view function.
    :type groups: list
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if g.user is None:
                return redirect(url_for(current_app.config['LDAP_LOGIN_VIEW'], next=request.path))
            match = [group for group in groups if group in g.ldap_groups]
            product_id = kwargs['id']
            product = Product.query.filter_by(id=product_id).first()
            owner = product.owner
            if not match and session['user_id'] != owner:
                abort(401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

# -------------------------------------------------------------------
# Copyright (C) 2018 Gopalakrishnan
#
# SPDX-License-Identifier: GPL-3.0-or-later
# See GPL-3.0-or-later in the Licenses folder for license information
# -------------------------------------------------------------------

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/clio'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application threads
# A common general assumption is using 2 per available cores
# to handle incoming requests using one
# perform backgorund operations using the other
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure and unique secret key for signing the data
CSRF_SESSION_KEY = 'secret'

# Secret key for signing cookies
SECRET_KEY = 'secret'

# LDAP Configuration
LDAP_OPENLDAP = True
LDAP_HOST = 'localhost'
LDAP_BASE_DN = 'dc=example,dc=com'
LDAP_USERNAME = 'cn=admin,dc=example,dc=com'
LDAP_PASSWORD = 'root'
LDAP_USER_OBJECT_FILTER = '(&(objectclass=inetOrgPerson)(uid=%s))'

LDAP_GROUP_MEMBERS_FIELD = 'member'
LDAP_GROUP_OBJECT_FILTER = '(&(objectclass=groupOfNames)(member=%s))'
LDAP_GROUP_MEMBER_FILTER = '(&(cn=*)(objectclass=groupOfNames)(member=%s))'
LDAP_GROUP_MEMBER_FILTER_FIELD = 'cn'

GROUP_NAME = 'ldapgroup'

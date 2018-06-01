# -------------------------------------------------------------------
# SPDX-License-Identifier: GPL-3.0-or-later
# See GPL-3.0-or-later in the Licenses folder for license information
# -------------------------------------------------------------------

from license_expression import Licensing
import validators

valid_relationship = ('DESCRIBES', 'DESCRIBED_BY', 'CONTAINS', 'CONTAINED_BY', 'GENERATES', 'GENERATED_FROM', 'ANCESTOR_OF', 'DESCENDANT_OF', 'VARIANT_OF', 'DISTRIBUTION_ARTIFACT', 'PATCH_FOR', 'PATCH_APPLIED', 'COPY_OF', 'FILE_ADDED', 'FILE_DELETED',
                      'FILE_MODIFIED', 'EXPANDED_FROM_ARCHIVE', 'DYNAMIC_LINK', 'STATIC_LINK', 'DATA_FILE_OF', 'TEST_CASE_OF', 'BUILD_TOOL_OF', 'DOCUMENTATION_OF', 'OPTIONAL_COMPONENT_OF', 'METAFILE_OF', 'PACKAGE_OF', 'AMENDS', 'PREREQUISITE_FOR', 'HAS_PREREQUISITE', 'OTHER')

valid_delivery = ('SOURCE', 'BINARY', 'ARCHIVE', 'APPLICATION',
                  'AUDIO', 'IMAGE', 'TEXT', 'VIDEO', 'DOCUMENTATION', 'SPDX', 'OTHER', 'NOT-DELIVERED')

def is_valid_license_expression(expression):
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
    return (url == '' or validators.url(url))

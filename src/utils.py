# -------------------------------------------------------------------
# Copyright (C) 2018 Gopalakrishnan
#
# SPDX-License-Identifier: GPL-3.0-or-later
# See GPL-3.0-or-later in the Licenses folder for license information
# -------------------------------------------------------------------

def set_boolean_value(status):
    val = None
    if status == 'true':
        val = True
    elif status == 'false':
        val = False
    return val

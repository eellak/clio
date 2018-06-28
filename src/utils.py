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


def get_number_of_entries(data):
    max_num = 0
    for key in data:
        if(key.startswith('component')):
            num = int(key.split('-')[1])
            if(num > max_num):
                max_num = num
    return max_num + 1


def make_component_info(data):
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

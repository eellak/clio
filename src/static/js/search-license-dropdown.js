/*
    Copyright (C) 2018 Gopalakrishnan

    SPDX-License-Identifier: GPL-3.0-or-later
    See GPL-3.0-or-later in the Licenses folder for license information
*/

window.onload = function () {
    var select_license = document.getElementById('select-license');
    select_license.onchange = function () {
	var id = select_license.options[select_license.selectedIndex].value;
	window.location.href = '/license/' + id;
    }
}

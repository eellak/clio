/*
    Copyright (C) 2018 Gopalakrishnan

    SPDX-License-Identifier: GPL-3.0-or-later
    See GPL-3.0-or-later in the Licenses folder for license information
*/

$(document).ready(function() {
    $('.ui.radio.checkbox').checkbox();
    $('.ui.form')
	.form({
	    fields: {
		full_name  : 'empty',
		identifier : 'empty',
	    }
	})
    ;
});

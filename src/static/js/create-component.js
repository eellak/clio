/*
    Copyright (C) 2018 Gopalakrishnan

    SPDX-License-Identifier: GPL-3.0-or-later
    See GPL-3.0-or-later in the Licenses folder for license information
*/

$(document).ready(function() {
    $('#pub_date').calendar({
	type: 'date', 
	maxDate: new Date()
    });
    $('.ui.dropdown').dropdown({
	forceSelection: false, 
	selectOnKeydown: false, 
	showOnFocus: false,
	on: "hover" 
    });
    $('.ui.form')
	.form({
	    fields: {
		name     : 'empty',
		version  : 'empty',
	    }
	})
    ;
});

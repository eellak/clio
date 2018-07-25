/*
    Copyright (C) 2018 Gopalakrishnan

    SPDX-License-Identifier: GPL-3.0-or-later
    See GPL-3.0-or-later in the Licenses folder for license information
*/

$(document).ready(function() {
    $('#approval_date').calendar({
	type: 'date', 
	maxDate: new Date()
    });
    $('.ui.dropdown').dropdown();
    $('.ui.form')
	.form({
	    fields: {
		name     : 'empty',
		version  : 'empty',
	    }
	})
    ;
    $(function() {
	$("body").on("click", ".ui.icon.button", function() {
	    var length = $(".input-group").length;
	    var clone = $("#selection").clone();
	    clone.find("select#component").attr("name", "component-"+length);
	    clone.find("select#relation").attr("name", "relation-"+length);
	    clone.find("select#delivery").attr("name", "delivery-"+length);
	    clone.find("input#modification").attr("name", "modification-"+length);
	    clone.find(".ui.dropdown").dropdown('clear');
	    clone.find(".ui.checkbox").checkbox('uncheck');
	    $("#selections").append(clone);
	});
    });
});

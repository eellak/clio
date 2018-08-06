/*
    Copyright (C) 2018 Gopalakrishnan

    SPDX-License-Identifier: GPL-3.0-or-later
    See GPL-3.0-or-later in the Licenses folder for license information
*/

$(document).ready(function() {
    $("#a-product").addClass("active")
    var table = $("#product").DataTable( {
	"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]], 
	buttons: ['copy', 'excel', 'pdf', 'print'],
    } );
    table.buttons().container()
	.appendTo( $('div.eight.column:eq(0)', table.table().container()) );
} );

/*
    Copyright (C) 2018 Gopalakrishnan

    SPDX-License-Identifier: GPL-3.0-or-later
    See GPL-3.0-or-later in the Licenses folder for license information
*/

$(document).ready(function() {
    $("#a-product").addClass("active")
    var table = $("#product").DataTable( {
	lengthChange: false,
	buttons: ['copy', 'excel', 'pdf', 'print'],
    } );
    table.buttons().container()
	.appendTo( $('div.eight.column:eq(0)', table.table().container()) );
} );

// Customization for tablesorter (jquery.tablsorter.min.js)
$.tablesorter.addParser({
    // set a unique id
    id: 'titles',
    is: function(s) {
        // return false so this parser is not auto detected
        return false;
    },
    format: function(s) {
        // Format your data for normalization
        s = $.trim(s)  // Make sure there are no leading spaces
        s = s.toLowerCase();
        s = s.replace(/^the /, '');
        s = s.replace(/^an? /, '');
        return s;
    },
    type: 'text'
});

$(document).ready(function() {
    // Apply tablesorter to #newspapers table
    $("#newspapers").tablesorter({
        headers: {
            // When sorting by titles, use the title formatter
            // so we skip "the", "a", and "an"
            '.sort-titles': { sorter: 'titles' },

            // Disable sorting, e.g. on the "browse issues" link
            '.sort-off': { sorter: false },
        },
        widgets: ['zebra'],

        // Default to sorting by first column
        sortList: [[0,0]]
    });

    // Filter text of each row in #newspapers table
    $("#filterTitles").keyup(function() {
        var searchText = $(this).val().toLowerCase();
        $.each($("#newspapers tbody tr"), function() {
            if($(this).text().toLowerCase().indexOf(searchText) === -1)
                $(this).hide();
            else
               $(this).show();
        });
    });
    $("#resetTitles").click(function() {
        $("#filterTitles").val("");
        $.each($("#newspapers tbody tr"), function() {
            $(this).show();
        });
    });
});

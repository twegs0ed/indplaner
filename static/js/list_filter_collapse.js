jQuery(document).ready(function($){
    $('<div id="show-filters" style="float: right; background-color:#79aec8; line-height: 18px;"><a href="#" style="color:#ffffff;">&larr;Show Filters</a></p>').prependTo('div.actions');
    $('#show-filters').hide();
    $('#changelist-filter h2').html('<a style="color: white;" id="hide-filters" href="#">Filter &rarr;</a>');

    $('#show-filters').click(function() {
        $('#changelist-filter').show('fast');
        $('#changelist').addClass('filtered');
        $('#show-filters').hide();
    });

    $('#hide-filters').click( function() {
        $('#changelist-filter').hide('fast');
        $('#show-filters').show();
        $('#changelist').removeClass('filtered');
    });
});



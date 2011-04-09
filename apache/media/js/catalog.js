$(function() {
    // Generate the custom slider if exists
    if ($('.custom_range_select').length > 0) {
        $('.custom_range_select').selectToUISlider({
            labelSrc: 'text',
            tooltipSrc: 'text',
            labels: 2,
        }).hide();
    }

    // Generate the price slider
    $('.price_range_select').selectToUISlider({
        labelSrc: 'text',
        tooltipSrc: 'text',
        labels: 2,
    }).hide();
    
    /* Each time the user changes the ordering criteria in the combobox, reload 
    the page to update the results */
	$('#ordering_options').change(function() {
	    /* current_url is a hidden field set by the server with all the search
	    parameters used for the query that yielded the current results. */
	    var url = $('#current_url').val() + $('#ordering_options').val()
	    window.location.replace(url)
	})
	
	// We check whether the advanced controls should be displayed or not
    
    /* id_advanced_controls is a hidden field set by the server that contains a
    1 if the user used advanced controls in the previous query and 0 if not.
    Also, the value for the field must be updated when the user expands or 
    collapses the advanced options for the server to be aware of the state when
    the form is submitted*/
    var advFieldVal = $('#id_advanced_controls').val()
    var visibleHiddenFields
    
    /* If the advanced controls were used in the previous query, keep them 
    visible.  Either way, set the text of the JS link accordingly, if we're 
    showing advanced controls, the link should say "Busqueda basica") */
    if (advFieldVal == "1") {
        $('#toggle_hidden_link').html("Búsqueda básica");
        visibleHiddenFields = true;
    } else {
        $('.hidden_filter_item').hide();
        visibleHiddenFields = false;
    }
    
    /* Handle the click of the JS link in a similar fashion */
    $('#toggle_hidden_link').click(function(event) {
        /* This prevents the screen from going to the top of the page when the
        link is clicked */
        event.preventDefault();
        
        // Update everything as predicted
        $('.hidden_filter_item').toggle();
        visibleHiddenFields = !visibleHiddenFields;
        if (visibleHiddenFields) {
            $('#toggle_hidden_link').html("Búsqueda básica");
            $('#id_advanced_controls').val(1);
        } else {
            $('#toggle_hidden_link').html("Búsqueda avanzada");
            $('#id_advanced_controls').val(0);
        }
    });
    
    $('#tiers-select').change(update_tier_selection)
    $('#tiers-select').keypress(update_tier_selection)
    if ($('#tiers-select').length > 0) {
        update_tier_selection()
    }
})

function update_tier_selection() {
    var tier = tiers[$('#tiers-select').val()]
    $('span#cellphone_price_span').html(format_currency(tier['cellphone_price']))
    $('span#plan_price_span').html(format_currency(tier['plan_price']))
    $('span#plan_data_span').html(tier['plan_data'])
    $('span#three_month_price_span').html(format_currency(tier['three_month_pricing']))
    $('span#six_month_price_span').html(format_currency(tier['six_month_pricing']))
    $('span#twelve_month_price_span').html(format_currency(tier['twelve_month_pricing']))
    $('a#cell_external_link').attr('href', '/store_product/' + tier['shpe_id'])
    $('a#cell_plan_link').attr('href', '/cellphones/plans/' + tier['plan_id'])
    
}

function format_currency(amount)
{
    return addCommas(amount.toString())
}

function addCommas( strValue ) {
    var objRegExp = new RegExp('(-?[0-9]+)([0-9]{3})');

    //check for match to search criteria
    while(objRegExp.test(strValue)) {
    //replace original string with first group match,
    //a comma, then second group match
    strValue = strValue.replace(objRegExp, '$1.$2');
    }
    return strValue;
}

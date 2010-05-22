/* Functions used in all the pages, most of them realted to the search panel
to the right */

$(function() {
    // First, we check whether the advanced controls should be displayed or not
    
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
    
    /* abs_min_price and abs_max_price are hidden fields set by the server and
    contain the lowest and highest notebook price in the database, we use those
    as limits for the slider */
    var abs_min_price = parseInt($('#abs_min_price').val())
    var abs_max_price = parseInt($('#abs_max_price').val())
    
    /* id_min_price and id_max_price are fields that contain the lower and upper
    bound for the price search system in the query that generated this page, 
    they are formatted as money, so we need to take away the thousands 
    separators. They may not be set if the previous query did not set up these 
    boundaries, in those cases we manually set them to lie in the boundaries */
    var min_price
    if ($('#id_min_price').val()) {
        min_price = parseInt($('#id_min_price').val().replace(/\./g, ''))
    } else {
        min_price = abs_min_price
        $('#id_min_price').val(min_price)
    }
        
    var max_price
    if ($('#id_max_price').val()) {
        max_price = parseInt($('#id_max_price').val().replace(/\./g, ''))
    } else {
        max_price = abs_max_price
        $('#id_max_price').val(max_price)
    } 
        
    /* We set up the price slider with sensible values */
    $('#price_slider').slider({
		range: true,
		min: abs_min_price,
		max: abs_max_price,
		values: [min_price, max_price],
		step: 10000,
		slide: handleSliderValueChange,
		stop: handleSliderValueChange,
		change: handleSliderValueChange
	});
	
	/* When we submit the search form, the displays for the price range are
	disabled inputs (as we don't the users to manually set them, but to use the 
	slider), which are not submitted by default (according to W3C
	standards), so we activate them just before submitting them so the server
	can receive them. Also, they are still formatted at this point, so we take
	away the thousands separator to avoid ugly GET variables getting sent */
	$('#search_form').submit(function() {
	    $('.price_range_input').removeAttr('disabled');
	    $('#id_min_price').val($('#id_min_price').val().replace(/\./g, ''))
	    $('#id_max_price').val($('#id_max_price').val().replace(/\./g, ''))
	    return true;
	});
	
	/* Initially the id_min_price and id_max_price contain raw numbers, so
	we just format them adding thousands separators to each */
	$('#id_min_price').val(addThousandsSeparators($('#id_min_price').val()))
	$('#id_max_price').val(addThousandsSeparators($('#id_max_price').val()))
	
    /* When the reset button is pressed, set all the search parameters to their
    default value */
    $('#reset_button').click(function() {
        $('.hidden_filter_item select').val('');
        $('.filter_item select').val('');        
        $('#price_slider').slider('values', [abs_min_price, abs_max_price])
    });
})

/* Function that takes care of keeping everything up to date when the slider
moves, in this case that means updating the input fields for the price range
to reflect the new values. */
function handleSliderValueChange(event, ui) {
    var values = $('#price_slider').slider('option', 'values');
    $('#id_min_price').val(addThousandsSeparators(values[0]));
    $('#id_max_price').val(addThousandsSeparators(values[1]));
}

/* Utility function that takes an integer value and returns a string 
corresponding to its display as money (i.e.: with thousands separators )*/
function addThousandsSeparators(value) {
    value = value + ''
    var sRegExp = new RegExp('([0-9]+)([0-9]{3})');

    while(sRegExp.test(value)) {
        value = value.replace(sRegExp, '$1.$2');
    }
    return value;
} 

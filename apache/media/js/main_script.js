$(function() {
    var advFieldVal = $('#id_advanced_controls').val()
    var visibleHiddenFields    
    if (advFieldVal == "1") {
        $('#toggle_hidden_link').html("Búsqueda básica");
        visibleHiddenFields = true;
    } else {
        $('.hidden_filter_item').hide();
        visibleHiddenFields = false;
    }
    
    $('#toggle_hidden_link').click(function(event) {
        event.preventDefault();
        
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
    
    $('#reset_button').click(function() {
        $('.hidden_filter_item select').val('');
        $('.filter_item select').val('');        
    });
    
    var abs_min_price = parseInt($('#abs_min_price').val())
    var abs_max_price = parseInt($('#abs_max_price').val())
    
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
        
    $('#price_slider').slider({
		range: true,
		min: abs_min_price,
		max: abs_max_price,
		values: [min_price, max_price],
		step: 10000,
		slide: handleSliderValueChange,
		stop: handleSliderValueChange
	});
	
	$('#search_form').submit(function() {
	    $('.price_range_input').removeAttr('disabled');
	    $('#id_min_price').val($('#id_min_price').val().replace(/\./g, ''))
	    $('#id_max_price').val($('#id_max_price').val().replace(/\./g, ''))
	    return true;
	});
	
	$('#id_min_price').val(addThousandsSeparators($('#id_min_price').val()))
	$('#id_max_price').val(addThousandsSeparators($('#id_max_price').val()))
})

function handleSliderValueChange(event, ui) {
    var values = $('#price_slider').slider('option', 'values');
    $('#id_min_price').val(addThousandsSeparators(values[0]));
    $('#id_max_price').val(addThousandsSeparators(values[1]));
}

function addThousandsSeparators(value) {
    value = value + ''
    var sRegExp = new RegExp('([0-9]+)([0-9]{3})');

    while(sRegExp.test(value)) {
        value = value.replace(sRegExp, '$1.$2');
    }
    return value;
} 

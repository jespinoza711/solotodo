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
    
    $(".processor_table tr:nth-child(odd)").addClass("odd-row");
})

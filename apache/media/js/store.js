$(function() {
    $('#reserve_button').click(function() {
        $('#reserve_products_form').submit()
    })
    
    $('#free_button').click(function() {
        $('#free_products_form').submit()
    })
    
    $('#advertisement_slot_form input:text').datepicker({ dateFormat: 'yy-mm-dd' });
    
    $('#advertisement_tabs').tabs();
    $('#sub_advertisement_tabs').tabs();
    
    $('#registry_tabs').tabs();
})

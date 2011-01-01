$(function() {
    $('.add_to_comparison_list_link').click(function(event) {
        event.preventDefault()
        var ntbk_id = $(this).attr('ntbk_id')
        var container = $(this).parent()
        $.post('/comparison/additem/', {
            ntbk_id: ntbk_id
        }, function(data) {
            result = $.parseJSON(data)
            if (result.code == 'OK') {
                container.slideUp(function() {
                    $(this).html('Notebook agregado <a href="/comparison/">Ver lista</a>').slideDown()
                })
            }
        })
    })
    
    $('.remove_from_comparison_list_link').click(function(event) {
        event.preventDefault()
        var ntbk_id = $(this).attr('ntbk_id')
        var container = $(this).parent()
        $.post('/comparison/removeitem/', {
            ntbk_id: ntbk_id
        }, function(data) {
            result = $.parseJSON(data)
            if (result.code == 'OK') {
                container.slideUp(function() {
                    $(this).html('Notebook eliminado <a href="/comparison/">Ver lista</a>').slideDown()
                })
            }
        })
    })
})

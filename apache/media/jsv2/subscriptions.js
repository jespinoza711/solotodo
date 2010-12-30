$(function() {
    $('.subscription_link').click(function(event) {
        event.preventDefault()
        $(this).parent().submit()
    })
})

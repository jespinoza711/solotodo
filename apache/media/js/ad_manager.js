$(function() {
    var container = $('#topmost_ad_container');

    if (container.length == 1) {
        var ad_id = container.attr('ad_id');

        $.post('/ad_impressed/', {
            ad_id: ad_id
        })
    }
});
$(function() {
    $('#id_notebook_type').selectmenu({
        menuWidth: 400,
        width: 173,
        format: notebook_type_formatting
    });

    var initial_price = parseInt($('#id_max_price').val());

    $("#slider-range-min").slider({
        range: "min",
        value: initial_price,
        min: 100000,
        max: 1000000,
        step: 50000,
        slide: function(event, ui) {
            $('#maximum_price').html('$' + add_thousands_separators(ui.value));
            $('#id_max_price').val(ui.value);
        }
    });

    $('#maximum_price').html('$' + add_thousands_separators(initial_price));
});

function notebook_type_formatting(text){
    var newText = text;
    //array of find replaces
    var findreps = [
        {find:/^([^\-]+) \- /g, rep: '<span class="ui-selectmenu-item-header">$1</span>'},
        {find:/([^\|><]+) \| /g, rep: '<span class="ui-selectmenu-item-content">$1</span>'},
        {find:/([^\|><\(\)]+) (\()/g, rep: '<span class="ui-selectmenu-item-content">$1</span>$2'},
        {find:/([^\|><\(\)]+)$/g, rep: '<span class="ui-selectmenu-item-content">$1</span>'},
        {find:/(\([^\|><]+\))$/g, rep: '<span class="ui-selectmenu-item-footer">$1</span>'}
    ];

    for(var i in findreps){
        newText = newText.replace(findreps[i].find, findreps[i].rep);
    }
    return newText;
}

function add_thousands_separators(nStr) {
    nStr += '';
    var x = nStr.split('.');
    var x1 = x[0];
    var x2 = x.length > 1 ? '.' + x[1] : '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
        x1 = x1.replace(rgx, '$1' + '.' + '$2');
    }
    return x1 + x2;
}

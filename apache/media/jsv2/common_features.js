function add_thousands_separators(nStr)
{
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

var addressFormatting = function(text){
    var newText = text;
    //array of find replaces
    var findreps = [
        {find:/^([^\-]+) \- /g, rep: '<span class="ui-selectmenu-item-header">$1</span>'},
        {find:/([^\|><]+) \| /g, rep: '<span class="ui-selectmenu-item-content">$1</span>'},
        {find:/([^\|><\(\)]+) (\()/g, rep: '<span class="ui-selectmenu-item-content">$1</span>$2'},
        {find:/([^\|><\(\)]+)$/g, rep: '<span class="ui-selectmenu-item-content">$1</span>'},
        {find:/(\([^\|><]+\))$/g, rep: '<span class="ui-selectmenu-item-footer">$1</span>'}
    ];

    var i;
    for(i in findreps){
        newText = newText.replace(findreps[i].find, findreps[i].rep);
    }
    return newText;
}


$(function() {
    /* Price slider */
    $( "#slider-range-min" ).slider({
        range: "min",
        value: 400000,
        min: 100000,
        max: 800000,
        step: 10000,
        slide: function( event, ui ) {
            $("#amount").html("$" + add_thousands_separators(ui.value));
            $("#id_max_price").val(ui.value);
        }
    });

    $('#usage select').selectmenu(
        {
            width: 250,
            style: 'dropdown',
            format: addressFormatting
        }
    );

    $("#amount").html("$" + add_thousands_separators($("#slider-range-min").slider("value")));
    $("#id_max_price").val($("#slider-range-min").slider("value"));

    $.each($('.errorlist'), function(index, value) {
        var field_container = $(value).next();
        field_container.addClass('control-group');
        field_container.addClass('error');
    });

    /* When the user hovers the mouse over the PC Parts
     * show submenu, and only hide it when the user scrolls
     * over another category (like notebooks) */
    $('#navigator li').hover(
        function() {
            $('#navigator li').removeClass('menu-item-hover');
            $(this).addClass('menu-item-hover');
            var link_tag = $(this).children('a');
            /* If the link is actually a menu */
            if (link_tag.attr('href') == '#') {
                $('#submenu').show();
            } else {
                $('#submenu').hide();
            }
        },
        function() {
            var link_tag = $(this).children('a');
            if ( link_tag.attr('href') != '#')
            $(this).removeClass('menu-item-hover');
        }
    );

    /* Modal window for login*/
    $('#login-link').click(function() {
       $('#login-modal').modal();
    });

    $('#login-modal .cancel').click(function() {
        $('#login-modal').modal('hide');
    });

    /* Login submit logic */
    $('#login-modal form').submit(function() {
        var field_ids = ['#id_username', '#id_password'];
        var values = ['', ''];
        var ticker = $('#login-modal .ticker');

        $.each(field_ids, function(index, value) {
            var field_element = $(value);
            var field_container =  field_element.parents('p').first();
            if (field_element.val() == '') {
                field_container.addClass('control-group');
                field_container.addClass('error');
            } else {
                field_container.removeClass('control-group');
                field_container.removeClass('error');
                values[index] = field_element.val()
            }
        });

        if (values[0] != '' && values[1] != '') {
            show_ticker_message(
                ticker,
                'Ingresando',
                function() {
                    $.post('/accounts/login/', {
                        username: values[0],
                        password: values[1]
                    }, function(data) {
                        console.log(data);
                        if (data.code == 'OK') {
                            window.location = ''
                        } else {
                            show_ticker_message(
                                ticker,
                                'Nombre de usuario y contraseña no coinciden',
                                function() {
                                    // Do nothing
                                }
                            );
                        }
                    }, 'json');
                }
            );
        } else {
            show_ticker_message(
                ticker,
                'Por favor ingresa tu nombre de usuario / contraseña',
                function() {
                    // Do nothing
                }
            );
        }

        return false;
    });
});

function show_ticker_message(ticker, message, callback) {
    var old_message = ticker.html();
    if (old_message != message) {
        ticker.slideUp(function() {
            ticker.html(message);
            ticker.slideDown(function() {
                callback();
            });
        });
    } else {
        callback();
    }
}

function handle_facebook_login(response) {
    var data = response.authResponse;
    $.post(
        '/accounts/facebook_login/',
        {
            access_token: data.accessToken,
            user_id: data.userID
        },
        function(data) {
            console.log(data);
            if (data.code == 'OK') {
                window.location = ''
            }
        },
        'json'
    );
}
$(function() {
    /* When the user hovers the mouse over the PC Parts
     * show submenu, and only hide it when the user scrolls
     * over another category (like notebooks) */
    $('#navigator li').hover(
        function() {
            var link_tag = $(this).children('a');
            /* If the link is actually a menu */
            if (link_tag.attr('href') == '#') {
                $('#submenu').show();
            } else {
                $('#submenu').hide();
            }
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
                    $.post('http://localhost:8000/account/login/', {
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
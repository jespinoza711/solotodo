var clear_search_field = true
var options = new Array();

$(function() {
    // Show error and info messages
    $('#error_message').slideDown().delay(3000).slideUp()
    $('#info_message').slideDown().delay(3000).slideUp()

    // If the user clicks for the first time the search bar, empty its contents
    $('.input-search').click(function() {
        if (clear_search_field) {
            $('.input-search').val('')
            clear_search_field = false
        }
    });

    $('.regenerate_link').click(function(event) {
        event.preventDefault()
    
        $("#dialog_regenerate").dialog({
	        resizable: false,
	        height: 260,
	        width: 450,
	        modal: true,
	        buttons: [
                {
                    text: "Confirmar",
                    click: function() { validate_regenerate_form() },
                    'class': 'ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only dialog_button', 
                },
                {
                    text: "Cancelar",
                    click: function() { $(this).dialog("close"); },
                    'class': 'ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only dialog_button', 
                }
            ]
        });
    });    
    
    $('.subscribe_link').click(function(event) {
        event.preventDefault()
        subscribe(authenticated_user, false, 1)
    })
    
    $('.favorite_link').click(function(event) {
        event.preventDefault()
        subscribe(authenticated_user, false, 0)
    })
    
    $('#id_product').change(function(event) {
        event.preventDefault()
        refresh_product_link()
    })
    
    refresh_product_link()


    $.each($('#id_product option'), function(idx, value) {
        if (idx == 0) {
            return true
        }
        options.push($(value))
    });

    $('#filtrar_form').submit(function(event) {
        var text = $('#staff_filtrar').val().toLowerCase()
        if (text.length == 0) {
            return false
        }

        $('#id_product').empty()
        var re = new RegExp(text, "i");

        $.each(options, function(idx, option) {
            var option_text = option.text();

            if (option_text.search(re) >= 0) {
                $('#id_product').append(option);
            }
        });

        refresh_product_link()

        return false
    });

})

function refresh_product_link() {
    var ids = $('#id_product').val()
    if (ids) {
        url = '/products/' + ids
        clone_url = '/staff/' + staff_id + '/clone_product/' + ids
    } else {
        url = '/all_products'
        clone_url = '#'
    }
        
    $('#product_link').attr('href', url)
    $('#clone_link').attr('href', clone_url)
}

function show_js_error(text) {
    $('#js_error_message').html(text).slideDown().delay(3000).slideUp()
}

function show_js_message(text) {
    $('#js_info_message').html(text).slideDown().delay(3000).slideUp()
}

function display_regenerate_error(message) {
    $('#regenerate_ajax_loader').slideUp(function() {
        $('#regenerate_error').slideUp(function() {
            $('#regenerate_error').html(message).slideDown()
        })
    })
}

function validate_regenerate_form() {
    username = $.trim($('#regenerate_username').val())
    
    if (username == '') {
        display_regenerate_error('Por favor ingrese un nombre de usuario')
        return
    }
    
    $('#regenerate_error').slideUp(function() {
        $('#regenerate_ajax_loader').slideDown()
        
        $.ajax({
            type: 'POST',
            data: ({ username: username }),
            url: '/account/request_password_regeneration/',
            dataType: 'json',
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function(data) {
                response = data
                if (response.code == 'OK') {
                    $('#regenerate_ajax_loader').slideUp()        
                    $("#dialog_regenerate").dialog('close')
                    show_js_message('Correo de regeneración de contraseña enviado')
                } else {
                    display_regenerate_error(response.message)
                }
            }
        });
    });
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function subscribe(registered, reload_on_finish, include_email) {
    if (!registered) {
        FB.login(function(response) {
          if (response.authResponse) {
            $.ajax({
                type: 'POST',
                url: '/account/facebook_ajax_login/',
                dataType: 'json',
                data: {
                    user_id: response.authResponse.userID,
                    access_token: response.authResponse.accessToken
                },
                beforeSend: function(xhr) {
                    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                },
                success: function(data) {
                    if (data.code == 'OK') {
                        subscribe(true, true, include_email);
                    }
                }
            });
          } else {
            // user cancelled login
          }
        }, { scope: 'email' });
    } else {
        url = '/account/add_subscription?product=' + product_id + '&email_notifications=' + include_email
        window.location = url
    }
}

function handle_facebook_login(authResponse) {
    myauthResponse = authResponse

    $.post(
        '/account/facebook_login/',
        {
            access_token: authResponse.authResponse.accessToken,
            user_id: authResponse.authResponse.userID
        },
        function(data) {
            if (data.code == 'OK') {
                window.location = ''
            }
        },
        'json'
    );
}

function handle_facebook_fusion() {
    window.location = '/account/facebook_fusion';
}

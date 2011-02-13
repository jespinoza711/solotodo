var clear_search_field = true

$(function() {
    $('.register_link').click(function(event) {
        event.preventDefault()
        show_signup_dialog('', 320, false, function() { 
            location.reload(true) 
        })
    });
    
    
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
	        height: 270,
	        width: 400,
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
    
    $('#error_message').slideDown().delay(3000).slideUp()
    $('#info_message').slideDown().delay(3000).slideUp()    
    
    $('.subscribe_link').click(function(event) {
        event.preventDefault()
        
        subscribe(authenticated_user, false, 1)
    })
    
    $('.favorite_link').click(function(event) {
        event.preventDefault()
        
        subscribe(authenticated_user, false, 0)
    })
    
    
})

function show_login_dialog(callback) {
    $('#login_error').hide()
    $('#dialog_login').dialog({
        resizable: false,
        height: 200,
        width: 400,
        modal: true,
        buttons: [
            {
                text: "Confirmar",
                click: function() { validate_login_form(callback) },
                'class': 'ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only dialog_button', 
            },
            {
                text: "Cancelar",
                click: function() { $(this).dialog('close'); },
                'class': 'ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only dialog_button', 
            }
        ]
    });    
}

function validate_login_form(callback) {
    username = $.trim($('#login_username').val())
    password = $('#login_password').val()
    
    if (username == '') {
        display_login_error('Por favor ingrese su nombre de usuario')
        return
    }
    
    if (password == '') {
        display_login_error('Por favor ingrese su contraseña')
        return
    }    
    
    $('#login_error').slideUp(function() {
        $('#login_ajax_loader').slideDown(function() {
            $.post('/account/ajax_login/', {
                username: username,
                password: password
            },
            function(data) {
                response = $.parseJSON(data)
                if (response.code == 'OK') {
                    callback()
                } else {
                    display_login_error(response.message)
                }
            })
        })
    })
}

function show_signup_dialog(text, height, show_login_link, callback) {
    $('#signup_text').html(text)
    $('#signup_error').hide()
    if (show_login_link) {
        $('#already_registered_link').show().unbind('click').click(function(event) {
            event.preventDefault()
            $("#dialog-confirm").dialog('close')
            show_login_dialog(callback)
        })
    } else {
        $('#already_registered_link').hide()
    }
    $("#dialog-confirm").dialog({
        resizable: false,
        height: height,
        width: 400,
        modal: true,
        buttons: [
            {
                text: "Confirmar",
                click: function() { validate_signup_form(callback) },
                'class': 'ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only dialog_button', 
            },
            {
                text: "Cancelar",
                click: function() { $(this).dialog("close"); },
                'class': 'ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only dialog_button', 
            }
        ]
    });
}

function validate_regenerate_form() {
    username = $.trim($('#regenerate_username').val())
    
    if (username == '') {
        display_regenerate_error('Por favor ingrese un nombre de usuario')
        return
    }
    
    $('#regenerate_error').slideUp(function() {
        $('#regenerate_ajax_loader').slideDown()
        
        $.post('/account/request_password_regeneration/', {
        username: username,
        },
        function(data) {
            response = $.parseJSON(data)
            if (response.code == 'OK') {
                $('#regenerate_ajax_loader').slideUp()        
                $("#dialog_regenerate").dialog('close')
                show_js_message('Correo de regeneración de contraseña enviado')
            } else {
                display_regenerate_error(response.message)
            }
        })
    })
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

function display_login_error(message) {
    $('#login_ajax_loader').slideUp(function() {
        $('#login_error').slideUp(function() {
            $('#login_error').html(message).slideDown()
        })
    })
}

function subscribe(registered, reload_on_finish, include_email) {
    if (!registered) {
        show_signup_dialog(
            'Para suscribirte a un notebook primero tienes que registrarte, no te preocupes, sólo tomará un segundo', 
            380, 
            true,
            function() { 
                subscribe(true, true, include_email) 
            })
    } else {
        url = '/account/add_subscription?product=' + product_id + '&email_notifications=' + include_email
        window.location = url
    }
}

function validate_signup_form(callback) {
    username = $.trim($('#signup_username').val())
    
    if (username == '') {
        display_signup_error('Por favor ingrese un nombre de usuario')
        return
    }
    
    if (username.length > 30) {
        display_signup_error('El nombre de usuario no puede tener mas de 30 caracteres')
        return
    }
    
    email = $.trim($('#signup_email').val())
    if (!validate_email(email)) {
        display_signup_error('Por favor ingrese un correo electrónico válido')
        return
    }
    
    password = $.trim($('#signup_password').val())
    if (password == '') {
        display_signup_error('Por favor ingrese una contraseña')
        return
    }
    
    repeat_password = $.trim($('#signup_repeat_password').val())
    if (password != repeat_password) {
        display_signup_error('Las contraseñas no concuerdan')
        return
    }    
    
    signup_key = $('#signup_key').val()
    
    $('#signup_error').slideUp(function() {
        $('#signup_ajax_loader').slideDown(function() {
            $.post('/account/signup/', {
                username: username,
                email: email,
                password: password,
                repeat_password: repeat_password,
                signup_key: signup_key,
            },
            function(data) {
                response = $.parseJSON(data)
                if (response.code == 'OK') {
                    callback()
                } else {
                    display_signup_error(response.message)
                }
            })  
        })
    })
}

function validate_email(email) {
   var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
   return reg.test(email)
}

function display_signup_error(message) {
    $('#signup_ajax_loader').slideUp(function() {
        $('#signup_error').html(message).slideDown()
    })
}

/* Function that takes care of keeping everything up to date when the slider
moves, in this case that means updating the input fields for the price range
to reflect the new values. */
function handleSliderValueChange(event, ui) {
    var values = $('#price_slider').slider('option', 'values');
    $('#id_min_price').val(addThousandsSeparators(values[0]));
    $('#id_max_price').val(addThousandsSeparators(values[1]));
}

/* Utility function that takes an integer value and returns a string 
corresponding to its display as money (i.e.: with thousands separators )*/
function addThousandsSeparators(value) {
    value = value + ''
    var sRegExp = new RegExp('([0-9]+)([0-9]{3})');

    while(sRegExp.test(value)) {
        value = value.replace(sRegExp, '$1.$2');
    }
    return value;
} 

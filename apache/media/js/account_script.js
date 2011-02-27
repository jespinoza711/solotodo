$(function() {
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
})

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
          if (response.session && response.perms) {
            $.ajax({
                type: 'POST',
                url: '/account/facebook_ajax_login/',
                dataType: 'json',
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
        }, { perms: 'email' });
    } else {
        url = '/account/add_subscription?product=' + product_id + '&email_notifications=' + include_email
        window.location = url
    }
}

function handle_facebook_login() {
    window.location = '/account/facebook_login?next=' + location.pathname;
}

function handle_facebook_fusion() {
    window.location = '/account/facebook_fusion';
}

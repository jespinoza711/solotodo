/* Functions used in all the pages, most of them realted to the search panel
to the right */

$(function() {
    // First, we check whether the advanced controls should be displayed or not
    
    /* id_advanced_controls is a hidden field set by the server that contains a
    1 if the user used advanced controls in the previous query and 0 if not.
    Also, the value for the field must be updated when the user expands or 
    collapses the advanced options for the server to be aware of the state when
    the form is submitted*/
    var advFieldVal = $('#id_advanced_controls').val()
    var visibleHiddenFields
    
    /* If the advanced controls were used in the previous query, keep them 
    visible.  Either way, set the text of the JS link accordingly, if we're 
    showing advanced controls, the link should say "Busqueda basica") */
    if (advFieldVal == "1") {
        $('#toggle_hidden_link').html("Búsqueda básica");
        visibleHiddenFields = true;
    } else {
        $('.hidden_filter_item').hide();
        visibleHiddenFields = false;
    }
    
    /* Handle the click of the JS link in a similar fashion */
    $('#toggle_hidden_link').click(function(event) {
        /* This prevents the screen from going to the top of the page when the
        link is clicked */
        event.preventDefault();
        
        // Update everything as predicted
        $('.hidden_filter_item').toggle();
        visibleHiddenFields = !visibleHiddenFields;
        if (visibleHiddenFields) {
            $('#toggle_hidden_link').html("Búsqueda básica");
            $('#id_advanced_controls').val(1);
        } else {
            $('#toggle_hidden_link').html("Búsqueda avanzada");
            $('#id_advanced_controls').val(0);
        }
    });
    
    /* abs_min_price and abs_max_price are hidden fields set by the server and
    contain the lowest and highest notebook price in the database, we use those
    as limits for the slider */
    var abs_min_price = parseInt($('#abs_min_price').val())
    var abs_max_price = parseInt($('#abs_max_price').val())
    
    /* id_min_price and id_max_price are fields that contain the lower and upper
    bound for the price search system in the query that generated this page, 
    they are formatted as money, so we need to take away the thousands 
    separators. They may not be set if the previous query did not set up these 
    boundaries, in those cases we manually set them to lie in the boundaries */
    var min_price
    if ($('#id_min_price').val()) {
        min_price = parseInt($('#id_min_price').val().replace(/\./g, ''))
    } else {
        min_price = abs_min_price
        $('#id_min_price').val(min_price)
    }
        
    var max_price
    if ($('#id_max_price').val()) {
        max_price = parseInt($('#id_max_price').val().replace(/\./g, ''))
    } else {
        max_price = abs_max_price
        $('#id_max_price').val(max_price)
    } 
        
    /* We set up the price slider with sensible values */
    $('#price_slider').slider({
		range: true,
		min: abs_min_price,
		max: abs_max_price,
		values: [min_price, max_price],
		step: 10000,
		slide: handleSliderValueChange,
		stop: handleSliderValueChange,
		change: handleSliderValueChange
	});
	
	/* When we submit the search form, the displays for the price range are
	disabled inputs (as we don't the users to manually set them, but to use the 
	slider), which are not submitted by default (according to W3C
	standards), so we activate them just before submitting them so the server
	can receive them. Also, they are still formatted at this point, so we take
	away the thousands separator to avoid ugly GET variables getting sent */
	$('#search_form').submit(function() {
	    $('.price_range_input').removeAttr('disabled');
	    $('#id_min_price').val($('#id_min_price').val().replace(/\./g, ''))
	    $('#id_max_price').val($('#id_max_price').val().replace(/\./g, ''))
	    return true;
	});
	
	/* Initially the id_min_price and id_max_price contain raw numbers, so
	we just format them adding thousands separators to each */
	$('#id_min_price').val(addThousandsSeparators($('#id_min_price').val()))
	$('#id_max_price').val(addThousandsSeparators($('#id_max_price').val()))
	
    /* When the reset button is pressed, set all the search parameters to their
    default value */
    $('#reset_button').click(function() {
        $('.hidden_filter_item select').val('');
        $('.filter_item select').val('');        
        $('#price_slider').slider('values', [abs_min_price, abs_max_price])
    });
    
    $('.LS').hover(
    function() {
        $(this).addClass('header_hover');
    }, function() {
        $(this).removeClass('header_hover');
    });
    
    $('.LS').click(function() {
        window.location.replace('/')
    });
    
    $('#error_message').slideDown().delay(3000).slideUp()
    $('#info_message').slideDown().delay(3000).slideUp()    
    
    $('#register_link').click(function(event) {
        event.preventDefault()
        show_signup_dialog('', 270, false, function() { 
            location.reload(true) 
        })
    });
    
    $('.regenerate_link').click(function(event) {
        event.preventDefault()
    
        $("#dialog_regenerate").dialog({
	        resizable: false,
	        height: 230,
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
    })
    
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
            310, 
            true,
            function() { 
                subscribe(true, true, include_email) 
            })
    } else {
        url = '/account/add_subscription?notebook=' + notebook_id + '&email_notifications=' + include_email
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

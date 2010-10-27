var available_ntbks = new Array()
var publicized_ntbks = new Array()
var unavailable_ntbks = new Array()

function NotebooksModel(container, callback) {
    this.list = new Array()   
    this.container = container
    
    if (callback == undefined)
        this.callback = function() {}
    else
        this.callback = callback
}
        
NotebooksModel.prototype.set_ntbk_list = function(new_list) {
    this.list = new_list
    this.update_model_view()
}

NotebooksModel.prototype.update_model_view = function() {
    this.container.empty()
    for (var i = 0; i < this.list.length; i++) {
        var li_html = '<li id="' + this.list[i].id + '">' + this.list[i].name + '</li>'
        this.container.append(li_html)
    }
    this.callback()
}

NotebooksModel.prototype.remove = function(id) {
    elem = extract(this.list, id)
    this.update_model_view()
    return elem
}

NotebooksModel.prototype.add = function(element) {
    this.list.push(element)
    this.update_model_view()
}


NotebooksModel.prototype.length = function() {
    return this.list.length
}

function extract(list, id) {
    for (var i = 0; i < list.length; i++) {
        if (list[i].id == id) {
            elem = list.splice(i, 1)
            return elem[0]
        }
    }
    
    return null
}

$(function() {
    available_ntbks = new NotebooksModel($('#available_ntbks'))
    
    publicized_ntbks = new NotebooksModel($('#publicized_ntbks'), function() {
        $('#publicized_ntbks_counter').html(this.length())
    })    
    
    unavailable_ntbks = new NotebooksModel($('#unavailable_ntbks'))
    
    
    $.getJSON('/advertisement/get_advertisement_options/', 
    {},
    function(data) {
        available_ntbks.set_ntbk_list(data[0])
        publicized_ntbks.set_ntbk_list(data[1])
        unavailable_ntbks.set_ntbk_list(data[2])
    })
    
    $('#available_ntbks li').live('click', function() {
        id = this.id
        $.post('/advertisement/submit/', { 
                'id': id
            },
            function(data){
                if (data.code == 'OK') {
                    offer = available_ntbks.remove(id)
                    publicized_ntbks.add(offer)
                }
                
            }, 
            'json');
    })
    
    $('#publicized_ntbks li').live('click', function() {
        id = this.id
        $.post('/advertisement/remove/', { 
                'id': id
            },
            function(data){
                if (data.code == 'OK') {
                    offer = publicized_ntbks.remove(id)
                    available_ntbks.add(offer)
                }
                
            }, 
            'json');
    })
})

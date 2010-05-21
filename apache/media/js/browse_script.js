$(function() {
	$('#id_ordering').change(function() {
	    var url = $('#current_url').val() + 'ordering=' + $('#id_ordering').val()
	    window.location.replace(url)
	})
});

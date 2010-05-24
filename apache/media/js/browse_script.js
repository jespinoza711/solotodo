/* Functions for the search/browse page */


$(function() {
    /* Each time the user changes the ordering criteria in the combobox, reload 
    the page to update the results */
	$('#ordering_options').change(function() {
	    /* current_url is a hidden field set by the server with all the search
	    parameters used for the query that yielded the current results. */
	    var url = $('#current_url').val() + $('#ordering_options').val()
	    window.location.replace(url)
	})
});

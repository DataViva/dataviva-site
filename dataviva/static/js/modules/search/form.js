var select = $("<select></select>").attr("id", 'search-selector').addClass("search-selector form-control");

	$.ajax({
            method: "POST",
            url: "/search/selector/all",
            success: function (search) {
            	search.selectors.forEach(function(entry) {
					select.append($('<option value="'+entry[0]+'">'+entry[0]+'</option>'));
				});
            }
        });
	
	$('#search-form').append(select);
    //onChange
    $('#search-selector option').val()



$(document).ready(function(){

});

var select = $("<select></select>").attr("id", 'search-selector').addClass("search-selector form-control");

	var search = 'teste';
	select.append($('<option value="">'+search+'</option>'));
	$('#search-form').append(select);

$(document).ready(function(){

});

var Metadata = (function(){
	var get = function(key){
	    return new Promise(function(resolve, reject) {
	        if (localStorage.getItem(key)) {
	            resolve(JSON.parse(localStorage.getItem(key)));
	        }
	        else {
	            $.ajax({
					url: dataviva.api_url + "/metadata/" + key,
	                success: function (data) {
	                    localStorage.setItem(key, JSON.stringify(data));
	                    resolve(JSON.parse(localStorage.getItem(key)));
	                }
	            });
	        }
	    });
	}

	return {
		get: get
	};

})();
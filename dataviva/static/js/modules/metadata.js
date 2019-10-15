var Metadata = (function(){
	var get = function(key){
	    return new Promise(function(resolve, reject) {
	        if (sessionStorage.getItem(key)) {
	            resolve(JSON.parse(sessionStorage.getItem(key)));
	        }
	        else {
	            $.ajax({
					url: dataviva.api_url + "metadata/" + key,
	                success: function (data) {
	                    sessionStorage.setItem(key, JSON.stringify(data));
	                    resolve(JSON.parse(sessionStorage.getItem(key)));
	                }
	            });
	        }
	    });
	}

	return {
		get: get
	};

})();
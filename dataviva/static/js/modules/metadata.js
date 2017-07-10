var Metadata = (function(){
	var get = function(key){
	    return new Promise(function(resolve, reject) {
	        if (localStorage.getItem(key)) {
	            resolve(JSON.parse(localStorage.getItem(key)));
	        }
	        else {
	            $.ajax({
	                url: "http://api.staging.dataviva.info/metadata/" + key,
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
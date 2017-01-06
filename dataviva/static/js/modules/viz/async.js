var ajaxQueue = function(urls, callback, ajax) {
    var results = [],
        queue = urls,
        config = ajax || {};

    var ready = function(result, url) {
        queue.splice(queue.indexOf(url), 1);
        if (result) results.push(result);
        if (queue.length === 0 ) {
            callback(results);
        }
    }

    queue.forEach(function(url) {
        $.ajax({
            dataType: config['dataType'] || 'json',
            method: config['method'] || 'GET',
            url: url,
            success: function(result) { ready(result, url); },
            error: function(result) { ready(null, url); },
        });
    });
}
var toolsBuilder = function(viz, data, title, ui) {
    d3.selectAll(".alt_tooltip")
        .on(d3plus.client.pointer.over, function() {
            dataviva.ui.tooltip("alt_tooltip", this)
    })
        .on(d3plus.client.pointer.out, function() {
            dataviva.ui.tooltip("alt_tooltip", false)
    });

    d3.selectAll('.close-popover-btn').on('click', function() {
        dataviva.popover.hide();
    });

    d3.select('#refresh-btn').on('click', function() {
        loadViz(data);
    });

    d3.select('#share-btn').on('click', function() {
        dataviva.popover.show('#share-popover');
    });

    d3.select('#share-popover').selectAll('input').on('click', function() {
        this.focus();
        this.select();
    });
   
    d3.xhr('/' + lang + '/embed/shorten/') 
        .header('Content-type','application/json')
        .post(JSON.stringify({'url': window.location.href}), function(error, data) {
            var shortUrl = window.location.origin + '/' + lang + '/' + JSON.parse(data.response).slug;

            d3.select('#shortened-url').attr('value', shortUrl);
            d3.select('#embed-url').attr('value', '<iframe width="560" height="315" src=' + shortUrl + ' frameborder="0"></iframe>');
            d3.select('#twitter-btn').attr('href', 'https://twitter.com/share?url='+ shortUrl +'&text='+ title +'&hashtags=dataviva');
            d3.select('#google-btn').attr('href', 'https://plus.google.com/share?url=' + shortUrl + '&hl=' + (lang == 'en' ? 'en-US' : 'pt-BR'));

            d3.select('#twitter-btn').on('click', function() {
                return !window.open(this.href, 'Twitter', 'width=640,height=300');
            });

            d3.select('#google-btn').on('click', function() {
                return !window.open(this.href, 'Google', 'width=640,height=300');
            });
        });

    d3.select('#download-btn').on('click', function() {
        dataviva.popover.show('#download-popover');
    });

    d3.select('#download-popover').select('.close-popover-btn').on('click', function() {
        dataviva.popover.hide();
    });

    d3.select('#download-csv').on('click', function() {
        viz.csv(true);
        dataviva.popover.hide();
    });

    d3.select('#download-svg').on('click', function() {
        dataviva.popover.hide();
    });

    d3.select('#controls-toggle-btn').on('click', function() {
        controls = !controls;
        viz.ui(controls ? ui : []);
        viz.draw();
    });
};

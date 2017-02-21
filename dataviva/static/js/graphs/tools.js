var toolsBuilder = function(viz, data, title, ui) {

    function expireCookie( cName ) {
        document.cookie =
        encodeURIComponent( cName ) +
        "=deleted; expires=" +
        new Date( 0 ).toUTCString();
      }

    var initializeDownload = function(){
        var svg = d3.select("#tree_map > svg")
        // Add necessary name space junk and get raw node

        svg.attr("version", 1.1)
            .attr("xmlns", "http://www.w3.org/2000/svg")
            .node()
        svg.insert('defs',":first-child")
        var svg_xml = (new XMLSerializer).serializeToString(svg.node());            
        var style = "\n";
        var requiredSheets = ['phylogram_d3.css', 'open_sans.css'];

        for (var i=0; i<document.styleSheets.length; i++) {
            var sheet = document.styleSheets[i];
            if (sheet.href) {
                var sheetName = sheet.href.split('/').pop();
                if (requiredSheets.indexOf(sheetName) != -1) {
                    var rules = sheet.rules;
                    if (rules) {
                        for (var j=0; j<rules.length; j++) {
                            style += (rules[j].cssText + '\n');
                        }
                    }
                }
            } 
        }

        img = new Image();

        d3.select("svg defs")
            .append('style')
            .attr('type','text/css')
            .html(style);

        img.src = 'data:image/svg+xml;base64,'+window.btoa(unescape(encodeURIComponent(svg_xml)));

        var canvas = document.createElement("canvas");

        var w = svg.node().getBBox().width,
            h = svg.node().getBBox().height;

        canvas.width = w;
        canvas.height = h;
        var context = canvas.getContext("2d")
        context.fillStyle = "white";
        context.fillRect(0,0,w,h);
        context.drawImage(img,0,0,w,h);

        title = title.removeAccents().split(" ").join("_");

        return [canvas, w, h, title, svg_xml];
    }

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

        var loadingPopover = dataviva.ui.loading('#share-popover'),
            url = window.location.href;

        if (!yearRange[0] && yearRange[1]) {
            if (url.match(/year=[0-9]{4}/))
                url = url.replace(/year=[0-9]{4}/, 'year=' + yearRange[1]);
            else if (url.match(/\?/))
                url += '&year=' + yearRange[1];
            else
                url += '?year=' + yearRange[1];
        } else {
            url = url.replace(/&year=[0-9]{4}/, '').replace(/\?year=[0-9]{4}&?/, '?');
        }
        console.log(url);

        d3.xhr('/' + lang + '/embed/shorten/')
        .header('Content-type','application/json')
        .post(JSON.stringify({'url': url}), function(error, data) {
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

            loadingPopover.hide();
        });
    });

    d3.select('#share-popover').selectAll('input').on('click', function() {
        this.focus();
        this.select();
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
        expireCookie("downloadToken");
    });

    d3.select('#download-pdf').on('click', function() {

        var initialize = initializeDownload();
        canvas = initialize[0];
        w = initialize[1]*0.264583333;
        h = initialize[2]*0.264583333;
        title = initialize[3];

        pdf = new jsPDF('l', 'mm', [w, h]);
        pdf.addImage(canvas, 'JPEG', 0,0,w,h);
        pdf.save(title);
        
        dataviva.popover.hide();
        expireCookie("downloadToken");
    });

    d3.select('#download-png').on('click', function() {
        var initialize = initializeDownload();
        canvas = initialize[0];
        title = initialize[3];
        
        img_download = canvas.toDataURL("image/png");
        var download = document.createElement('a');
        download.href = img_download;
        download.download = title + ".png";
        download.click();

        dataviva.popover.hide();
        expireCookie("downloadToken");
    });

    d3.select('#download-svg').on('click', function() {
        var initialize = initializeDownload();
        title = initialize[3];
        svg = initialize[4];
        
        var svgBlob = new Blob([svg], {type:"image/svg+xml;charset=utf-8"});
        saveAs(svgBlob, title + ".svg");

        dataviva.popover.hide();
        expireCookie("downloadToken");
    });

    var controls = true;
    d3.select('#controls-toggle-btn').on('click', function() {
        controls = !controls;
        viz.ui(controls ? ui : []);
        viz.draw();
    });
};

jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "num-dataviva-pre": function ( a ) {
        var x = String(a).replace( /<[\s\S]*?>|USD\s|R\$\s|\skg/g, "" );
        var multiplier = 1;


        if (dataviva.language = 'pt'){
            x = x.replace( /,/, "." );
            if (x.match(/Trilh\u00e3o|Trilh\u00f5es/g) != null) {
                multiplier = multiplier * 1000000000000
            } else if (x.match(/Bilh\u00e3o|Bilh\u00f5es/g) != null) {
                multiplier = multiplier * 1000000000
            } else if (x.match(/Milh\u00e3o|Milh\u00f5es/g) != null) {
                multiplier = multiplier * 1000000
            } else if (x.match(/Mil/g) != null) {
                multiplier = multiplier * 1000
            }
        } else if (dataviva.language = 'en'){
            if (x.match(/T/g) != null) {
                multiplier = multiplier * 1000000000000
            } else if (x.match(/B/g) != null) {
                multiplier = multiplier * 1000000000
            } else if (x.match(/M/g) != null) {
                multiplier = multiplier * 1000000
            } else if (x.match(/k/g) != null) {
                multiplier = multiplier * 1000
            }
        }

        var number = parseFloat( x );
        return number * multiplier;
    },

    "num-dataviva-asc": function ( a, b ) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "num-dataviva-desc": function ( a, b ) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
});

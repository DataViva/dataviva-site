window.showGraph = function(major, tab) {
    if ($('#graphs #graphs-' + tab).length === 0) {
        $.ajax({
            method: "POST",
            url: major+"/graphs/"+tab,
            success: function (graphs) {
                $('#graphs').append(graphs);
            }
        });
    }
    $("#graphs").children().hide();
    $('#graphs #graphs-' + tab).show();
}

$(document).ready(function () {
    $(function() {
        var jcarousel = $('.jcarousel');

        jcarousel
            .on('jcarousel:reload jcarousel:create', function () {
                var carousel = $(this),
                    width = carousel.innerWidth();

                if (width >= 600) {
                    width = 200;
                } else if (width >= 350) {
                    width = 170;
                }

                carousel.jcarousel('items').css('width',width);
            })
            .jcarousel({
                wrap: 'circular'
            });

        $('.jcarousel-control-prev').jcarouselControl({
            target: '-=1'
        });

        $('.jcarousel-control-next').jcarouselControl({
            target: '+=1'
        });
    });

    if(document.location.hash) {
        var tab = document.location.hash.substring(1),
            major = document.location.pathname.split('/')[3]

        $('[href=#' + tab + ']').tab('show');

        showGraph(major, tab);
    }

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        if ($(this).attr('graph') != null) {
            var major = this.dataset.major,
                tab = $(this).attr('aria-controls');

            showGraph(major, tab);
        }
    });
});
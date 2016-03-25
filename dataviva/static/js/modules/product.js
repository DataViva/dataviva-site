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
        alert('#' + document.location.hash.substring(1));
    }

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        var product = this.dataset.product,
            location = this.dataset.location,
            graph = $(this).attr('aria-controls');

        $.ajax({
            method: "POST",
            url: product+"/graphs/"+graph+"?bra_id="+location,
            success: function (msg) {

            }
        })

    });
});

window.showGraph = function(category, tab, location) {
    if ($('#graphs #graphs-' + tab).length === 0) {
        $.ajax({
            method: "POST",
            url: category+"/graphs/"+tab+(location !== null ? "?bra_id="+location : ""),
            success: function (graphs) {
                $('#graphs').append(graphs);
                $(graphs).find('a').click(function() {
                    //window.history.pushState("", "", window.location+$(graphs).find('a')[0].href.split('/'+lang)[1]);
                })
            }
        });
    }
    $('#graphs').show();
    $("#graphs").children().hide();
    $('#graphs #graphs-' + tab).show();
}

$('a[class="pull-right btn btn-primary btn-xs m-r-lg"]').click(function() {
    var link = $(this).attr('href');
    $('li[role="presentation"] a[href="'+link+'"]').closest('li').addClass('active').siblings().removeClass('active');
});

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

        if ($('.jcarousel-wrapper .jcarousel ul li').length <= 4) {
            $('.jcarousel-control-prev').addClass("hidden-lg")
            $('.jcarousel-control-next').addClass("hidden-lg")
        }

        if ($('.jcarousel-wrapper .jcarousel ul li').length <= 3) {
            $('.jcarousel-control-prev').addClass("hidden-md")
            $('.jcarousel-control-next').addClass("hidden-md")
        }

        if ($('.jcarousel-wrapper .jcarousel ul li').length <= 2) {
            $('.jcarousel-control-prev').addClass("hidden-sm")
            $('.jcarousel-control-next').addClass("hidden-sm")
        }
    });

    if($('#graphs .list-group.panel .selected').parent().hasClass('collapse')){
        $('#graphs .list-group.panel .selected').parent().attr('class', 'collapse in');
    }

    $('a[data-toggle="tab"]').on('shown.bs.tab', Category.changeTab);
});


$('.category .nav-graph .list-group-item').click(function() {
    $(this).addClass('selected').siblings().removeClass('selected');
    $(this).children().removeClass('selected');
    $(this).siblings().children().removeClass('selected');
});

var Category = (function() {

    function changeTab(e) {
        if ($(this).attr('graph') != null) {
            var category = this.dataset.id,
                location = this.dataset.location,
                tab = $(this).attr('aria-controls');

            var url = window.location.href.split('?')[0];

            if(url.split('/').length == 5)
                window.history.pushState("", tab, window.location.href + '/' +tab);
            else
                window.history.pushState("", tab, window.location.href + '/' +tab);

            showGraph(category, tab, location);
        } else {
            $('#graphs').hide();
        } 
    }

    return {
        changeTab : changeTab
    }

})();
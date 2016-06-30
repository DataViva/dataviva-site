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
    if($('#graphs .list-group.panel .active').parent().hasClass('collapse')){
        $('#graphs .list-group.panel .active').parent().attr('class', 'collapse in');
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

            if(url.split('/').length == 6)
                window.history.pushState('', '', url + '/' + tab);
            else{
                var url = window.location.href.split('?')[0];
                url = url.split('/');
                url.pop();
                url = url.concat(tab);
                url = url.join('/');
                window.history.pushState('', '', url);
            }

            showGraph(category, tab, location);
        } else {
            $('#graphs').hide();
        } 
    }

    return {
        changeTab : changeTab
    }

})();

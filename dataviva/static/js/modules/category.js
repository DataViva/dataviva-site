window.showGraph = function(url, tab, location) {
    if ($('#graphs #graphs-' + tab).length === 0) {
        $.ajax({
            method: "POST",
            url: url + "/graphs/" + tab + (location !== null ? "?bra_id=" + location : ""),

            success: function (graphs) {
                $('#graphs').append(graphs);
                $('.list-group.panel a[target]').on('click', Category.updateGraphUrl);
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
    $('li[role="presentation"] a[href="'+link+'"]').closest('li').addClass('selected').siblings().removeClass('selected');
});

$(document).ready(function () {
    if($('#graphs .list-group.panel .selected').parent().hasClass('collapse')){
        $('#graphs .list-group.panel .selected').parent().attr('class', 'collapse in');
    }

    $('a[data-toggle="tab"]').on('shown.bs.tab', Category.changeTab);

    $('.list-group.panel a[target]').on('click', Category.updateGraphUrl);

});

$('.category .nav-graph .list-group-item').click(function() {
    $(this).addClass('selected').siblings().removeClass('selected');
    $(this).children().removeClass('selected');
    $(this).siblings().children().removeClass('selected');
});

var Category = (function() {

    function getUrlBeforePageTab(){
        var url = window.location.href.split('?')[0];

        if(url.split('/').length == 6)
            return url;
        else{
            url = url.split('/');
            url.pop();
            url = url.join('/');
            return url;
        }
    }

    function updateUrl(tab){
        var url = getUrlBeforePageTab();

        if(tab != 'general')
            window.history.pushState('', '', url + '/' + tab);
        else
            window.history.pushState('', '', url);
    }

    function changeTab(e) {
        var location = this.dataset.location,
            tab = $(this).attr('aria-controls');

        updateUrl(tab);

        if ($(this).attr('graph') != null)
            showGraph(getUrlBeforePageTab(), tab, location);
        else
            $('#graphs').hide();
    }

    function updateGraphUrl(){
        var parent = $(this).data('parent').slice(1);
        var graphType = $(this).attr('href').split('/')[3];
        var menu = parent + '-' + graphType;

        var graphUrl = $(this).attr('href').split('/').slice(3).join('/');

        var url = window.location.href.split('?')[0] + '?menu=' + menu + '&url=' + encodeURIComponent(graphUrl);
        window.history.pushState('', '', url);
    }

    return {
        changeTab : changeTab,
        updateGraphUrl : updateGraphUrl,
    }

})();



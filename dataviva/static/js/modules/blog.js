var BlogTable = function () {
    this.tableId = '#blog-table';

    this.table = $(this.tableId).DataTable({
        "sAjaxSource": "/blog/post/all",
        "sAjaxDataProp": "posts",
        "order": [],
        "aoColumnsDefs": [
            { "data": "postselector" },
            { "data": "title" },
            { "data": "authors" },
            { "data": "publicationDate" },
            { "data": "active" },
        ],
        "columnDefs": [
            {
                "targets": 0,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, post, meta){

                    var checkbox = '<div class="checkbox checkbox-success">' +
                                   '    <input name="selected-item" id="item'+post[0]+'" value="'+post[0]+'" type="checkbox">' +
                                   '    <label for="'+post[0]+'"></label>'
                                   '</div>';

                    return checkbox;
                }
            },
            {
                "targets": 1,
                "className": "column-title",
                "render": function (data, type, post, meta){
                    return '<a href="/blog/post/'+post[0]+'">'+post[1]+'</a>';
                }
            },
            {
                "targets": 4,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, post, meta){
                    if (data){
                       return '<input type="checkbox" class="js-switch" name="checkboxApproval" value="'+post[0]+'" checked>';
                    }
                    else {
                       return '<input type="checkbox" class="js-switch" name="checkboxApproval" value="'+post[0]+'">';
                    }
                }
              }],
        "columns": [
                { "width": "8%" },
                null,
                null,
                { "width": "20%" },
                { "width": "12%" }
        ],
        "paging": false,
        "bFilter": false,
        "info": false,
        "initComplete": function(settings, json) {
            $( ".js-switch" ).each(function() {
                var switchery = new Switchery(this, {
                    size: 'small',
                    color: '#5A9DC4'
                });
            });
        }
    });

    $('#blog-table thead tr th').first().addClass('check-all')

    $('#blog-table .check-all').click(function() {
        var checked = $('#blog-table .check-all input:checkbox').get(0).checked;
        $('input[name="selected-item"]').each(function() {
            $(this).prop('checked', checked);
        });
    })

};

BlogTable.prototype.getCheckedIds = function(first_argument) {
    var checkedIds = [];
    $('#blog-table input[name="selected-item"]').each(function() {
        if (this.checked) {
            checkedIds.push(this.value);
        }
    });
    return checkedIds;
};

var blogTable = new BlogTable();

var activate = function(ids){
    $.ajax({
      method: "POST",
      url: "/"+lang+"/blog/admin/activate",
      data: {ids:ids},
      success: function (msg) {
      }
    });
}

var deactivate = function(ids){
    $.ajax({
      method: "POST",
      url: "/"+lang+"/blog/admin/deactivate",
      data: {ids:ids},
      success: function (msg) {
      }
    });
}

var destroy = function(ids){
    $.ajax({
      method: "POST",
      url: "/"+lang+"/blog/admin/delete",
      data: {ids:ids},
      success: function (msg) {
      }
    });
}

var edit = function(ids){
    window.location = '/'+lang+'/blog/admin/post/'+ids[0]+'/edit';
}

var inputThumbCallback = function() {
    $($('#thumb-crop')).cropper({
        aspectRatio: 350/227,
        preview: '#thumb-preview',
        viewMode: 3
    });

    $('#thumb-img').hide();
    $('#thumb-crop').show();
    $('.thumb .crop-controls').show();
    $('.thumb label').hide();
}

$(document).ready(function(){

    $('#text-content-editor').append($('#text_content').val())
    $('#text-content-editor').summernote(summernoteConfig);

    $('#blog-edit').click(function() {
        summernoteConfig['focus'] = true;
        $('#text-content-editor').summernote(summernoteConfig);
    });

    $('#blog-preview').click(function() {
        var aHTML = $('#text-content-editor').summernote('code');
        $('#text_content').val(aHTML);
        $('#text-content-editor').summernote('destroy');
    });

    cropInput($('#thumb-crop'), $('#thumb-input'), inputThumbCallback)

    $('#thumb-zoomIn').click(function() {
        $('#thumb-crop').cropper('zoom', 0.1);
    });
    $('#thumb-zoomOut').click(function() {
        $('#thumb-crop').cropper('zoom', -0.1);
    });
    $('#thumb-rotateLeft').click(function() {
        $('#thumb-crop').cropper('rotate', 45);
    });
    $('#thumb-rotateRight').click(function() {
        $('#thumb-crop').cropper('rotate', -45);
    });
    $('#thumb-save').click(function() {
        var thumbDataURL = $('#thumb-crop').cropper('getDataURL');
        $('#thumb').val(thumbDataURL);
        $('#thumb-img').attr('src', thumbDataURL);
        $('#thumb-crop').cropper('destroy');
        $('#thumb-crop').attr('src', '');
        $('#thumb-img').show();
        $('.thumb label').show();
        $('.thumb .crop-controls').hide();
    });


    $('#admin-delete').click(function() {
        destroy(blogTable.getCheckedIds());
    });
    $('#admin-edit').click(function() {
        edit(blogTable.getCheckedIds());
    });
    $('#admin-activate').click(function() {
        activate(blogTable.getCheckedIds());
    });
    $('#admin-deactivate').click(function() {
        deactivate(blogTable.getCheckedIds());
    });


    $(function() {
        $('#blog-form').submit(function() {
            var aHTML = $('#text-content-editor').summernote('code');
            $('#text_content').val(aHTML);
            return true;
        });
    });
});
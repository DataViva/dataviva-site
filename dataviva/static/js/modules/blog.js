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

    $(function() {
        $('#blog-form').submit(function() {
            var aHTML = $('#text-content-editor').summernote('code');
            $('#text_content').val(aHTML);
            return true;
        });
    });
});


var ScholarApproval = function () {
    this.table = $('#approvalTable').DataTable({
        "sAjaxSource": "/blog/all",
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
                                   '    <input name="postselector" id="'+post[0]+'" type="checkbox">' +
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

};

ScholarApproval.prototype.multipleCheckbox = function(){
    $('#approvalTable thead').on('click','#select-all', function () {
        var posts = {};
        $('input[name="checkboxApproval"]').each(function() {
            posts[this.value] = this.checked;
        });
        sendCheckedArticle(posts);
    });
};

ScholarApproval.prototype.singleCheckbox = function(){
    $('#approvalTable tbody').on('click','.body-checkbox', function () {
        var post = {};
        post[this.firstElementChild.value] = this.firstElementChild.checked;
        sendCheckedArticle(post);
    });
};


ScholarApproval.prototype.controlCheckbox = function(approvalTable){
    $('#select-all').on('click', function(){
       var rows = approvalTable.table.rows({ 'search': 'applied' }).nodes();
       $('input[type="checkbox"]', rows).prop('checked', this.checked);
    });

    $('#approvalTable tbody').on('change', 'input[type="checkbox"]', function(){
       if(!this.checked){
          var el = $('#select-all').get(0);
          if(el && el.checked && ('indeterminate' in el)){
             el.indeterminate = true;
            }
        }
    });
};

var approvalTable = new ScholarApproval();
approvalTable.multipleCheckbox();
approvalTable.singleCheckbox();
approvalTable.controlCheckbox(approvalTable);



function sendCheckedArticle(postsApproval){
    var lang = $('html').attr('lang');
    $.ajax({
      method: "POST",
      url: "/"+lang+"/blog/admin/activate",
      data: postsApproval,
      success: function (msg) {
      }
    })
}
(function(factory){
    if(typeof define==='function'&&define.amd){
        define(['jquery'],factory);
    }else if(typeof module==='object'&&module.exports){
        module.exports=factory(require('jquery'));
    }else{
        factory(window.jQuery);
    }
}
(function($){
    // Button text
    var text = {
        'pt': {
            edit: 'Inserir visualização',
            titleLabel: 'Visualização com iframe',
            tooltip: 'Visualização'
        },
        'en': {
            edit: 'Insert visualization',
            titleLabel: 'Visualization with iframe',
            tooltip: 'Visualization'
        }
    };

    $.extend($.summernote.plugins,{
        'chart':function(context){
            var self=this;
            var ui=$.summernote.ui;
            var $note=context.layoutInfo.note;
            var $editor=context.layoutInfo.editor;
            
            if (typeof context.options.imageTitle === 'undefined') {
                context.options.imageTitle = {};
            }

            if (typeof context.options.imageTitle.specificAltField === 'undefined') {
                context.options.imageTitle.specificAltField = false;
            }

            var options = context.options;
            
            context.memo('button.chart', function () {
                var button = ui.button({
                    // Button icon
                    contents: '<i class="fa fa-area-chart" aria-hidden="true"></i>',
                    tooltip: text[dataviva.language].tooltip,
                    click: function (e) {
                        context.invoke('chart.show');
                    }
                });

                return button.render();
            });

            // Modal showing enter options
            this.initialize = function () {
                var $container = options.dialogsInBody ? $(document.body) : $editor;

                var body = '<div class="form-group">' +
                             '<label>' + text[dataviva.language].titleLabel + '</label>' +
                             '<input class="note-image-title-text form-control" type="text" />' +
                           '</div>';

                var footer = '<button href="#" class="btn btn-primary note-image-title-btn">' + text[dataviva.language].edit + '</button>';
                            
                this.$dialog = ui.dialog({
                    title: text[dataviva.language].edit,
                    body: body,
                    footer: footer
                }).render().appendTo($container);
            };

            this.destroy = function () {
                ui.hideDialog(this.$dialog);

                this.$dialog.remove();
            };

            this.show = function () {

                var urlInfo;

                this.showLinkDialog(urlInfo).then(function (urlInfo) {
                    ui.hideDialog(self.$dialog);

                    context.invoke('focus');

                    // Creating a struct to be responsive
                    var chart = document.createElement('div'),
                        wrapper = document.createElement('div'),
                        img = document.createElement('img'),
                        iframe = document.createElement('iframe');
                        embed = document.createElement('embed');
                    
                    // Placehold to embed graph
                    img.src = "http://placehold.it/1600x900/FFFFFF?text= ";

                    // Getting the given url
                    resquest_iframe = urlInfo.url;
                    
                    if (resquest_iframe.lenght != 0){
                        iframe = $.parseHTML(resquest_iframe)[0];

                        // If iframe wasn't embedded
                        if (iframe.nodeName != "IFRAME") {
                            var url = iframe;
                            embed.src = url.wholeText;
                        }
                        else
                            embed.src = iframe.src;

                        chart.style = "max-width: 868px; height:auto; margin:0px auto;";
                        img.style = "display:block; width:100%; height:100%;";
                        wrapper.style = "position: relative;";
                        wrapper.className = "visu-wrapper";
                        embed.style = "position:absolute; top:0; left:0; width:100%; height:100%;";

                        wrapper.appendChild(img);
                        wrapper.appendChild(embed);
                        chart.appendChild(wrapper);

                        // Restoring focus on text edtion point
                        context.invoke('editor.restoreRange');
                        context.invoke('editor.focus');

                        // Inserting in summernote html
                        context.invoke('editor.insertNode', chart);

                        $note.val(context.invoke('code'));
                        $note.change();
                    }
                });
            };

            this.showLinkDialog = function (urlInfo) {
                return $.Deferred(function (deferred) {
                    var $url = self.$dialog.find('.note-image-title-text'),
                        $editBtn = self.$dialog.find('.note-image-title-btn');

                    ui.onDialogShown(self.$dialog, function () {
                        context.triggerEvent('dialog.shown');

                        // Saving the text edition point
                        context.invoke('editor.saveRange');

                        $url.val('').trigger('focus');

                        $editBtn.click(function (event) {
                            event.preventDefault();
                            deferred.resolve({
                                url: $url.val(),
                            });
                        })
                    });


                    ui.onDialogHidden(self.$dialog, function () {
                        $editBtn.off('click');

                        if (deferred.state() === 'pending') {
                            deferred.reject();
                        }
                    });

                    ui.showDialog(self.$dialog);
                });
            };
        }
    });
}));
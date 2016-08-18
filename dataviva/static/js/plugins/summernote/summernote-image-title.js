(function (factory) {
    /* global define */
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['jquery'], factory);
    } else if (typeof module === 'object' && module.exports) {
        // Node/CommonJS
        module.exports = factory(require('jquery'));
    } else {
        // Browser globals
        factory(window.jQuery);
    }
}(function ($) {
    var text = {
        'pt': {
            edit: 'Salvar',
            titleLabel: 'Legenda',
            tooltip: 'Editar legenda'
        },
        'en': {
            edit: 'Save',
            titleLabel: 'Subtitle',
            tooltip: 'Edit subtitle'
        }
    };

    $.extend($.summernote.plugins, {
        'imageTitle': function (context) {
            var self = this;

            var ui = $.summernote.ui;
            var $note = context.layoutInfo.note;
            var $editor = context.layoutInfo.editor;
            var $editable = context.layoutInfo.editable;

            if (typeof context.options.imageTitle === 'undefined') {
                context.options.imageTitle = {};
            }

            var options = context.options;

            context.memo('button.imageTitle', function () {
                var button = ui.button({
                    contents: ui.icon(options.icons.pencil),
                    tooltip: text[dataviva.language].tooltip,
                    click: function (e) {
                        context.invoke('imageTitle.show');
                    }
                });

                return button.render();
            });

            this.initialize = function () {
                var $container = options.dialogsInBody ? $(document.body) : $editor;

                var body = '<div class="form-group">' +
                             '<label>' + text[dataviva.language].titleLabel + '</label>' +
                             '<input class="note-image-title-text form-control" type="text" />' +
                           '</div>';

                var footer = '<button href="#" class="btn btn-success note-image-title-btn">' + text[dataviva.language].edit + '</button>';
                            
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
                var $img = $($editable.data('target'));
                var imgInfo = {
                    imgDom: $img,
                    title: $img.attr('title'),
                };
                this.showLinkDialog(imgInfo).then(function (imgInfo) {
                    ui.hideDialog(self.$dialog);
                    var $img = imgInfo.imgDom;

                    if (imgInfo.title) {
                        $img.attr('title', imgInfo.title);
                    }
                    else {
                        $img.removeAttr('title');
                    }

                    $note.val(context.invoke('code'));
                    $note.change();
                });
            };

            this.showLinkDialog = function (imgInfo) {
                return $.Deferred(function (deferred) {
                    var $imageTitle = self.$dialog.find('.note-image-title-text'),
                        $editBtn = self.$dialog.find('.note-image-title-btn');

                    ui.onDialogShown(self.$dialog, function () {
                        context.triggerEvent('dialog.shown');

                        $editBtn.click(function (event) {
                            event.preventDefault();
                            deferred.resolve({
                                imgDom: imgInfo.imgDom,
                                title: $imageTitle.val(),
                            });
                            add_caption(imgInfo.imgDom);                           
                        });

                        $imageTitle.val(imgInfo.title).trigger('focus');

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
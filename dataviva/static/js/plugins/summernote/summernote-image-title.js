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
            altLabel: 'Fonte',
            tooltip: 'Editar legenda'
        },
        'en': {
            edit: 'Save',
            titleLabel: 'Caption',
            altLabel: 'Source',
            tooltip: 'Edit caption'
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

            if (typeof context.options.imageTitle.specificAltField === 'undefined') {
                context.options.imageTitle.specificAltField = false;
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

                if (options.imageTitle.specificAltField) {
                    body += '<div class="form-group">' +
                               '<label>' + text[dataviva.language].altLabel + '</label>' +
                               '<input class="note-image-alt-text form-control" type="text" />' +
                             '</div>';
                }

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
                    title: $img.attr('data-original-title'),
                    alt: $img.attr('title')
                };
                this.showLinkDialog(imgInfo).then(function (imgInfo) {
                    ui.hideDialog(self.$dialog);
                    var $img = imgInfo.imgDom;

                    if (imgInfo.alt) {
                        $img.attr('title', imgInfo.alt);
                    }
                    else {
                        $img.removeAttr('title');
                    }

                    if (imgInfo.title) {
                        $img.attr('data-original-title', imgInfo.title);
                    }
                    else {
                        $img.removeAttr('data-original-title');
                    }

                    $note.val(context.invoke('code'));
                    $note.change();
                });
            };

            this.showLinkDialog = function (imgInfo) {
                return $.Deferred(function (deferred) {
                    var $imageTitle = self.$dialog.find('.note-image-title-text'),
                        $imageAlt = (options.imageTitle.specificAltField) ? self.$dialog.find('.note-image-alt-text') : null,
                        $editBtn = self.$dialog.find('.note-image-title-btn');

                    ui.onDialogShown(self.$dialog, function () {
                        context.triggerEvent('dialog.shown');

                        $editBtn.click(function (event) {
                            event.preventDefault();
                            deferred.resolve({
                                imgDom: imgInfo.imgDom,
                                title: $imageTitle.val(),
                                alt: (options.imageTitle.specificAltField) ? $imageAlt.val() : $imageTitle.val(),
                            });
                        });

                        $imageTitle.val(imgInfo.title).trigger('focus');

                        if (options.imageTitle.specificAltField)
                            $imageAlt.val(imgInfo.alt);

                        imgInfo.imgDom
                            .attr('data-toggle', 'tooltip')
                            .attr('data-placement', 'bottom');
                        load_tooltip(imgInfo.imgDom);
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
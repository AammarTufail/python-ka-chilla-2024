window.CopyTheCodeToClipboard = (function (window, document, navigator) {
    var textArea,
        copy;

    function isOS() {
        return navigator.userAgent.match(/ipad|iphone/i);
    }

    function createTextArea(text) {
        textArea = document.createElement('textArea');
        textArea.value = text;
        document.body.appendChild(textArea);
    }

    function selectText() {
        var range,
            selection;

        if (isOS()) {
            range = document.createRange();
            range.selectNodeContents(textArea);
            selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
            textArea.setSelectionRange(0, 999999);
        } else {
            textArea.select();
        }
    }

    function copyToClipboard() {
        document.execCommand('copy');
        document.body.removeChild(textArea);

        // Redirect to page.
        if( copyTheCode.redirect_url ) {
            window.location.href = copyTheCode.redirect_url;
        }
    }

    copy = function (text) {
        createTextArea(text);
        selectText();
        copyToClipboard();
    };

    return {
        copy: copy
    };
})(window, document, navigator);

(function ($) {

    CopyTheCode = {

        selector: copyTheCode.settings.selector || copyTheCode.selector || 'pre',
        button_position: copyTheCode.settings['button-position'] || 'inside',

        /**
         * Init
         */
        init: function () {
            this._bind();
            this._initialize();
        },

        /**
         * Binds events
         */
        _bind: function () {
            $(document).on('click', '.copy-the-code-button', CopyTheCode.copyCode);
            $(document).on('click', '.copy-the-code-shortcode', CopyTheCode.copyShortcode);
        },

        /**
         * Initialize the Button
         */
        _initialize: function () {
            if (!$(copyTheCode.selectors).length) {
                return;
            }

            $(copyTheCode.selectors).each(function (index, el) {
                var button_copy_text = el['button_copy_text'] || '';
                var button_position = el['button_position'] || '';
                var button_text = el['button_text'] || '';
                var button_title = el['button_title'] || '';
                var selector = el['selector'] || '';
                var style = el['style'] || '';
                var copy_format = el['copy_format'] || '';

                $(selector).each(function (index, single_selector) {

                    var buttonMarkup = CopyTheCode._getButtonMarkup(button_title, button_text, style);

                    $(single_selector).addClass('copy-the-code-target');

                    if ('cover' !== style && 'outside' === button_position) {
                        $(single_selector).wrap('<span data-copy-format="' + copy_format + '" data-button-text="' + button_text + '" data-button-position="' + button_position + '" data-button-copy-text="' + button_copy_text + '" data-style="' + style + '" data-button-title="' + button_title + '" data-selector="' + selector + '" class="copy-the-code-wrap copy-the-code-style-' + style + ' copy-the-code-outside-wrap"></span>');
                        $(single_selector).parent().prepend('<div class="copy-the-code-outside">' + buttonMarkup + '</div>');
                    } else {
                        $(single_selector).wrap('<span data-copy-format="' + copy_format + '" data-button-text="' + button_text + '" data-button-position="' + button_position + '" data-button-copy-text="' + button_copy_text + '" data-style="' + style + '" data-button-title="' + button_title + '" data-selector="' + selector + '" class="copy-the-code-wrap copy-the-code-style-' + style + ' copy-the-code-inside-wrap"></span>');
                        $(single_selector).append(buttonMarkup);
                    }

                    switch (style) {
                        case 'svg-icon':
                            $(single_selector).find('.copy-the-code-button').html(copyTheCode.buttonSvg);
                            break;
                        case 'cover':
                        case 'button':
                        default:
                            $(single_selector).find('.copy-the-code-button').html(button_text);
                            break;
                    }


                });
            });

        },

        /**
         * Get Copy Button Markup
         */
        _getButtonMarkup: function (button_title, button_text, style) {
            if ('svg-icon' === style) {
                button_text = copyTheCode.buttonSvg;
            }

            return '<button class="copy-the-code-button" data-style="' + style + '" title="' + button_title + '">' + button_text + '</button>';
        },

        format: function (html) {
            var tab = '\t';
            var result = '';
            var indent = '';

            html.split(/>\s*</).forEach(function (element) {
                if (element.match(/^\/\w/)) {
                    indent = indent.substring(tab.length);
                }

                result += indent + '<' + element + '>\r\n';

                if (element.match(/^<?\w[^>]*[^\/]$/) && !element.startsWith("input")) {
                    indent += tab;
                }
            });

            return result.substring(1, result.length - 3);
        },

        /**
         * Copy to Clipboard
         */
        copyShortcode: function (event) {
            event.preventDefault();

            var btn = $(this),
                oldText = btn.html(),
                target = btn.attr('data-target') || '',
                copy_content_as = btn.attr('data-copy-as') || copyTheCode.copy_content_as,
                button_copy_text = btn.attr('data-button-copy-text') || '',
                content = btn.attr('data-content') || '',
                link = btn.attr( 'data-link' ) || '';

            // Copy the secrate content.
            if (content) {
                CopyTheCodeToClipboard.copy(content);
                // Copied!
                btn.text(button_copy_text);
                setTimeout(function () {
                    btn.html(oldText);

                    if( link ) {
                        window.open(link, '_blank').focus()
                    }
                }, 1000);
                return;
            }

            var source = $(target);

            if (!source.length) {
                btn.text('Not found!');
                setTimeout(function () {
                    btn.text(oldText);
                }, 1000);
                return;
            }

            var html = source.html();

            html = CopyTheCode.format(html);

            if ('html' !== copy_content_as) {

                // Convert the <br/> tags into new line.
                var brRegex = /<br\s*[\/]?>/gi;
                html = html.replace(brRegex, "\n");

                // Convert the <div> tags into new line.
                var divRegex = /<div\s*[\/]?>/gi;
                html = html.replace(divRegex, "\n");

                // Convert the <p> tags into new line.
                var pRegex = /<p\s*[\/]?>/gi;
                html = html.replace(pRegex, "\n");

                // Convert the <li> tags into new line.
                var pRegex = /<li\s*[\/]?>/gi;
                html = html.replace(pRegex, "\n");

                // Remove all tags.
                html = html.replace(/(<([^>]+)>)/ig, '');
            }

            if ('html' !== copy_content_as) {
                html = html.replace(/[\t\n]+/gm, ' ').trim();
            } else {
                var reWhiteSpace = new RegExp("/^\s+$/");
                html = html.replace(reWhiteSpace, "");
            }

            var tempElement = $("<div id='temp-element'></div>");
            $("body").append(tempElement);
            html = $.trim(html);
            $('#temp-element').html(html);
            var html = $('#temp-element').html();
            $('#temp-element').remove();

            var tempHTML = html;

            // Copy the Code.
            var tempPre = $("<textarea id='temp-pre'>"),
                temp = $("<textarea>");

            // Append temporary elements to DOM.
            $("body").append(temp);
            $("body").append(tempPre);

            // Set temporary HTML markup.
            tempPre.html(tempHTML);

            var content = tempPre.text();

            content = content.trim();

            if( copyTheCode.trim_lines ) {
                content = content.replace(/^(?=\n)$|\s*$|\n\n+/gm,"");
                if( content ) {
                    content = content.split('\n');
                    content = content.map( item => {
                        return item.trim();
                    } );
                    content = content.join('\n');
                }
            }

            // Format the HTML markup.
            temp.val(content).select();

            // Support for IOS devices too.
            CopyTheCodeToClipboard.copy(content.trim());

            // Remove temporary elements.
            temp.remove();
            tempPre.remove();

            // Copied!
            btn.text(button_copy_text);
            setTimeout(function () {
                btn.text(oldText);
            }, 1000);
        },

        /**
         * Copy to Clipboard
         */
        copyCode: function (event) {
            event.preventDefault();

            var btn = $(this),
                oldText = btn.text(),
                parent = btn.parents('.copy-the-code-wrap'),
                selector = parent.attr('data-selector') || '',
                button_text = parent.attr('data-button-text') || '',
                button_position = parent.attr('data-button-position') || '',
                button_copy_text = parent.attr('data-button-copy-text') || '',
                button_title = parent.attr('data-button-title') || '',
                style = parent.attr('data-style') || ''
                copy_format = parent.attr('data-copy-format') || '';

            // Fix: nested selectors e.g. `.entry-content pre`
            if (selector.indexOf(' ') >= 0) {
                var source = btn.parents('.copy-the-code-wrap');
            } else {
                var source = btn.parents('.copy-the-code-wrap').find(selector);
            }

            if ( 'google-docs' === copy_format ) {
                // Hide button temporary.
                if ( 'inside' === button_position ) {
                    $( '.copy-the-code-button' ).hide();
                }

                var range = document.createRange();
                range.selectNode(source[0]);
                window.getSelection().addRange(range);
                document.execCommand('copy');

                // Clear selection.
                if (window.getSelection) {
                    if (window.getSelection().empty) {  // Chrome
                        window.getSelection().empty();
                    } else if (window.getSelection().removeAllRanges) {  // Firefox
                        window.getSelection().removeAllRanges();
                    }
                } else if (document.selection) {  // IE?
                    document.selection.empty();
                }

                // Show button again.
                if ( 'inside' === button_position ) {
                    $( '.copy-the-code-button' ).show();
                }

            } else {

                var html = source.html();

                var buttonMarkup = CopyTheCode._getButtonMarkup(button_title, button_text, style);

                // Remove the <copy> button.
                html = html.replace(buttonMarkup, '');

                // Emojis.
                let allEmojis = CopyTheCode._getImages( html );

                if ( allEmojis ) {
                    allEmojis.map( function(image) {
                        let alt = CopyTheCode._getAlt( image );
                        if ( alt ) {
                            let cleanAlt = alt[0];
                            cleanAlt = cleanAlt.replaceAll( '"', '' );
                            cleanAlt = cleanAlt.replaceAll( "'", '' );
                            cleanAlt = cleanAlt.replaceAll( 'alt=', '' );
                            html = html.replaceAll( image, cleanAlt );
                        }
                    });

                }

                // Remove all duplicate empty lines.
                if( copyTheCode.remove_spaces ) {
                    html = html.replace(/^(?=\n)$|\s*$|\n\n+/gm,"");
                }

                if ('html' !== copyTheCode.copy_content_as) {
                    // Convert the <br/> tags into new line.
                    var brRegex = /<br\s*[\/]?>/gi;
                    html = html.replace(brRegex, "\n");

                    // Convert the <div> tags into new line.
                    var divRegex = /<div\s*[\/]?>/gi;
                    html = html.replace(divRegex, "\n");

                    // Convert the <p> tags into new line.
                    var pRegex = /<p\s*[\/]?>/gi;
                    html = html.replace(pRegex, "\n");

                    // Convert the <li> tags into new line.
                    var pRegex = /<li\s*[\/]?>/gi;
                    html = html.replace(pRegex, "\n");

                    // Remove all tags.
                    html = html.replace(/(<([^>]+)>)/ig, '');
                }

                // Remove white spaces.
                var reWhiteSpace = new RegExp("/^\s+$/");
                html = html.replace(reWhiteSpace, "");

                var tempElement = $("<div id='temp-element'></div>");
                $("body").append(tempElement);
                html = $.trim(html);
                $('#temp-element').html(html);
                var html = $('#temp-element').html();
                $('#temp-element').remove();

                var tempHTML = html;
                var reWhiteSpace = new RegExp("/^\s+$/");
                tempHTML = tempHTML.replace(reWhiteSpace, "");

                // Remove button text.
                tempHTML = tempHTML.replace(button_text, '');

                // Copy the Code.
                var tempPre = $("<textarea id='temp-pre'>"),
                    temp = $("<textarea>");

                // Append temporary elements to DOM.
                $("body").append(temp);
                $("body").append(tempPre);

                // Set temporary HTML markup.
                var content = tempPre.html(tempHTML).text();

                content = $.trim(content);

                // Format the HTML markup.
                temp.val(content).select();

                // Support for IOS devices too.
                CopyTheCodeToClipboard.copy(content);

                // Remove temporary elements.
                temp.remove();
                tempPre.remove();
            }

            // Copied!
            btn.text(button_copy_text);
            setTimeout(function () {
                if ('svg-icon' === style) {
                    btn.html(copyTheCode.buttonSvg);
                } else {
                    btn.text(oldText);
                }
            }, 1000);
        },

        _getImages( content ) {
            return content.match( /<img\s+[^>]*?src=("|')([^"']+)">/gi );
        },

        _getAlt( img ) {
            return img.match( /alt=("|')([^"']+)"|'/gi );
        }

    };

    /**
     * Initialization
     */
    $(function () {
        CopyTheCode.init();
    });

})(jQuery);
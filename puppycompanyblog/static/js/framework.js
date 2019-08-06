(function ($) {
    'use strict';
    var Accordion = function (elm, options) {
        var self,
            $this = $( elm ),
            $items = $( '[data-rt-accordion-item]', $this ),
            $header = $( 'header', $items ),
            slideItem = function ( direction, $item ) {
                if ( direction == 'up' ) {
                    $item
                        .removeClass( 'active' )
                        .find( '.content' )
                        .slideUp().end()
                        .find( 'header span' )
                        .removeClass( 'wicon-iconmonstr-minus-thin' )
                        .addClass( 'wicon-iconmonstr-plus-thin' );
                } else if ( direction == 'down' ) {
                     if ( options.toggle ) {
                        $items
                            .removeClass( 'active' )
                            .find( '.content' )
                            .slideUp().end()
                            .find( 'header span' )
                            .removeClass( 'wicon-iconmonstr-minus-thin' )
                            .addClass( 'wicon-iconmonstr-plus-thin' );
                     }
                     $item.addClass( 'active' )
                        .find( '.content' )
                        .slideDown().end().
                        find( 'header span' )
                        .removeClass( 'wicon-iconmonstr-plus-thin' )
                        .addClass( 'wicon-iconmonstr-minus-thin' );
               }
            },
            init = function () {
                $items.find( '.content' ).hide();
                $( '<span class="wicon-iconmonstr-plus-thin"></span>' ).appendTo( $header );
                if ( options.active ) {
                    $items
                    .eq( options.active )
                    .addClass( 'active' )
                    .find( '.content' )
                    .show().end()
                    .find( 'header span' )
                    .removeClass( 'wicon-iconmonstr-plus-thin' )
                    .addClass( 'wicon-iconmonstr-minus-thin' );
                }
                $header.on( 'click', function () {
                    var $item = $( this ).parents( '[data-rt-accordion-item]' );
                    if ( $item.hasClass( 'active' ) ) {
                        slideItem( 'up', $item );
                    } else {
                        slideItem( 'down', $item );
                    }
                } );
            };
        self = {
            init: init
        };
        return self;
    };
    $.fn.rtAccordion = function (opt) {
        return this.each(function () {
            var accordion;
            if (!$(this).data('rtAccordion')) {
                accordion = new Accordion(this, $.extend(true, {
                    active: ( $(this).data('rt-accordion-active') === undefined ) ? 0 : $(this).data('rt-accordion-active') - 1,
                    toggle: ( $(this).data('rt-accordion-toggle') === undefined ) ? 0 : $(this).data('rt-accordion-toggle'),
                }, opt));
                accordion.init();
                $(this).data('rtAccordion', accordion);
            }
        });
    };
    var $rtAccordion = $( '[data-rt-accordion]' );
    if ( $rtAccordion.length ) {
        $rtAccordion.rtAccordion();
    }
}(jQuery));
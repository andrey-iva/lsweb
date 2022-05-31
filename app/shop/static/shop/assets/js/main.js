(function($) {
    "use strict";
    //
    $("#phone").intlTelInput({
        geoIpLookup: function(success, failure) {
            $.get("https://ipinfo.io", function() {}, "jsonp").always(function(resp) {
              var countryCode = (resp && resp.country) ? resp.country : "us";
              success(countryCode);

              if (countryCode === "RU") {
                $('#phone').mask('000 000-00-00')
              }

              if (countryCode === "BY") {
                $('#phone').mask('00 000-00-00')
              }

              if (countryCode === "KZ") {
                $('#phone').mask('000 000 0000')
              }
              
            });
        },
        initialCountry: "auto",
        preferredCountries: ["ru"],
        separateDialCode: true,
        onlyCountries: ["ru", "by", "kz"],
        utilsScript: "/static/shop/assets/js/inttel/js/utils.js",
    })

    $("#order_create").submit(function(e) {
        if ($("#phone").val()[0] !== "+") {
            $("#phone").val( $(".iti__selected-dial-code").text() + " " + $("#phone").val() )
        }
    });

    // $('#phone').mask('000-000-00-00');

    /*------ ScrollUp -------- */
    $.scrollUp({
        scrollText: '<i class="icon-arrow-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    });

    /*------ Wow Active ----*/
    new WOW().init();

    /*------ Hero slider active 1 Главная банер----*/
    $('.hero-slider-active-1').slick({
        autoplay: true,
        autoplaySpeed: 10000,
        slidesToShow: 1,
        slidesToScroll: 1,
        fade: true,
        loop: true,
        dots: true,
        arrows: true,
        pauseOnHover: true,
        pauseOnDotsHover: true,
        focusOnSelect: true,
        prevArrow: '<span class="slider-icon-1-prev"><i class="icon-arrow-left"></i></span>',
        nextArrow: '<span class="slider-icon-1-next"><i class="icon-arrow-right"></i></span>',

    });

    /*------ Hero slider active 2 ----*/
    // $('.hero-slider-active-2').slick({
    //     slidesToShow: 1,
    //     slidesToScroll: 1,
    //     fade: true,
    //     loop: true,
    //     dots: false,
    //     arrows: true,
    //     prevArrow: '<span class="slider-icon-1-prev"><i class="icon-arrow-left"></i></span>',
    //     nextArrow: '<span class="slider-icon-1-next"><i class="icon-arrow-right"></i></span>',
    // });

    /*------ Hero slider active 3 ----*/
    // $('.hero-slider-active-3').slick({
    //     slidesToShow: 1,
    //     slidesToScroll: 1,
    //     fade: true,
    //     loop: true,
    //     dots: true,
    //     arrows: false,
    // });

    /*------ Product slider active ----*/
    // $('div.product-slider-active').slick({
    //     autoplay: true,
    //     autoplaySpeed: 5000,
    //     slidesToShow: 4,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: true,
    //     arrows: false,
    //     responsive: [{
    //             breakpoint: 1199,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 991,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 767,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 575,
    //             settings: {
    //                 slidesToShow: 1,
    //             }
    //         }
    //     ]
    // });

    /*------ Product slider active 2 ----*/
    // $('.product-slider-active-2').slick({
    //     slidesToShow: 3,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: true,
    //     rows: 2,
    //     arrows: false,
    //     responsive: [{
    //             breakpoint: 1199,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 991,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 767,
    //             settings: {
    //                 slidesToShow: 1,
    //             }
    //         },
    //         {
    //             breakpoint: 575,
    //             settings: {
    //                 slidesToShow: 1,
    //             }
    //         }
    //     ]
    // });


    /*------ Product slider active 3 ----*/
    // $('.product-slider-active-3').slick({
    //     slidesToShow: 5,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: false,
    //     arrows: true,
    //     prevArrow: '<span class="pro-slider-icon-1-prev"><i class="icon-arrow-left"></i></span>',
    //     nextArrow: '<span class="pro-slider-icon-1-next"><i class="icon-arrow-right"></i></span>',
    //     responsive: [{
    //             breakpoint: 1199,
    //             settings: {
    //                 slidesToShow: 4,
    //             }
    //         },
    //         {
    //             breakpoint: 991,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 767,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 575,
    //             settings: {
    //                 slidesToShow: 1,
    //             }
    //         }
    //     ]
    // });

    /*------ Product slider active 4 ----*/
    // $('.product-slider-active-4').slick({
    //     slidesToShow: 4,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: false,
    //     arrows: true,
    //     prevArrow: '<span class="pro-slider-icon-1-prev"><i class="icon-arrow-left"></i></span>',
    //     nextArrow: '<span class="pro-slider-icon-1-next"><i class="icon-arrow-right"></i></span>',
    //     responsive: [{
    //             breakpoint: 1199,
    //             settings: {
    //                 slidesToShow: 4,
    //             }
    //         },
    //         {
    //             breakpoint: 991,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 767,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 575,
    //             settings: {
    //                 slidesToShow: 1,
    //             }
    //         }
    //     ]
    // });

    /*------ Product slider active 5 ----*/
    // $('.product-slider-active-5').slick({
    //     slidesToShow: 4,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: false,
    //     arrows: false,
    //     responsive: [{
    //             breakpoint: 1199,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 991,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 767,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 575,
    //             settings: {
    //                 slidesToShow: 1,
    //             }
    //         }
    //     ]
    // });

    /*------ product categories slider 1 ----*/
    // $('.product-categories-slider-1').slick({
    //     slidesToShow: 6,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: false,
    //     arrows: true,
    //     prevArrow: '<span class="pro-slider-icon-1-prev"><i class="icon-arrow-left"></i></span>',
    //     nextArrow: '<span class="pro-slider-icon-1-next"><i class="icon-arrow-right"></i></span>',
    //     responsive: [{
    //             breakpoint: 1199,
    //             settings: {
    //                 slidesToShow: 4,
    //             }
    //         },
    //         {
    //             breakpoint: 991,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 767,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 575,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         }
    //     ]
    // });

    /*------ Product categories slider 3 ----*/
    // $('.product-categories-slider-3').slick({
    //     slidesToShow: 6,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: false,
    //     arrows: true,
    //     rows: 2,
    //     prevArrow: '<span class="pro-slider-icon-1-prev"><i class="icon-arrow-left"></i></span>',
    //     nextArrow: '<span class="pro-slider-icon-1-next"><i class="icon-arrow-right"></i></span>',
    //     responsive: [{
    //             breakpoint: 1199,
    //             settings: {
    //                 slidesToShow: 4,
    //             }
    //         },
    //         {
    //             breakpoint: 991,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 767,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 575,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         }
    //     ]
    // });


    /*--- Language currency active ----*/
    // $('.language-dropdown-active').on('click', function(e) {
    //     e.preventDefault();
    //     $('.language-dropdown').slideToggle(400);
    // });
    // $('.currency-dropdown-active').on('click', function(e) {
    //     e.preventDefault();
    //     $('.currency-dropdown').slideToggle(400);
    // });

    /*====== SidebarCart ======*/
    function miniCart() {
        var navbarTrigger = $('.cart-active'),
            endTrigger = $('.cart-close'),
            container = $('.sidebar-cart-active'),
            wrapper = $('.main-wrapper');

        wrapper.prepend('<div class="body-overlay"></div>');

        navbarTrigger.on('click', function(e) {
            e.preventDefault();
            container.addClass('inside');
            wrapper.addClass('overlay-active');
        });

        endTrigger.on('click', function() {
            container.removeClass('inside');
            wrapper.removeClass('overlay-active');
        });

        $('.body-overlay').on('click', function() {
            container.removeClass('inside');
            wrapper.removeClass('overlay-active');
        });
    };
    miniCart();

    /*-------------------------------
       Header Search Toggle
    -----------------------------------*/
    // var searchToggle = $('.search-toggle');
    // searchToggle.on('click', function(e) {
    //     e.preventDefault();
    //     if ($(this).hasClass('open')) {
    //         $(this).removeClass('open');
    //         $(this).siblings('.search-wrap-1').removeClass('open');
    //     } else {
    //         $(this).addClass('open');
    //         $(this).siblings('.search-wrap-1').addClass('open');
    //     }
    // })


    /* NiceSelect */
    $('.nice-select').niceSelect();


    /*-------------------------
      Category active
    --------------------------*/
    // $('.categori-show').on('click', function(e) {
    //     e.preventDefault();
    //     $('.categori-hide , .categori-hide-2').slideToggle(900);
    // });

    /*--------------------------------
        Deal slider active
    -----------------------------------*/
    // $('.deal-slider-active').slick({
    //     slidesToShow: 1,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: false,
    //     arrows: true,
    //     prevArrow: '<span class="slider-icon-1-prev"><i class="icon-arrow-left"></i></span>',
    //     nextArrow: '<span class="slider-icon-1-next"><i class="icon-arrow-right"></i></span>',
    // });


    /*--------------------------------
        Sidebar product active
    -----------------------------------*/
    // $('.sidebar-product-active').slick({
    //     slidesToShow: 1,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: false,
    //     rows: 3,
    //     arrows: true,
    //     prevArrow: '<span class="sidebar-icon-prev"><i class="icon-arrow-left"></i></span>',
    //     nextArrow: '<span class="sidebar-icon-next"><i class="icon-arrow-right"></i></span>',
    // });

    /*--------------------------------
        Sidebar blog active
    -----------------------------------*/
    // $('.sidebar-blog-active').slick({
    //     slidesToShow: 1,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: false,
    //     rows: 2,
    //     arrows: true,
    //     prevArrow: '<span class="sidebar-icon-prev"><i class="icon-arrow-left"></i></span>',
    //     nextArrow: '<span class="sidebar-icon-next"><i class="icon-arrow-right"></i></span>',
    // });

    /*--------------------------------
        Product categories slider
    -----------------------------------*/
    // $('.product-categories-slider-2').slick({
    //     slidesToShow: 5,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: false,
    //     arrows: true,
    //     prevArrow: '<span class="sidebar-icon-prev"><i class="icon-arrow-left"></i></span>',
    //     nextArrow: '<span class="sidebar-icon-next"><i class="icon-arrow-right"></i></span>',
    //     responsive: [{
    //             breakpoint: 1199,
    //             settings: {
    //                 slidesToShow: 4,
    //             }
    //         },
    //         {
    //             breakpoint: 991,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 767,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 575,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         }
    //     ]
    // });

    /*--------------------------------
        Testimonial active
    -----------------------------------*/
    // $('.testimonial-active-1').slick({
    //     slidesToShow: 1,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: true,
    //     arrows: false,
    // });
    /*--------------------------------
        Testimonial active 2
    -----------------------------------*/
    // $('.testimonial-active-2').slick({
    //     slidesToShow: 1,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: false,
    //     arrows: false,
    // });

    /*--------------------------------
        Product slider active 6
    -----------------------------------*/
    // $('.product-slider-active-6').slick({
    //     slidesToShow: 2,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: true,
    //     rows: 2,
    //     arrows: false,
    //     responsive: [{
    //             breakpoint: 1199,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 991,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 767,
    //             settings: {
    //                 slidesToShow: 1,
    //             }
    //         },
    //         {
    //             breakpoint: 575,
    //             settings: {
    //                 slidesToShow: 1,
    //             }
    //         }
    //     ]
    // });

    /*--------------------------------
        Product slider active 7
    -----------------------------------*/
    // $('.product-slider-active-7').slick({
    //     slidesToShow: 4,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: true,
    //     rows: 2,
    //     arrows: false,
    //     responsive: [{
    //             breakpoint: 1199,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 991,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 767,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 575,
    //             settings: {
    //                 slidesToShow: 1,
    //             }
    //         }
    //     ]
    // });

    /*--------------------------------
        Product slider active 8
    -----------------------------------*/
    // $('.product-slider-active-8').slick({
    //     slidesToShow: 5,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: true,
    //     arrows: true,
    //     prevArrow: '<span class="sidebar-icon-prev"><i class="icon-arrow-left"></i></span>',
    //     nextArrow: '<span class="sidebar-icon-next"><i class="icon-arrow-right"></i></span>',
    //     responsive: [{
    //             breakpoint: 1199,
    //             settings: {
    //                 slidesToShow: 4,
    //             }
    //         },
    //         {
    //             breakpoint: 991,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 767,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 575,
    //             settings: {
    //                 slidesToShow: 1,
    //             }
    //         }
    //     ]
    // });

    /*--------------------------------
        Product slider active 9
    -----------------------------------*/
    // $('.product-slider-active-9').slick({
    //     slidesToShow: 4,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: true,
    //     arrows: false,
    //     responsive: [{
    //             breakpoint: 1199,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 991,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 767,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 575,
    //             settings: {
    //                 slidesToShow: 1,
    //             }
    //         }
    //     ]
    // });

    /*------- Color active -----*/
    $('.pro-details-color-content').on('click', 'a', function(e) {
        e.preventDefault();
        $(this).addClass('active').parent().siblings().children('a').removeClass('active');
    });

    /*--------------------------------
        Social icon active
    -----------------------------------*/
    if ($('.pro-details-action').length) {
        var $body = $('body'),
            $cartWrap = $('.pro-details-action'),
            $cartContent = $cartWrap.find('.product-dec-social');
        $cartWrap.on('click', '.social', function(e) {
            e.preventDefault();
            var $this = $(this);
            if (!$this.parent().hasClass('show')) {
                $this.siblings('.product-dec-social').addClass('show').parent().addClass('show');
            } else {
                $this.siblings('.product-dec-social').removeClass('show').parent().removeClass('show');
            }
        });
        /*Close When Click Outside*/
        $body.on('click', function(e) {
            var $target = e.target;
            if (!$($target).is('.pro-details-action') && !$($target).parents().is('.pro-details-action') && $cartWrap.hasClass('show')) {
                $cartWrap.removeClass('show');
                $cartContent.removeClass('show');
            }
        });
    }

    /*---------------------
        Price range
    --------------------- */
    var sliderrange = $('#slider-range');
    var amountprice = $('#amount');
    $(function() {
        sliderrange.slider({
            range: true,
            min: 16,
            max: 400,
            values: [0, 300],
            slide: function(event, ui) {
                amountprice.val("$" + ui.values[0] + " - $" + ui.values[1]);
            }
        });
        amountprice.val("$" + sliderrange.slider("values", 0) +
            " - $" + sliderrange.slider("values", 1));
    });

    /*----------------------------
        Cart Plus Minus Button
    ------------------------------ */
    var CartPlusMinus = $('.cart-plus-minus');
    CartPlusMinus.prepend('<div class="dec qtybutton">-</div>');
    CartPlusMinus.append('<div class="inc qtybutton">+</div>');
    $(".qtybutton").on("click", function() {
        var $button = $(this);
        var oldValue = $button.parent().find("input").val();
        if ($button.text() === "+") {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 1) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 1;
            }
        }
        if (newVal > 100) {
            newVal = 100
        }
        $button.parent().find("input").val(newVal);
    });

    /*====== Sidebar menu Active ======*/
    function mobileHeaderActive() {
        var navbarTrigger = $('.mobile-header-button-active'),
            endTrigger = $('.sidebar-close'),
            container = $('.mobile-header-active'),
            wrapper4 = $('.main-wrapper');

        wrapper4.prepend('<div class="body-overlay-1"></div>');

        navbarTrigger.on('click', function(e) {
            e.preventDefault();
            container.addClass('sidebar-visible');
            wrapper4.addClass('overlay-active-1');
        });

        endTrigger.on('click', function() {
            container.removeClass('sidebar-visible');
            wrapper4.removeClass('overlay-active-1');
        });

        $('.body-overlay-1').on('click', function() {
            container.removeClass('sidebar-visible');
            wrapper4.removeClass('overlay-active-1');
        });
    };
    mobileHeaderActive();

    /*---------------------
        mobile-menu
    --------------------- */
    var $offCanvasNav = $('.mobile-menu , .category-menu-dropdown'),
        $offCanvasNavSubMenu = $offCanvasNav.find('.dropdown');

    /*Add Toggle Button With Off Canvas Sub Menu*/
    $offCanvasNavSubMenu.parent().prepend('<span class="menu-expand"><i></i></span>');

    /*Close Off Canvas Sub Menu*/
    $offCanvasNavSubMenu.slideUp();

    /*Category Sub Menu Toggle*/
    $offCanvasNav.on('click', 'li a, li .menu-expand', function(e) {
        var $this = $(this);
        try {
            if (($this.parent().attr('class').match(/\b(menu-item-has-children|has-children|has-sub-menu)\b/)) && ($this.attr('href') === '#' || $this.hasClass('menu-expand'))) {
                e.preventDefault();
                if ($this.siblings('ul:visible').length) {
                    $this.parent('li').removeClass('active');
                    $this.siblings('ul').slideUp();
                } else {
                    $this.parent('li').addClass('active');
                    $this.closest('li').siblings('li').removeClass('active').find('li').removeClass('active');
                    $this.closest('li').siblings('li').find('ul:visible').slideUp();
                    $this.siblings('ul').slideDown();
                }
            }
        } catch(err) {
            console.info(err)
        }
    });


    /*--- checkout toggle function ----*/
    // $('.checkout-click1').on('click', function(e) {
    //     e.preventDefault();
    //     $('.checkout-login-info').slideToggle(900);
    // });


    /*--- checkout toggle function ----*/
    // $('.checkout-click3').on('click', function(e) {
    //     e.preventDefault();
    //     $('.checkout-login-info3').slideToggle(1000);
    // });

    /*-------------------------
    Create an account toggle
    --------------------------*/
    // $('.checkout-toggle2').on('click', function() {
    //     $('.open-toggle2').slideToggle(1000);
    // });

    // $('.checkout-toggle').on('click', function() {
    //     $('.open-toggle').slideToggle(1000);
    // });

    /*-------------------------
    checkout one click toggle function
    --------------------------*/
    // var checked = $('.sin-payment input:checked')
    // if (checked) {
    //     $(checked).siblings('.payment-box').slideDown(900);
    // };
    // $('.sin-payment input').on('change', function() {
    //     $('.payment-box').slideUp(900);
    //     $(this).siblings('.payment-box').slideToggle(900);
    // });


    // Instantiate EasyZoom instances
    // var $easyzoom = $('.easyzoom').easyZoom();

    /*-------------------------------------
        Product details big image slider
    ---------------------------------------*/
    $('.pro-dec-big-img-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        draggable: false,
        fade: false,
        asNavFor: '.product-dec-slider-small , .product-dec-slider-small-2',
    });

    /*---------------------------------------
        Product details small image slider
    -----------------------------------------*/
    $('.product-dec-slider-small').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        asNavFor: '.pro-dec-big-img-slider',
        dots: false,
        focusOnSelect: true,
        fade: false,
        prevArrow: '<span class="pro-dec-prev"><i class="icon-arrow-left"></i></span>',
        nextArrow: '<span class="pro-dec-next"><i class="icon-arrow-right"></i></span>',
        responsive: [{
                breakpoint: 991,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 767,
                settings: {
                    slidesToShow: 4,
                }
            },
            {
                breakpoint: 575,
                settings: {
                    slidesToShow: 2,
                }
            }
        ]
    });

    /*----------------------------------------
        Product details small image slider 2
    ------------------------------------------*/
    $('.product-dec-slider-small-2').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        vertical: true,
        asNavFor: '.pro-dec-big-img-slider',
        dots: false,
        focusOnSelect: true,
        fade: false,
        prevArrow: '<span class="pro-dec-prev"><i class="icon-arrow-up"></i></span>',
        nextArrow: '<span class="pro-dec-next"><i class="icon-arrow-down"></i></span>',
        responsive: [{
                breakpoint: 1365,
                settings: {
                    slidesToShow: 4,
                }
            },
            {
                breakpoint: 1199,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 991,
                settings: {
                    slidesToShow: 4,
                }
            },
            {
                breakpoint: 767,
                settings: {
                    slidesToShow: 4,
                }
            },
            {
                breakpoint: 575,
                settings: {
                    slidesToShow: 2,
                }
            }
        ]
    });


    /*--
        Magnific Popup
    ------------------------*/
    $('.img-popup').magnificPopup({
        type: 'image',
        gallery: {
            enabled: true
        }
    });

    // $('.related-product-active').slick({
    //     slidesToShow: 4,
    //     slidesToScroll: 1,
    //     fade: false,
    //     loop: true,
    //     dots: false,
    //     arrows: false,
    //     responsive: [{
    //             breakpoint: 1199,
    //             settings: {
    //                 slidesToShow: 3,
    //             }
    //         },
    //         {
    //             breakpoint: 991,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 767,
    //             settings: {
    //                 slidesToShow: 2,
    //             }
    //         },
    //         {
    //             breakpoint: 575,
    //             settings: {
    //                 slidesToShow: 1,
    //             }
    //         }
    //     ]
    // });

    /*------------------------
        Sidebar sticky active
    -------------------------- */
    // $('.sidebar-active').stickySidebar({
    //     topSpacing: 0,
    //     bottomSpacing: 30,
    //     minWidth: 767,
    // });

    /*--- language currency active ----*/
    // $('.mobile-language-active').on('click', function(e) {
    //     e.preventDefault();
    //     $('.lang-dropdown-active').slideToggle(900);
    // });
    // $('.mobile-currency-active').on('click', function(e) {
    //     e.preventDefault();
    //     $('.curr-dropdown-active').slideToggle(900);
    // });


    if (document.getElementById("scroll_to_products")) {
        $([document.documentElement, document.body]).animate({
            scrollTop: $("#scroll_to_products").offset().top
        }, 1000);
    }

    $(".video-first").html(
        "<div class='spinner-border spinner-border' role='status'>\
            <span class='sr-only'>Загрузка...</span>\
        </div>")
    setTimeout(function(e) {
        $(".video-first").html('<iframe src="https://www.youtube.com/embed/sFqMX_tBUCs" title="Компания ISOFIX-MSK"\
         frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"\
          allowfullscreen></iframe>')
    }, 3000)

    $(".video-second").html(
        "<div class='spinner-border spinner-border' role='status'>\
            <span class='sr-only'>Загрузка...</span>\
        </div>")
    setTimeout(function(e) {
        $(".video-second").html('<iframe src="https://www.youtube.com/embed/NtOjU7BhsHA" title="Приспособления для установки\
         нескольких автокресел на заднее сиденье" frameborder="0" allow="accelerometer; autoplay; clipboard-write;\
          encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')
    }, 5000)

    $(function () {
      $('[data-toggle="tooltip"]').tooltip()
    })

    // фильтр
    function buildOptions(param) {
        var htm = "<option></option>\n"
        for (var key in  param) {
            htm += "<option value='" + key + "'>" + key + "</option>\n"
        }
        return htm
    }

    function setFilterOptions() {

    }
    $('#modal_filter').on('shown.bs.modal', function() {
        // $(".bracket").addClass("d-none")

        $("#modal_filter select").off()

        $("#modal_filter select").each(function() {
            $(this).val(false)
        })

        var tokenCSRF = $("body").find("input[name=csrfmiddlewaretoken]")
        var bracket = "кронштейн"
        var rail    = "рейка"
        var service = "услуга"
        var prevOption = "<option value='' selected>загрузка...</option>"
        var content = $("#modal_filter_content")
        var searchFail = '<div class="col-12 h5 text-danger text-center">Данные поиска отсутствуют!</div>'

        $(".models_car").html("")
        $(".years_car").html("")
        $(".seat_types_car").html("")
        content.html("")

        // $("#modal_filter select").on("change", function(e) {
        //     var currentSelectValue = $(this).val()
            
        //     if (currentSelectValue === bracket) {
        //         $(".bracket").removeClass("d-none")
        //         var requestData = {}

        //         requestData[tokenCSRF.attr("name")] = tokenCSRF.val()
        //         requestData["product_type"] = bracket
        //         requestData["all_brands"]   = true

        //         $(".brands_car").html(prevOption)
        //         $.ajax({
        //             url: FILTER_URL,
        //             method: "POST",
        //             data: requestData,
        //             success: function(response) {
        //                 try {
        //                     var brandsCar = JSON.parse(response)
        //                 } catch(err) {
        //                     console.info(err)
        //                     return
        //                 }

        //                 var keys = []
        //                 for (var k in brandsCar){
        //                     keys.push(k)
        //                 }

        //                 var brands = {}
        //                 keys.sort()
        //                 for (var i = 0; i < keys.length; i++) {
        //                     brands[keys[i]] = keys[i]
        //                 }

        //                 var htmlOptionsTags = buildOptions(brands)
        //                 $(".brands_car").html(htmlOptionsTags)
        //             },
        //         })
        //     }

        //     if (currentSelectValue === rail) {
        //         console.log(currentSelectValue)
        //     }

        //     if (currentSelectValue === service) {
        //         console.log(currentSelectValue)
        //     }

        //     // console.log("END currentSelectValue: ", currentSelectValue)
        // })

        $(".brands_car").on("change", function(e) {
            var currentBrand = $(this).val()
            var requestData = {}

            content.html("")

            if (currentBrand === '') {
                $(".models_car").html("")
                $(".years_car").html("")
                $(".seat_types_car").html("")
                return
            }

            requestData[tokenCSRF.attr("name")] = tokenCSRF.val()
            requestData["brand_name"] = currentBrand
            requestData["product_type"] = bracket
            
            $(".models_car").html(prevOption)
            $(".years_car").html(prevOption)
            $(".seat_types_car").html(prevOption)

            $.ajax({
                url: FILTER_URL,
                method: "POST",
                data: requestData,
                success: function(response) {
                    try {
                        var requestData = JSON.parse(response)
                    } catch(err) {
                        console.info(err)
                        return
                    }
                    $(".models_car").html(buildOptions(requestData["model_car"]))
                    $(".years_car").html(buildOptions(requestData["year"]))
                    $(".seat_types_car").html(buildOptions(requestData["seat_type"]))
                },
            })
        })

        $("select.change_bracket").on("change", function(e) {
            var brandCar = $(".brands_car").val()
            var requestData = {}
            $("select.change_bracket").each(function() {
                var currenElem = $(this)
                if (this.value != '') {
                    requestData[currenElem.data("filterName")] = currenElem.val()
                }
            })
            
            if (Object.keys(requestData).length <= 1) { return }

            requestData[tokenCSRF.attr("name")] = tokenCSRF.val()
            content.html(
                "<div class='spinner-border spinner-border m-auto mt-5' role='status'>\
                    <span class='sr-only'>Загрузка...</span>\
                </div>")

            $.ajax({
                url: FILTER_URL,
                method: "POST",
                data: requestData,
                success: function(response) {
                    try {
                        var responseData = JSON.parse(response)
                        if ('length_zero' in responseData) {
                            content.html(searchFail)
                            return
                        }
                    } catch(err) {
                        console.info(err)
                        return
                    }

                    var htm = ""
                    var products = responseData["products"]
                    for (var i = 0; i < products.length; i++) {
                        var product = products[i]
                        htm +=
                            "<div class='col-xl-4 col-lg-4 col-md-6 col-sm-6 col-12'>\
                                <div class='single-product-wrap mb-35'>\
                                    <div class='product-img product-img-zoom mb-15'>\
                                        <a href='" + product["product_url"] + "'>\
                                            <img src='" + product["product_image"] + "'>\
                                        </a>\
                                    </div>\
                                    <div class='product-content-wrap-2 text-center'>\
                                        <h3>" + product["product_name"] + "</h3>\
                                        <div class='product-price-2'>\
                                            <span>" + product["product_price"] + "</span>\
                                        </div>\
                                    </div>\
                                    <div class='product-content-wrap-2 product-content-position text-center'>\
                                        <h3><a href='" + product["product_url"] + "'>" + product["product_name"] + "</a></h3>\
                                        <div class='product-price-2'>\
                                            <span>" + product["product_price"] + "</span>\
                                        </div>\
                                        <div class='pro-add-to-cart'>\
                                            <a class='btn btn-outline-danger rounded' href='" + product["product_url"] + "'>Подробнее</a>\
                                        </div>\
                                    </div>\
                                </div>\
                            </div>"
                    }
                    content.html(htm)
                    if (htm === '') { content.html(searchFail) }
                },
            })
        })

        // -----------------
    })
    $(".clear_all").on("click", function(e) {
        // $(".bracket").addClass("d-none")

        // $(".select_products").html(
        //     '<option></option>\
        //     <option value="кронштейн">Кронштейны</option>\
        //     <option value="рейка">Рейки</option>\
        //     <option value="услуга">Услуги</option>'
        // )

        $(".brands_car").html( $(".brands_car").html() )
        $(".models_car").html("")
        $(".years_car").html("")
        $(".seat_types_car").html("")

        $("#modal_filter_content").html("")
    })
    // end filter

    function setSessionPrapam(URL) {
        $.ajax({
            url: URL,
            method: "GET",
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            success: function(response) {
                console.info(response)
            },
            error: function() { console.error(this.url) },
        });
    }

    // колличество продуктов на странице
    $("#product_list_size").change(function(e) {
        var url = $(this).val()
        setSessionPrapam(url)
        window.location = window.location.pathname
    });
    // сортировка продуктов
    $("#procuct_list_sort").change(function(e) {
        var url = $(this).val()
        setSessionPrapam(url)
        window.location = window.location.pathname
    });
    // отображение в виде таблицы
    $(".grid_style").click(function(e) {
        var url = $(this).data("gridStyleUrl")
        if (!$(this).hasClass("active")) {
            setSessionPrapam(url)
            window.location = window.location.pathname
        }
        return false
    });
    // отображение в виде списка
    $(".list_style").click(function(e) {
        var url = $(this).data("listStyleUrl")
        if (!$(this).hasClass("active")) {
            setSessionPrapam(url)
            window.location = window.location.pathname
        }
        return false
    });

    // модальное окно с карточкой товара

    
    // отключаем повторную инициализацию, карточка товара
    $("#exampleModal").find(".close").click(function(e) {
        $('.quickview-slide-active').slick('unslick');
    })

    // quickview-slide-active nav-style-6 slick-initialized slick-slider
    // обновление данных в модальном окне, текущая карточка товара
    $(".quick_view").on("click", function(e) {
        e.preventDefault()
        
        // глючит слайдер
        if ($(".quickview-slide-active").hasClass("slick-initialized")) {
            $(".quickview-slide-active").removeClass("slick-initialized")
            $(".quickview-slide-active").removeClass("slick-slider")
        }
        var modal = $("#exampleModal");
        var parentElem = $(this)

        var bigIMG =
            "<div id='pro-1' class='tab-pane fade show active'>\
                    <img src='" + parentElem.data("productImageBase") + "'>\
                </div>"

        var smallIMG =
            "<a class='active' data-toggle='tab' href='#pro-1'>\
                    <img src='" + parentElem.data("productImageBase") + "'>\
                </a>"
        // запрос на получение доп изображений
        modal.find(".quickview-big-img").html(bigIMG)
        modal.find(".quickview-slide-active").html(smallIMG)
        $.ajax({
            url: parentElem.data("productAbsoluteUrl"),
            method: "GET",
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            success: function(response) {
                try {
                    var responseData = JSON.parse(response)
                    console.log(responseData)
                } catch (err) {
                    // если ошибка при получении url-лов картинок, вставляем базовое изображение
                    // 
                    // modal.find(".quickview-big-img").html(bigIMG)
                    // modal.find(".quickview-slide-active").html(smallIMG)
                    // console.info("УСТАНОВЛЕНЫ БАЗОВЫЕ ИЗОБРАЖЕНИЕ:", err)
                    return
                }

                var sPro = 2
                for (var i = 0; i < responseData.length; i++) {
                    bigIMG +=
                        "<div id='pro-" + (sPro++) + "' class='tab-pane fade'>\
                        <img src='" + responseData[i] + "'>\
                    </div>"
                }
                

                sPro = 2
                for (var i = 0; i < responseData.length; i++) {
                    smallIMG +=
                        "<a data-toggle='tab' href='#pro-" + (sPro++) + "'>\
                        <img src='" + responseData[i] + "'>\
                    </a>"
                }

                modal.find(".modal_product_name").html("<a style='color:black;' href='" +
                    parentElem.data("productAbsoluteUrl") + "'>" +
                    parentElem.data("productName") + "</a>"
                )
                modal.find(".modal_product_price").html("<span>" + parentElem.data("productPrice") + "</span>")
                modal.find(".modal_product_category").html("<span>Категория: </span><a href='" +
                    parentElem.data("productCategoryUrl") + "'>" +
                    parentElem.data("productCategory") + ",</a>"
                )
                modal.find(".modal_item_num").html("<span>Код товара: </span>" + parentElem.data("productItemNum"))
                var available = parentElem.data("productAvailable")
                if (available === "True") {
                    modal.find(".modal_product_available").html("<span>Наличие: </span> Есть в наличии")
                } else {
                    modal.find(".modal_product_available").html("<span>Наличие: </span> Нет в наличии")
                }
                modal.find(".modal_product_desc_short").text(parentElem.data("productDescriptionShort"))

                modal.find("form").attr("action", parentElem.data("productAddToCartUrl"))

                modal.find(".quickview-big-img").html(bigIMG)
                modal.find(".quickview-slide-active").html(smallIMG)

                $('.quickview-slide-active').not('.slick-initialized').slick({
                    // lazyLoad: 'ondemand',
                    slidesToShow: 3,
                    slidesToScroll: 1,
                    fade: false,
                    loop: true,
                    dots: false,
                    arrows: true,
                    focusOnSelect: true,
                    prevArrow: '<span class="icon-prev"><i class="icon-arrow-left"></i></span>',
                    nextArrow: '<span class="icon-next"><i class="icon-arrow-right"></i></span>',
                    responsive: [{
                            breakpoint: 1199,
                            settings: {
                                slidesToShow: 3,
                            }
                        },
                        {
                            breakpoint: 991,
                            settings: {
                                slidesToShow: 3,
                            }
                        },
                        {
                            breakpoint: 767,
                            settings: {
                                slidesToShow: 3,
                            }
                        },
                        {
                            breakpoint: 575,
                            settings: {
                                slidesToShow: 2,
                            }
                        }
                    ]
                });


                $('#exampleModal').trigger('shown.bs.modal')

                $('.quickview-slide-active a').on('click', function() {
                    $('.quickview-slide-active a').removeClass('active');
                })
            },
            error: function() {
                console.error(this.url)
            },
        });


    });

    // product deatail page
    // Берет value из счетчика колличества товаров input[name=qtybutton]
    // Устанавливает value в скрытом поле input[name=quantity] 
    $(".product_detail").click(function(e) {
        var plusMinusValue = $("input[name=qtybutton]").val()
        $("input[name=quantity]").val(plusMinusValue)
    });
    // cart detail page
    $(".cart-detail-products").each(function(e) {
        var parentElem = $(this)

        // Берет value из текущего счетчика колличества товаров input[name=qtybutton]
        // Устанавливает value в текущем скрытом поле input[name=quantity]
        parentElem.click(function(e) {
            var plusMinusValue = $(this).find("input[name=qtybutton]").val()
            var quantity = $(this).find("input[name=quantity]")
            quantity.val(plusMinusValue)
        });

        // Устанавливает action=URL для  отправки текущей формы
        // В зависимости от нажатой книпки текущей формы delete/update
        parentElem.find("button").click(function(e) {
            var update = $(this).data("updateUrl")
            var remove = $(this).data("deleteUrl")

            var currentForm = parentElem.find("form")

            if (update) {
                currentForm.attr("action", update)
            }

            if (remove) {
                currentForm.attr("action", remove)
            }
        })
        // /cart/detail/
        // 1 установка подитоговой цены всех продуктов
        // 2 Счетчик корзиры + стоимость на странице для ПК 
        // 3 Счетчик на странице для ПЛ
        function changeCartLengthSubTotal(responseData) {
            $("#sub_total").html(
                "Подитог <span>" + responseData.sub_total + "</span>"
            )
            $("#grand_total").html(
                "Итог <span>" + responseData.sub_total + "</span>"
            )
            $(".cart_info").html("<i class='icon-basket-loaded'></i><span class='black'>" + responseData.cart_length + "</span>" + responseData.sub_total)
            $(".cart_middle").html("<i class='icon-basket-loaded'></i><span class='pro-count black'>" + responseData.cart_length + "</span>")
        }

        // Все формы на странице корзины /cart/detail/
        // ОБНОВЛЕНИЕ И УДАЛЕНИЕ ТОВАРОВ
        parentElem.find("form").submit(function(e) {
            e.preventDefault()
            // action="" по умолчанию /cart/add/id/ override=1 устанавливает в зависимости от нажатой кнопки
            // В parentElem.find("button").click(function(e) {}
            parentElem.find("td.product-subtotal").html(
                "<div class='spinner-border spinner-border-sm' role='status'>\
                    <span class='sr-only'>Загрузка...</span>\
                </div>")
            // $("#triffs_list").html('<li><input data-delivery-name="standard" data-delivery-sum="0" type="radio" name="tariff_code" value="standard"> Standard <span>'+CURRENCY+'0.00</span></li>')
            // $("#ser").html('<input maxlength="50" type="text" name="city" id="city" placeholder="Ваш город" required>')
            $.ajax({
                url: $(this).attr("action"),
                method: "POST",
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                data: $(this).serialize(),
                success: function(response) {
                    try {
                        var responseData = JSON.parse(response)
                    } catch (err) {
                        console.info("ОБНОВЛЕНИЕ И УДАЛЕНИЕ ТОВАРОВ, ОШИБКА ПРИ РАЗБОРЕ ПОЛУЧЕННЫХ ДАННЫХ:", err)
                        return
                    }
                    console.info(this.url, "remove||update main cart:", responseData)
                    // product-subtotal
                    if (responseData.result === "update") {

                        parentElem.find("td.product-subtotal").text(responseData.total_price)
                        changeCartLengthSubTotal(responseData)

                    } else if (responseData.result === "remove") {

                        parentElem.addClass("d-none")
                        if (parseInt(responseData.cart_length) === 0) {
                            $("#cart-container").html("<h3 class=\"text-center\">Ваша корзина пуста</h3>\
                                        <div class=\"text-center h6\"><a class='btn btn-danger' href='" + 
                                        PRODUCT_LIST_URL + "'>Перейти к покупкам</a></div>")
                            //window.location = PRODUCT_LIST_URL
                        }

                        changeCartLengthSubTotal(responseData)
                    } else {
                        console.error(this.url, "error update cart")
                    }
                },
                error: function() { console.error(this.url) },
            })
        })
    });

    // Удаление товары из мини корзины
    function removeItemMiniCart() {
        $(".cart-detail-mini-delete").each(function(e) {
            var parent = $(this) // tag LI
            // Все формы в мини корзине
            $(this).find("form").submit(function(e) {
                e.preventDefault()
                $.ajax({
                    url: $(this).attr("action"),
                    method: "POST",
                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                    data: $(this).serialize(),
                    success: function(response) {
                        try {
                            var responseData = JSON.parse(response)
                        } catch (err) {
                            console.info("УДАЛЕНИЕ ТОВАРОВ ИЗ МИНИ КОРЗИНЫ, ОШИБКА ПРИ РАЗБОРЕ ПОЛУЧЕННЫХ ДАННЫХ:", err)
                            return
                        }
                        console.info(this.url, "remove mini cart:", responseData)
                        if (responseData.result === "remove") {
                            parent.addClass("d-none")
                            // счетчики корзины на странице
                            $(".cart_info").html("<i class='icon-basket-loaded'></i><span class='black'>" + responseData.cart_length + "</span>" + responseData.sub_total)
                            $(".cart_middle").html("<i class='icon-basket-loaded'></i><span class='pro-count black'>" + responseData.cart_length + "</span>")
                            // цена товаров в мини корзине
                            $("#cart-mini-sub-total").text(responseData.sub_total)

                            if (parseInt(responseData.cart_length) === 0) {
                                // кнопки в мини корзине
                                $("#enpty_mini_cart").removeClass("d-none")
                                $("#no_enpty_mini_cart").addClass("d-none")
                            }
                        }
                    },
                    error: function() { console.error(this.url) },
                });
            });
        });
    }
    removeItemMiniCart()

    // Все кнопки добавить в корзину добовление товаров в корзину
    $(".product_list_add_to_cart").submit(function(e) {
        e.preventDefault()

        $.ajax({
            url: $(this).attr("action"),
            method: "POST",
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            data: $(this).serialize(),
            success: function(response, status, xhr) {
                try {
                    var responseData = JSON.parse(response)
                } catch (err) {
                    console.info("ДОБАВЛЕНИЕ В КОЗИНУ, ОШИБКА ПРИ РАЗБОРЕ ПОЛУЧЕННЫХ ДАННЫХ:", err)
                    console.log(response)
                    return
                }
                console.info(this.url, "update mini cart:", responseData)
                // если товар успешно добавлен в козину, обновляем 
                if (responseData.result === "update") {
                    // Открытие мини корзины при добавлении товара
                    $(".sidebar-cart-active").addClass("inside")
                    $(".main-wrapper").addClass("overlay-active")

                    if ($("#exampleModal").hasClass("show")) {
                        $(".product_detail_close").click()
                    }
                    
                    // кнопки в мини корзине
                    var elemBTN = $("#no_enpty_mini_cart")
                    if (elemBTN.hasClass("d-none")) {
                        elemBTN.removeClass("d-none")
                        $("#enpty_mini_cart").addClass("d-none")
                    }

                    $("#cart_mini_content").html(
                        "<li class='spinner-border spinner-border-sm text-center' role='status'>\
                        <span class='sr-only'>Загрузка...</span>\
                    </li>")
                    // Запрос на содержимое корзины товаров, /cart/json/
                    $.ajax({
                        url: CART_INFO_JSON_URL,
                        method: "GET",
                        headers: { 'X-Requested-With': 'XMLHttpRequest' },
                        success: function(response) {
                            try {
                                var responseData = JSON.parse(response)
                            } catch (err) {
                                console.info("ПОЛУЧЕНИЕ ДАННЫХ КОРЗИНЫ, ОШИБКА ПРИ РАЗБОРЕ ПОЛУЧЕННЫХ ДАННЫХ:", err)
                                return
                            }
                            console.info(this.url, "get info", responseData)
                            // счетчики корзины на странице
                            $(".cart_info").html("<i class='icon-basket-loaded'></i><span class='black'>" + responseData.cart_length + "</span>" + responseData.sub_total)
                            $(".cart_middle").html("<i class='icon-basket-loaded'></i><span class='pro-count black'>" + responseData.cart_length + "</span>")
                            // цена товаров в мини корзине
                            $("#cart-mini-sub-total").text(responseData.sub_total)

                            var htm = ""
                            
                            for (var k in responseData) {
                                if (k === "sub_total" || k === 'cart_length') { continue }

                                htm += "<li class='single-product-cart cart-detail-mini-delete'>\
                                        <div class='cart-img'>\
                                            <a href='" + responseData[k]["product_url"] + "'>\
                                                <img src='" + responseData[k]["image"] + "'>\
                                            </a>\
                                        </div>\
                                        <div class='cart-title'>\
                                            <h4 class='pb-0 mb-1'><a href='" + responseData[k]["product_url"] + "'>" + responseData[k]["name"] + "</a></h4>\
                                            <span style='font-size: 12px ;'>(" + 
                                            responseData[k]["quantity"] + " × " + 
                                            responseData[k]["price"]    + ") + (" + 
                                            responseData[k]["quantity"] + " × " + 
                                            responseData[k]["price_install"] + ")</span>\
                                        </div>\
                                        <div class='cart-delete'>\
                                            <form action='/cart/remove/" + k + "/' method='post'>\
                                            " + CSRF_TOKEN + "\
                                                <button class='btn btn-link btn-outline-none' type='submit'>×</button>\
                                            </form>\
                                        </div>\
                                        </li>"
                            }
                            $("#cart_mini_content").html(htm)
                            removeItemMiniCart()
                        },
                        error: function() { console.error(this.url) },
                    });
                }
            },
            error: function() { console.error(this.url) },
        });
    });

    $("#add_anchor").change(function() {
        if (this.checked) {
            $.ajax({
                url: $(this).data("url"),
                method: "POST",
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                data: {
                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                    "quantity": 1,
                    "override": 0,
                }
            }).done(function(response) {
                console.log("add_anchor", response)
            }).fail(function(err) {
                console.log("add_anchor", err)
            })
        } else {
            $.ajax({
                url: $(this).data("urlRemove"),
                method: "POST",
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                data: {
                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                }
            }).done(function(response) {
                console.log("add_anchor", response)
            }).fail(function(err) {
                console.log("add_anchor", err)
            })
        }
    });
})(jQuery);
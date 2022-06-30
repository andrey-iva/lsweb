(function($) {
    "use strict";

    function formatPrice(cls) {
        var formatCurrency = $(cls)
        formatCurrency.each(function() {
            var formatSum = new Intl.NumberFormat('ru-RU', {
                style: 'currency', 
                currency: 'RUB' 
            }).format( parseInt($(this).text().trim()) )
            $(this).text(formatSum)
        });
    }
    formatPrice(".format_currency")
    //

    $("#v1").click(function(e) {
        $(this).addClass("d-none")
        $(".v1").removeClass("d-none")
        $(".v1").html('<video controls autoplay width="100%">\
            <source src="/media/video/1.mp4" />\
        </video>')
    });

    $("#v2").click(function(e) {
        $(this).addClass("d-none")
        $(".v2").removeClass("d-none")
        $(".v2").html('<video controls autoplay width="100%">\
            <source src="/media/video/2.mp4" />\
        </video>')
    });

    $("#phone").intlTelInput({
        geoIpLookup: function(success, failure) {
            $.get("https://ipinfo.io", function() {}, "jsonp").always(function(resp) {
              var countryCode = (resp && resp.country) ? resp.country : "us";
              success(countryCode);
              
              if (countryCode === "RU") {
                $('#phone').mask('000 000-00-00')
              }

              // if (countryCode === "BY") {
              //   $('#phone').mask('00 000-00-00')
              // }

              // if (countryCode === "KZ") {
              //   $('#phone').mask('000 000 0000')
              // }

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
            // if (window.location.pathname.match(/^\/product/)) {
            //     window.location = window.location.pathname
            // }  
        });

        $('.body-overlay').on('click', function() {
            container.removeClass('inside');
            wrapper.removeClass('overlay-active');
            // if (window.location.pathname.match(/^\/product\//)) {
            //     window.location = window.location.pathname
            // } 
        });
    };
    miniCart();


    /* NiceSelect */
    $('.nice-select').niceSelect();

    /*------- Color active -----*/
    $('.pro-details-color-content').on('click', 'a', function(e) {
        e.preventDefault();
        $(this).addClass('active').parent().siblings().children('a').removeClass('active');
    });

    /*--------------------------------
        Social icon active
    -----------------------------------*/
    function  SocialIconActive() {
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
    }
    // SocialIconActive()

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


    if (document.getElementById("scroll_to_products")) {
        $([document.documentElement, document.body]).animate({
            scrollTop: $("#scroll_to_products").offset().top
        }, 1000);
    }

    if (document.getElementById("scroll_to_product")) {
        $([document.documentElement, document.body]).animate({
            scrollTop: $("#scroll_to_product").offset().top
        }, 1000);
    }

    if (document.getElementById("scroll_to_cart_title")) {
        $([document.documentElement, document.body]).animate({
            scrollTop: $("#scroll_to_cart_title").offset().top
        }, 1000);
    }

    $(".video-first").html(
        "<div class='spinner-border spinner-border' role='status'>\
            <span class='sr-only'>Загрузка...</span>\
        </div>")
    setTimeout(function(e) {
        $(".video-first").html('<iframe width="560" height="315" src="https://www.youtube.com/embed/sFqMX_tBUCs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')
    }, 3000)

    $(".video-second").html(
        "<div class='spinner-border spinner-border' role='status'>\
            <span class='sr-only'>Загрузка...</span>\
        </div>")
    setTimeout(function(e) {
        $(".video-second").html('<iframe title="Обзор кронштейн-рейки ISOFIX-MSK. Три автокресла на заднем сиденье" width="500" height="281" src="https://www.youtube.com/embed/NtOjU7BhsHA?feature=oembed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen=""></iframe>')
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

    

    $('.quick_view').on('click', function (e) {
        $("script#sh").remove()
        var modal = $("#modal_body_q")
        var quickView = $(this)

        $('#exampleModal').off()
        $("#modal_add_to_cart").off()
        $(".qtybutton").off()

        modal.empty()
        modal.html(
        '<div class="d-flex justify-content-center">\
            <div class="spinner-border" role="status">\
                <span class="sr-only">Loading...</span>\
            </div>\
        </div>')

        $.ajax({
            url: quickView.data("productAbsoluteUrl"),
            method: "GET",
        }).done(function(response) {

            var response = JSON.parse(response)
            var productImages = response["image_urls"]
            var product = response["product"]
            var productLoop = response["product_loop"]

            // console.log(response)

            var bigImages =
            "<div id='pro-1' class='tab-pane fade show active'>\
                    <img src='" + quickView.data("productImageBase") + "'>\
                </div>"

            var smallImages =
                "<a class='active' data-toggle='tab' href='#pro-1'>\
                        <img src='" + quickView.data("productImageBase") + "'>\
                    </a>"

            var sPro = 2
                for (var i = 0; i < productImages.length; i++) {
                    bigImages +=
                    "<div id='pro-" + (sPro++) + "' class='tab-pane fade'>\
                        <img src='" + productImages[i] + "'>\
                    </div>"
                }


                sPro = 2
                for (var i = 0; i < productImages.length; i++) {
                    smallImages +=
                        "<a data-toggle='tab' href='#pro-" + (sPro++) + "'>\
                        <img src='" + productImages[i] + "'>\
                    </a>"
                }

            var intoCart          = quickView.data("intoCart")
            var isLoop            = quickView.data("isLoopInstall")
            var totalPriceInstall = quickView.data("totalPriceInstall")

            var productQuantity = quickView.data("productQuantity")


            function isBracket() {
                if (quickView.data("productType") === "кронштейн") {
                    return true
                } else {
                    return false
                }
                // return (
                //     quickView.data("productType") !== "рейка" && 
                //     quickView.data("productServiceType") !== "услуга" &&
                //     quickView.data("productAttribute") !== "loop"
                // )
            }

            var loopElem = '<div class="h6 font-weight-bold mb-3">Дополнительные услуги:</div>\
            <span class="text-dark">Петля для якорного крепления <b style="color: black;" class="format_curr">'+ quickView.data("productLoopPrice") +'</b>\
            <input id="anchor" class="form-check-input" type="checkbox" name="loop" \
            style="\
                max-width: 120px;\
                margin-left: -7px;\
                zoom: 0.4;\
                cursor: pointer;\
                " '+ (isLoop === "True" ? "checked" : "") +'></span>'
            var loopCheckbox = isBracket() ? loopElem : ""  

            var installElem = 'Установка кронштейна <b style="color: black;" class="format_curr">'+ quickView.data("productPriceInstall") +'</b>\
            <input class="form-check-input" type="checkbox" name="price_install" value="1" \
            style="\
                max-width: 320px;\
                zoom: 0.4;\
                cursor: pointer;"'+ (parseInt(totalPriceInstall) > 0 ? "checked" : "") +'>'
            var installCheckbox = isBracket() ? installElem : ""
            var lst = "<li><span>Тип сиденья: </span>" + quickView.data("productSeatType") + "</li>"+
                    "<li><span>Марка авто: </span> " + quickView.data("productModel") + "</li>"+
                    "<li><span>Год выпуска: </span> " + quickView.data("productYear") + "</li>"
            var bracketList = isBracket() ? lst : ""


            var modalContent = '\
<div class="row">\
    <div class="col-lg-5 col-md-6 col-12 col-sm-12">\
        <div class="tab-content quickview-big-img">\
            '+ bigImages +'\
        </div>\
        <div class="quickview-wrap mt-15">\
            <div class="quickview-slide-active nav-style-6">\
                '+ smallImages +'\
            </div>\
        </div>\
    </div>\
    <div class="col-lg-7 col-md-6 col-12 col-sm-12">\
        <form form action="'+ quickView.data("productAddToCartUrl") +'" method="post" id="modal_add_to_cart" class="product-details-content quickview-content">\
        ' + CSRF_TOKEN + '\
        <input type="text" name="override" value="'+ (intoCart === "yes" ? "1" : "0") +'" hidden>\
        <input id="modal_quantity" type="text" name="quantity" value="1" hidden>\
            <h4 class="font-weight-bold">' + product["name"] + '</h4>\
            <div class="product-ratting-review-wrap">\
            </div>\
            <p>' + product["description"] + '</p>\
            <div class="pro-details-price">\
                <span><b class="format_curr">' + product["price"] + '</b></span>\
            </div>\
            <div>\
                '+ loopCheckbox +'\
            </div>\
            <div class="mb-3 mt-3">\
                <span class="text-dark">'+ installCheckbox +'</span>\
            </div>\
            <div class="product-quantity pro-details-quality">\
                <div class="cart-plus-minus">\
                    <input class="cart-plus-minus-box" type="text" name="qtybutton" value="'+ productQuantity +'" disabled>\
                </div>\
            </div>\
            <div class="product-details-meta mt-1">\
                <ul>\
                    <li><span>Категория:</span> ' + product["category"] + '</li>\
                    <li><span>Код товара: </span> ' + product["code"] + '</li>\
                    '+ bracketList +'\
                    <li><span>Наличие: </span> ' + (product["available"] ? "Есть в наличии" : "Нет в наличии")  + '</li>\
                </ul>\
            </div>\
            <div class="pro-details-action-wrap">\
                <div class="pro-details-add-to-cart">\
                    <button type="submit" class="btn btn-danger btn-lg bg-black p-3 border-0 btn-outline-none">'+ (intoCart === "yes" ? "Обновить товар" : "Добавить в корзину") +'</button>\
                </div>\
                <div class="pro-details-action">\
                    <div class="ya-share2" \
                    data-url="'+ window.location.origin + quickView.data("productAbsoluteUrl") +'"\
                    data-image="'+ window.location.origin + quickView.data("productImageBase") +'"\
                    data-description="'+ product["description"] +'"\
                    data-lang="ru" data-curtain data-use-links data-size="l"\
                    data-color-scheme="blackwhite"\
                    data-limit="0"\
                    data-direction="vertical"\
                    data-popup-direction="top"\
                    data-more-button-type="short"\
                    data-services="vkontakte,odnoklassniki,telegram,viber,whatsapp,moimir,messenger"\
                    ></div>\
                </div>\
            </div>\
        </form>\
    </div>\
</div>'
            modal.html(modalContent)
            $("body").append('<script id="sh" src="https://yastatic.net/share2/share.js"></script>')
            formatPrice(".format_curr")
            // .not('.slick-initialized')
            $('.quickview-slide-active').not('.slick-initialized').slick({
                // lazyLoad: 'ondemand',
                slidesToShow: 3,
                slidesToScroll: 1,

                fade: false,
                loop: true,
                dots: false,
                arrows: true,
                prevArrow: '<span class="icon-prev"><i class="icon-arrow-left"></i></span>',
                nextArrow: '<span class="icon-next"><i class="icon-arrow-right"></i></span>',
                responsive: [
                    {
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

            $('.quickview-slide-active a').on('click', function() {
                $('.quickview-slide-active a').removeClass('active');
            })



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
                quickView.data("productQuantity", newVal)
                $("#modal_quantity").val(newVal)
            });

            $("#modal_add_to_cart").submit(function(e) {
                e.preventDefault()

                var formElem = $(this)
                if (formElem.find("input[name=loop]").prop("checked")) {
                    quickView.data("isLoopInstall", "True")
                } else {
                    quickView.data("isLoopInstall", "False")
                }

                if (formElem.find("input[name=price_install]").prop("checked")) {
                    quickView.data("totalPriceInstall", 1)
                } else {
                    quickView.data("totalPriceInstall", 0)
                }
                $.ajax({
                    url: this.action,
                    method: "POST",
                    data: $(this).serialize(),
                }).done(function(response) {
                    quickView.data("intoCart", "yes")
                    // Открытие мини корзины при добавлении товара
                    $(".sidebar-cart-active").addClass("inside")
                    $(".main-wrapper").addClass("overlay-active")

                    if ($("#exampleModal").hasClass("show")) {
                        $(".modal_quickView_close").click()
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

                    // product петля для якорного крепления
                    // код дублируется
                    if (formElem.find("#anchor").prop("checked")) {
                        $.ajax({
                            url: CART_COUNT_QUANTITY_URL,
                            method: "POST",
                            headers: { 'X-Requested-With': 'XMLHttpRequest' },
                            data: {"csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),}
                        }).done(function(response) {
                            try {
                                // колличество товаров с петлей
                                response = JSON.parse(response)
                                console.log("/cart/count/quantity/on/", response)
                            } catch(err) {
                                console.error("/cart/count/quantity/on/")
                            }
                            var quantity_on = response["quantity_on"]
                            $.ajax({
                                url: "/cart/add/" + quickView.data("productLoopId") + "/",
                                method: "POST",
                                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                                data: {
                                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                                    // "quantity": $("input[name=quantity]").val(),
                                    "quantity": quantity_on,
                                    "override": 1,
                                    // "override": $("input[name=override]").val(),
                                    "price_install": formElem.find("input[name=price_install]").prop("checked") ? 1 : 0
                                }
                            }).done(function(response) {
                                console.log("add_anchor", response)
                                printCart()
                            }).fail(function(err) {
                                console.log("add_anchor", err)
                            });
                        })
                    } else if (formElem.find("#anchor").prop("checked") === false) {
                        // модифицирует сессию, удаляет если 0, производит модификацию + -
                        $.ajax({
                            url: "/cart/remove/loop/" + quickView.data("productLoopId") + "/",
                            method: "POST",
                            headers: { 'X-Requested-With': 'XMLHttpRequest' },
                            data: {
                                "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                                "quantity": $("input[name=quantity]").val(),
                            }
                        }).done(function(response) {
                            console.log('remove: ', this.url, response)
                            // удаляет отметку loop: on
                            $.ajax({
                                url: "/cart/del/sessionkeyloop/" + quickView.data("productId") + "/",
                                method: "POST",
                                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                                data: {
                                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                                }
                            }).done(function(response) {
                                response = JSON.parse(response)
                                console.log("loop off::", response, this.url)
                                printCart()
                            })
                        })
                    } else {
                        printCart()
                    }
                    $('#exampleModal').on('shown.bs.modal', function() {});

                }).fail(function(err) {});
            });

        }).fail(function(err) {
            console.log(err)
        });
    });

    // $("#exampleModal").find(".close").click(function(e) {
    //     $('.quickview-slide-active').slick('unslick');
    // })

    // product deatail page
    $(".product_detail").click(function(e) {
        var plusMinusValue = $("input[name=qtybutton]").val()
        $("input[name=quantity]").val(plusMinusValue)
    });


    // cart detail page
    $(".cart-detail-products").each(function(e) {
        var currentForm = $(this)

        if (currentForm.data("markerLoop") === 'on') {
            // $("body").find("form[data-product-attr=loop]").find("div.dec").off()
            // $("body").find("form[data-product-attr=loop]").find("div.inc").off()
            // $("body").find("form[data-product-attr=loop]").find("button").prop("disabled", true)
        }

        var plusMinusValue = currentForm.find("input[name=qtybutton]").val()
        var quantity = currentForm.find("input[name=quantity]")
        quantity.val(plusMinusValue)
        
        currentForm.find(".cart-plus-minus").click(function(e) {
            plusMinusValue = currentForm.find("input[name=qtybutton]").val()
            quantity = currentForm.find("input[name=quantity]")
            quantity.val(plusMinusValue)
        })

        // Устанавливает action=URL для  отправки текущей формы
        // В зависимости от нажатой книпки текущей формы delete/update
        currentForm.find("button").click(function(e) {
            var update = $(this).data("updateUrl")
            var remove = $(this).data("deleteUrl")
            // var currentForm = currentForm.find("form")
            $(".spiner").removeClass("d-none")
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
        // function changeCartLengthSubTotal(responseData) {
        //     $("#sub_total").html(
        //         "Подитог <span>" + responseData.sub_total + "</span>"
        //     )
        //     $("#grand_total").html(
        //         "Подитог <span>" + responseData.sub_total + "</span>"
        //     )
        //     $(".cart_info").html("<i class='icon-basket-loaded'></i><span class='black'>" + responseData.cart_length + "</span>" + responseData.sub_total)
        //     $(".cart_middle").html("<i class='icon-basket-loaded'></i><span class='pro-count black'>" + responseData.cart_length + "</span>")
        // }

        // Все формы на странице корзины /cart/detail/
        // ОБНОВЛЕНИЕ И УДАЛЕНИЕ ТОВАРОВ
        // action="" по умолчанию /cart/add/id/ override=1 устанавливает в зависимости от нажатой кнопки
        // В currentForm.find("button").click(function(e) {}
        // currentForm.find("span.product-subtotal").html(
        //     "<div class='spinner-border spinner-border-sm' role='status'>\
        //         <span class='sr-only'>Загрузка...</span>\
        //     </div>")
        // currentForm.find("span.product-subtotal-install").html(
        //     "<div class='spinner-border spinner-border-sm' role='status'>\
        //         <span class='sr-only'>Загрузка...</span>\
        //     </div>")
        // $("#triffs_list").html('<li><input data-delivery-name="standard" data-delivery-sum="0" type="radio" name="tariff_code" value="standard"> Standard <span>'+CURRENCY+'0.00</span></li>')
        // $("#ser").html('<input maxlength="50" type="text" name="city" id="city" placeholder="Ваш город" required>')

        // hidden buttons update
        currentForm.find("input.cart_detail_install_bracket").on("change", function(e) {
            currentForm.find("div.cart_detail_install_bracket_spiner").removeClass("d-none")
            currentForm.find("button.btn_update").trigger("click")
            currentForm.find("button.btn_update").trigger("submit")
        });
        currentForm.find("input.cart_detail_install_loop").on("change", function(e) {
            currentForm.find("div.cart_detail_install_loop_spiner").removeClass("d-none")
            currentForm.find("button.btn_update").trigger("click")
            currentForm.find("button.btn_update").trigger("submit")
        });
        currentForm.submit(function(e) {
            e.preventDefault()
            var currentForm = $(this)
            // console.log(currentForm.attr("action"))
            // return
            // console.log(currentForm.find("input[name=quantity]").val())
            // return
            $.ajax({
            url: currentForm.attr("action"),
            method: "POST",
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            data: $(this).serialize(),
            success: function(response) {
                try {
                    var responseData = JSON.parse(response)
                    console.log('>>>>', responseData)
                } catch (err) {
                    console.info("ОБНОВЛЕНИЕ И УДАЛЕНИЕ ТОВАРОВ, ОШИБКА ПРИ РАЗБОРЕ ПОЛУЧЕННЫХ ДАННЫХ:", err)
                    return
                }
                console.info(this.url, "remove||update main cart:", responseData)
                var PRODUCTID = responseData["product_id"]
                // product-subtotal
                if (responseData.result === "update") {
                    // console.log('=======>', responseData)
                    // currentForm.find("span.product-subtotal").text(responseData.total_price)
                    // if (currentForm.find("input[name=price_install]").prop("checked")) {
                    //     currentForm.find("span.item_price_install").text(responseData.price_install)
                    // } else {
                    //     currentForm.find("span.item_price_install").text(CURRENCY + "0")
                    // }
                    // currentForm.find("span.product-subtotal-install").text(responseData.total_price_install)
                    // changeCartLengthSubTotal(responseData)

                    if (typeof(currentForm.find("#add_anchor").prop("checked")) === "undefined") {
                        window.location = window.location.pathname
                    }

                    if (currentForm.find("#add_anchor").prop("checked")) {
                        $.ajax({
                            url: CART_COUNT_QUANTITY_URL,
                            method: "POST",
                            headers: { 'X-Requested-With': 'XMLHttpRequest' },
                            data: {"csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),}
                        }).done(function(response) {
                            try {
                                // колличество товаров с петлей
                                response = JSON.parse(response)
                                console.log("/cart/count/quantity/on/", response)
                            } catch(err) {
                                console.error("/cart/count/quantity/on/")
                            }
                            var quantity_on = response["quantity_on"]


                            $.ajax({
                                url: GET_LOOP_ID_URL,
                            }).done(function(response) {
                                try {
                                    response = JSON.parse(response)
                                    console.info("loop_id:", response["loop_id"])
                                } catch(err) {
                                    console.error("не получил ID:", GET_LOOP_ID_URL)
                                }

                                var loopId = response["loop_id"]

                                $.ajax({
                                    url: "/cart/add/" + loopId + "/",
                                    method: "POST",
                                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                                    data: {
                                        "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                                        // "quantity": $("input[name=quantity]").val(),
                                        "quantity": quantity_on,
                                        "override": 1,
                                        // "override": $("input[name=override]").val(),
                                        // "price_install": $("input[name=price_install]").prop("checked") ? 1 : 0
                                    }
                                }).done(function(response) {
                                    console.log("add_anchor", response)
                                    // printCart()
                                    window.location = window.location.pathname
                                }).fail(function(err) {
                                    console.log("add_anchor", err)
                                });

                            });
         
                        })
                    }

                    if (currentForm.find("#add_anchor").prop("checked") === false) {
                        $.ajax({
                            url: GET_LOOP_ID_URL,
                        }).done(function(response) {
                            try {
                                response = JSON.parse(response)
                                console.info("loop_id:", response["loop_id"])
                            } catch(err) {
                                console.error("не получил ID:", GET_LOOP_ID_URL)
                            }

                            var loopId = response["loop_id"]

                            // модифицирует сессию, удаляет если 0, производит модификацию + -
                            $.ajax({
                                url: "/cart/remove/loop/" + loopId + "/",
                                method: "POST",
                                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                                data: {
                                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                                    "quantity": currentForm.find("input[name=quantity]").val(),
                                }
                            }).done(function(response) {
                                console.log(response)
                                // удаляет отметку loop: on
                                $.ajax({
                                    url: "/cart/del/sessionkeyloop/" + currentForm.data("productId") + "/",
                                    method: "POST",
                                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                                    data: {
                                        "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                                    }
                                }).done(function(response) {
                                    console.log("loop off", response, "del/sessionkeyloop/" + currentForm.data("productId") + "/")
                                    window.location = window.location.pathname
                                })
                            })
                        })
                    }
                    
                } else if (responseData.result === "remove") {
                    // currentForm.addClass("d-none")
                    // currentForm.remove()

                    if (parseInt(responseData.cart_length) === 0) {
                        // $("#cart-container").html("<h3 class=\"text-center\">Ваша корзина пуста</h3>\
                        //             <div class=\"text-center h6\"><a class='btn btn-danger' href='" +
                        //             PRODUCT_LIST_URL + "'>Перейти к покупкам</a></div>")
                        window.location = PRODUCT_LIST_URL
                    } else {
                        
                        $.ajax({
                            url: CART_COUNT_QUANTITY_URL,
                            method: "POST",
                            headers: { 'X-Requested-With': 'XMLHttpRequest' },
                            data: {"csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),}
                        }).done(function(response) {
                            try {
                                // колличество товаров с петлей
                                response = JSON.parse(response)
                                console.log("/cart/count/quantity/on/", response)
                            } catch(err) {
                                console.error("/cart/count/quantity/on/")
                            }
                            
                            var quantity_on = response["quantity_on"]

                            $.ajax({
                                url: GET_LOOP_ID_URL,
                            }).done(function(response) {
                                try {
                                    response = JSON.parse(response)
                                    console.info("loop_id:", response["loop_id"])
                                } catch(err) {
                                    console.error("не получил ID:", GET_LOOP_ID_URL)
                                }

                                var loopId = response["loop_id"]
                                if (parseInt(PRODUCTID) === parseInt(loopId)) {
                                    $.ajax({
                                        url: CART_REMOVE_LOOP_MARKER_URL,
                                        method: "POST",
                                        data: {"csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()}
                                    }).done(function(response) {
                                        console.log(response)
                                        if (response) {
                                            window.location = window.location.pathname
                                        }
                                    })
                                } else {
                                    $.ajax({
                                        url: "/cart/add/" + loopId + "/",
                                        method: "POST",
                                        data: {
                                           "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                                            "quantity": quantity_on,
                                            "override": 1, 
                                        }
                                    }).done(function(response) {
                                        window.location = window.location.pathname
                                    })
                                }
                                
                        })
                     })
                    }

                    // changeCartLengthSubTotal(responseData)
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
            var marker = 0
            if ($(this).find("form").data("productAttr") === "loop") {
                marker += 1
            }

            $(this).find("form").submit(function(e) {
                e.preventDefault()
                var form = $(this)
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

                            if (form.data("productAttr") === "loop") {
                                $.ajax({
                                    url: CART_REMOVE_LOOP_MARKER_URL,
                                    method: "POST",
                                    data: {"csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()}
                                }).done(function(response) {
                                    console.log("mini cart", response)
                                    window.location = window.location.pathname
                                })
                            }
                            window.location = window.location.pathname
                        }
                    },
                    error: function() { console.error(this.url) },
                });
            });
        });
    }
    removeItemMiniCart()

    function printCart() {
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

                function formatP(price) {
                    return new Intl.NumberFormat('ru-RU', {
                        style: 'currency', 
                        currency: 'RUB' 
                    }).format( price )
                }

                $("#cart-mini-sub-total").text( formatP(parseInt(responseData.sub_total.slice(1))) )

                var htm = ""
                var installSum = 0
                for (var k in responseData) {
                    if (k === "sub_total" || k === 'cart_length') { continue }

                    installSum += parseInt(responseData[k]["price_install"].slice(1))

                    var install = ""
                    if (parseInt(responseData[k]["price_install"].slice(1)) > 0) {
                        install = "<div style='font-size: 12px ;'><i class='fa fa-wrench' aria-hidden='true'></i> " +
                                responseData[k]["quantity"] + " × " +
                                formatP(parseInt(responseData[k].price_install.slice(1))) + "</div>"
                    }

                    htm += "<li class='single-product-cart cart-detail-mini-delete'>\
                            <div class='cart-img'>\
                                <a href='" + responseData[k]["product_url"] + "'>\
                                    <img src='" + responseData[k]["image"] + "'>\
                                </a>\
                            </div>\
                            <div class='cart-title'>\
                                <h4 class='pb-0 mb-1'><a href='" + responseData[k]["product_url"] + "'>" + responseData[k]["name"] + "</a></h4>\
                                <div style='font-size: 12px ;'><i class='fa fa-shopping-cart' aria-hidden='true'></i> " +
                                responseData[k]["quantity"] + " × " +
                                formatP(parseInt(responseData[k].price.slice(1))) + "</div>" + install + "\
                            </div>\
                            <div class='cart-delete'>\
                                <form action='/cart/remove/" + k + "/' method='post' data-product-attr='"+ responseData[k]["attribute"] +"'>\
                                " + CSRF_TOKEN + "\
                                    <button class='btn btn-link btn-outline-none' type='submit'>×</button>\
                                </form>\
                            </div>\
                            </li>"
                }
                if (installSum > 0) {

                    $(".cart_info").html("<i class='icon-basket-loaded'></i><img class='is_work mr-2 ml-1' src='/static/shop/images/work.png'><span class='black'>" + responseData.cart_length + "</span>" + responseData.sub_total)
                    $(".cart_middle").html("<i class='icon-basket-loaded'><img height='20' class='is_work mr-0 ml-3' src='/static/shop/images/work.png'></i><span class='pro-count black'>" + responseData.cart_length + "</span>")
                }
                var productDetealForm = $(".product_detail").find("input[name=override]")

                if (parseInt($("form.product_detail").find("input[name=override]").val()) === 0) {
                    $("form.product_detail").find("input[name=override]").val(1)
                    $("form.product_detail").find("button[type=submit]").text("Обновить товар")
                }
                $("#cart_mini_content").html(htm)
                removeItemMiniCart()
            },
            error: function() { console.error(this.url) },
        });
    }

    // Все кнопки добавить в корзину добовление товаров в корзину
    $(".product_list_add_to_cart").submit(function(e) {
        e.preventDefault()
        var formElem = $(this)

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
                    // product петля для якорного крепления
                    if (formElem.find("#add_anchor").prop("checked")) {
                        $.ajax({
                            url: CART_COUNT_QUANTITY_URL,
                            method: "POST",
                            headers: { 'X-Requested-With': 'XMLHttpRequest' },
                            data: {"csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),}
                        }).done(function(response) {
                            try {
                                // колличество товаров с петлей
                                response = JSON.parse(response)
                                console.log("/cart/count/quantity/on/", response)
                            } catch(err) {
                                console.error("/cart/count/quantity/on/")
                            }
                            var quantity_on = response["quantity_on"]
                            $.ajax({
                                url: formElem.find("#add_anchor").data("urlAdd"),
                                method: "POST",
                                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                                data: {
                                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                                    // "quantity": $("input[name=quantity]").val(),
                                    "quantity": quantity_on,
                                    "override": 1,
                                    // "override": $("input[name=override]").val(),
                                    "price_install": $("input[name=price_install]").prop("checked") ? 1 : 0
                                }
                            }).done(function(response) {
                                console.log("add_anchor", response)
                                printCart()
                            }).fail(function(err) {
                                console.log("add_anchor", err)
                            });
                        })
                        
                    } else if (formElem.find("#add_anchor").prop("checked") === false) {
                        var url = formElem.find("#add_anchor").data("urlRemove")
                        // модифицирует сессию, удаляет если 0, производит модификацию + -
                        $.ajax({
                            url: url,
                            method: "POST",
                            headers: { 'X-Requested-With': 'XMLHttpRequest' },
                            data: {
                                "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                                "quantity": $("input[name=quantity]").val(),
                            }
                        }).done(function(response) {
                            console.log('remove: ', url, response)
                            // удаляет отметку loop: on
                            $.ajax({
                                url: formElem.find("#add_anchor").data("urlLoopOff"),
                                method: "POST",
                                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                                data: {
                                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                                }
                            }).done(function(response) {
                                response = JSON.parse(response)
                                console.log("loop off::", response, this.url)
                                printCart()
                            })
                        })
                    } else {
                        printCart()
                    }


                }
            },
            error: function() { console.error(this.url) },
        });
    });

    // product detail
    $(".del-service").change(function(e) {
        var url = $(this).data("url")
        if (this.checked === false) {
            $.ajax({
                url: url,
                method: "POST",
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                data: {
                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                    "quantity": $("input[name=quantity]").val(),
                    "override": $("input[name=override]").val(),
                    "price_install": $("input[name=price_install]").prop("checked") ? 1 : 0
                }
            }).done(function(response) {
                console.log('remove: ', url)
            })
        }
    });
})(jQuery);
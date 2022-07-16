$( function() {
    // д. Дом, кв. Квартира, стр. Строение, к. Корпус
    $("body").change(function(e) {
        var first_name = $("#first_name").val()
        var last_name = $("#last_name").val()
        var phone = $("#phone").val()
        var email = $("#email").val()

        $('.info_list_name').text( first_name && last_name ? last_name + " " + first_name : "" )
        $('.info_list_phone').text( phone ? phone : "" )
        $('.info_list_email').text( email ? email : "" )

        var address = ""
        var street = $("input[name=street]").val()
        address += street ? 'ул ' + street.charAt(0).toUpperCase() + street.slice(1) + ", ": ""

        var building = $("input[name=building]").val()
        address += building ? 'д ' + building + ", ": ""

        var flat = $("input[name=flat]").val()
        address += flat ? 'кв ' + flat + ", ": ""

        var house = $("input[name=house]").val()
        address += house ? 'стр ' + house + ", ": ""

        var block = $("input[name=block]").val()
        address += block ? 'пд ' + block + ", ": ""

        var floor = $("input[name=floor]").val()
        address += floor ? 'эт ' + floor + ", ": ""

        var housing = $("input[name=housing]").val()
        address += housing ? 'корп ' + housing + ", ": ""

        var lIndex = address.lastIndexOf(',')
        if (lIndex !== -1) {
            var replacement = ""
            address = address.substring(0, lIndex) + replacement + address.substring(lIndex + 1);
            $("input[name=address]").val(address)
            
            var arr = ["street", "building", "flat", "house", "block", "floor", "housing"]
            for (var i = 0; i < arr.length; i++) {
               $("input[name="+ arr[i] +"]").prop("required", false) 
            }
        } 
        $(".info_list_address").text(address)
    })

    var token = "17a564feb19fabf1391ab53059b81a6a2012b9a9";
    // $("#map").eq(0).css("all", "initial")
    // 55.645664,37.403028

    var PERCENT = 5

    // удаляет районы города и всё с 65 уровня
    var defaultFormatResult = $.Suggestions.prototype.formatResult;

    function formatResult(value, currentValue, suggestion, options) {
      var newValue = suggestion.data.country+', '+suggestion.data.city;
      suggestion.value = newValue;
      return defaultFormatResult.call(this, newValue, currentValue, suggestion, options);
    }

    function formatSelected(suggestion) {
      return suggestion.data.country+', '+suggestion.data.city;
    }

    function fetchDelivery(kladr_id) {
      var serviceUrl = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/delivery";
      var request = {
        "query": kladr_id
      };
      var params = {
        type: "POST",
        contentType: "application/json",
        headers: {
          "Authorization": "Token " + token
        },
        data: JSON.stringify(request)
      };
        return $.ajax(serviceUrl, params);
    }

    function setDefaultPayment() {
        $(".payment_method_bacs").each(function(e) {
            $(this).addClass("payment-box")
        })
        $(".default_payment").removeClass("payment-box")

        if ($("input[name=tariff]").length > 0) {
            $("input[name=tariff]").each(function() {
                if ($(this).prop("checked")) {
                   addPercent(0, $(this).val())
                }
            });
        }
        $("input[name=payment_method]").each(function() {
            if ($(this).val() === "paynow") {
                $(this).prop("checked", true)
            }
        });
    }

    function serverError(err) {
        $(".tariffs_list").html("<p class='text-danger'>"+ err["statusText"] +"</p>")
    };

    function addDeliveryTax(tax) {
        var csrf = $("input[name=csrfmiddlewaretoken]")

        $.ajax({
            url: CART_ADD_DELIVERY_TAX_URL,
            method: "POST",
            data: {
                "delivery_tax": tax,
                "csrfmiddlewaretoken": csrf.val(),
            },
        }).done(function(response) {
            var response = JSON.parse(response)

            console.log('in to addDeliveryTax: ', response["grand_total"])


            if ("error" in response) {
                console.log(response["error"])
            }
        }).fail(function(err) {
            serverError(err)
        });
    }


    function addPercent(percent, tax) {
        // проценты к итоговой цене при оплате
        $.ajax({
            url: CART_ADD_PERCENT_URL,
            method: "POST",
            data: {
                "percent": percent,
                "delivery_sum": tax, 
                "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
            },
        }).done(function(response) {
            try {
                var response = JSON.parse(response)
                var grandTotal = response["grand_total"]
                // var grandTotal = (parseFloat(response["grand_total"]) + parseFloat(tax)).toFixed(2)

                if (parseInt(grandTotal)) {
                    // $("#order_grand_total").text( (CURRENCY + grandTotal.toString()).replace(".", ",") )
                    var formatSum = new Intl.NumberFormat('ru-RU', {
                        style: 'currency', 
                        currency: 'RUB' 
                    }).format( grandTotal )
                    $("#order_grand_total").text(formatSum)
                }
            } catch(err) {
                console.error("addPercent error")
            }

            // addDeliveryTax(tax)
            // console.log('addPercent: ', response["grand_total"], 'tax: ', tax)

            if ("error" in response) {
                console.log(response["error"])
            }
        }).fail(function(err) {
            serverError(err)
        });
    };

    function resetCheckedPayment() {
        $(".payment_method_bacs").addClass("payment-box")
        $("input[name=payment_method]").each(function(e) {
            this.checked = false
        })
    }

    function printErr(message) {
        // $(".search_city_err_msg").text(message)
        setTimeout(function() {
            // $(".search_city_err_msg").text("")
            $(".tariffs_list").html("<p style='color: black;'>Ничего не найдено!</p>")
        }, 3000)
    };

    function formatCurr(f) {
        return new Intl.NumberFormat('ru-RU', {
            style: 'currency', 
            currency: 'RUB' 
        }).format(f)
    }

    function printTariffs(tariffs, s) {
        if (!tariffs.length) {
            $(".tariffs_list").html("<p style='color: black;'>Ничего не найдено!</p>")
            return
        }
        var tariffs_list = $(".tariffs_list")
        var deliveryPoints = tariffs.pop()
        console.log(tariffs)
        console.log(deliveryPoints)

        var tariffListHTML = ""

        tariffs_loop:
        for (var i = 0; i < tariffs.length; i++) {
            // print tariff list
            if (tariffs[i]["errors"]) {
                console.log(tariffs[i])
                for (var e = 0; e < tariffs[i]["errors"].length; e++) {
                    var err = tariffs[i]["errors"][e]["message"].split(":")
                    err = err[err.length - 1]
                    tariffListHTML += "<li>"+ tariffs[i]["tariff_name"] + ": " + err +"</li>"
                }
                continue
            }

            if ("delivery_sum" in tariffs[i]) {
                var tariffName  = tariffs[i]["tariff_name"]
                var periodMin   = tariffs[i]["period_min"]
                var periodMax   = tariffs[i]["period_max"]
                var calendarMin = tariffs[i]["calendar_min"]
                var calendarMax = tariffs[i]["calendar_max"]
                var deliverySum = tariffs[i]["delivery_sum"]
                var weightCalc  = tariffs[i]["weight_calc"]
                var totalSum    = tariffs[i]["total_sum"]
                var currency    = tariffs[i]["currency"]
                var tariffCode  = tariffs[i]["tariff_code"]

                tariffListHTML += '<li>\
                <input \
                data-tariff-code="' + tariffCode + '"\
                data-delivery-sum="0"\
                data-tariff-name="'+ tariffName +'"\
                type="radio"\
                name="tariff"\
                value="'+ (totalSum ? totalSum : deliverySum) +'"\
                >'+ tariffName +' (до '+ periodMax +' дней) \
                <span>'+ formatCurr( (totalSum ? totalSum : deliverySum) ) +'</span>'

                // tariffListHTML += '<div class="badge badge-danger detail" style="cursor: pointer;">Подробнее</div><div class="d-none">'
                tariffListHTML += '<div class="ml-3" style="font-size: 12px;">-Доставка <span>'+ formatCurr(deliverySum) +'</span></div>'
                
                for (var service of tariffs[i]["services"]) {
                    if (service["code"] === "INSURANCE") {
                        tariffListHTML += '<div class="ml-3" style="font-size: 12px;">-Страховка <span>'+ formatCurr(service["sum"]) +'</span></div>'
                    }
                    if (service["code"].match(/^WASTE_PAPER/)) {
                        tariffListHTML += '<div class="ml-3" style="font-size: 12px;">-Упаковка <span>'+ formatCurr(service["sum"]) +'</span></div>'
                    }
                }
                
                tariffListHTML += '<div class="ml-3 text-danger" style="font-size: 12px;">-Стоимость <span>'+ formatCurr(totalSum) +'</span></div>'
                // tariffListHTML += '</div>'
                tariffListHTML += '</li>'
            }
        }

        if (deliveryPoints.length) {
            $(".tariffs_list").html(tariffListHTML)
            
            var deliveryV = parseInt($("input[name=delivery_name]:checked").val())

            // До адреса клиента
            if (deliveryV === 1) {
                $(".tariffs_list li").each(function(e) {
                   
                    if ($(this).find("input[data-tariff-code='137']").val()) {
                        $(this).find("input[data-tariff-code='137']").prop("checked", true)
                        $("input[name=tariff_code]").val('137')
                        $(".delivery_points_list").remove()
                    } else {
                        $(this).empty()
                    }
                })
            }

            if (deliveryV === 2) {
                $(".tariffs_list li").each(function(e) {
                    if ($(this).find("input[data-tariff-code='136']").val()) {
                        $(this).find("input[data-tariff-code='136']").prop("checked", true)
                        $("input[name=tariff_code]").val('136')
                    } else {
                        $(this).empty()
                    }
                })
            }
            // $(".tariffs_list").find("input[data-tariff-code='136']").prop("checked", true)
            // if ($("select[name=country_point]").val() === "RU") {
            //     $(".tariffs_list").find("input[data-tariff-code='136']").prop("checked", true)
            // } else {
            //     $(".tariffs_list").find("input[data-tariff-code='483']").prop("checked", true)
            // }
            setDefaultPayment()
            // $(".detail").on("click", function(e) {
            //     $(this).next().toggleClass("d-none")
            // })

            $("input[name=tariff]").each(function() {
                if ($(this).prop("checked")) {
                    $("input[name=delivery_sum]").val(this.value)
                    $("input[name=delivery_type]").val($(this).data("tariffName"))
                    // $("input[name=tariff_code]").val($(this).data("tariffCode"))
                }
            });
            $("input[name=tariff]").change(function(e) {
                setDefaultPayment()

            })

            // Пункты выдачи заказов
            var points = []
            var locations = []
            var locationsCodes = {}

            var deliveryPointsHTML =
            '<label for="city">Пункты выдачи заказов <abbr style="color: red;" class="required" title="required">*</abbr></label>'
            + '<input id="search_point" class="mb-2 form-control-sm bg-light outline-none border border-secondary rounded-0"\
             type="text" placeholder="ввести адрес">'
            + '<select id="delivery_points" name="delivery_points" \
            class="form-control form-control-sm bg-light outline-none border border-secondary rounded-0">\
            // <option>выбрать адрес</option>'
            for (var i = 0; i < deliveryPoints.length; i++) {

                locationsCodes[deliveryPoints[i]["location"]["address_full"]] = deliveryPoints[i]["code"]

                deliveryPointsHTML += '<option value="'+ deliveryPoints[i]["code"] +'">'+
                deliveryPoints[i]["location"]["address_full"] +'</option>'

                var latitude = deliveryPoints[i]["location"]["latitude"]
                var longitude = deliveryPoints[i]["location"]["longitude"]

                points.push([latitude, longitude])
                locations.push(deliveryPoints[i]["location"]["address_full"])
            }
            deliveryPointsHTML += "</select>"
            $(".delivery_points_list").removeClass("d-none")
            $(".delivery_points_list").html(deliveryPointsHTML)
            $("select[name=delivery_points]").change(function(e) {
                var pvz_code = $(this).val()
                // var text_option = ''
                // $(".delivery_points_list option").each(function() {
                //     if ($(this).val() === pvz_code) {
                //         text_option += "-" + $(this).text()
                //     }
                // })
                $(".info_list_pvz").text(pvz_code)
            })


            $(".maps").empty();
            $(".maps").append(
                "<div class='delivery-title border-0'>\
                    <h3>Пункты выдачи заказов</h3>\
                    <div id=\"map\"></div>\
                </div>"
            )

            if (points.length > 0) {
                p = {
                    "type": "FeatureCollection",
                    "features": [],
                }

                for (var i = 0; i < deliveryPoints.length; i++) {
                    var latitude = deliveryPoints[i]["location"]["latitude"]
                    var longitude = deliveryPoints[i]["location"]["longitude"]
                    var type = (deliveryPoints[i]["type"] === "PVZ") ? "Пункт выдачи заказов" : "Постамат"
                    var body = "<ul>"
                    body += "<li>Тип пункта: "+ type +"</li>"
                    body += "<li>Адрес: "+ deliveryPoints[i]["location"]["address_full"] +"</li>"

                    if (typeof(deliveryPoints[i]["phones"]) !== "undefined") {
                        for (var idx = 0; idx < deliveryPoints[i]["phones"].length; idx++) {
                            body += "<li>Тел: "+ deliveryPoints[i]["phones"][idx]["number"] +"</li>"
                        }
                    }
                    body += "<li>Время работы: "+ deliveryPoints[i]["work_time"] +"</li>"
                    body += "<li>Дополнительно: "+( typeof(deliveryPoints[i]["address_comment"]) === "undefined" ? "" : deliveryPoints[i]["address_comment"] )+"</li>"
                    body += "</ul>"
                    p["features"].push({
                        "type": "Feature",
                        "id": i,
                        "geometry": {"type": "Point", "coordinates": [latitude, longitude]},
                        "properties": {
                            "hintContent": "<p>"+ deliveryPoints[i]["location"]["address"] +"</p>",
                            "balloonContentHeader": "<h5>Информация</h5><hr>",
                            "balloonContentBody": body,
                            "code": deliveryPoints[i]["code"],
                        },
                    })
                }

                
                ymaps.ready(init);

                function init () {
                    var myMap = new ymaps.Map('map', {
                            center: [s["data"]["geo_lat"], s["data"]["geo_lon"]],
                            zoom: 11
                        }, {
                            searchControlProvider: 'yandex#search'
                        }),

                        objectManager = new ymaps.ObjectManager({
                            // Чтобы метки начали кластеризоваться, выставляем опцию.
                            // clusterize: true,
                            // ObjectManager принимает те же опции, что и кластеризатор.
                            gridSize: 32,
                            clusterDisableClickZoom: true,
                        });

                    // Чтобы задать опции одиночным объектам и кластерам,
                    // обратимся к дочерним коллекциям ObjectManager.
                    objectManager.objects.options.set('preset', 'islands#greenDotIcon');
                    objectManager.clusters.options.set('preset', 'islands#greenClusterIcons');

                    myMap.geoObjects.add(objectManager);

                    objectManager.add(JSON.stringify(p));

                    objectManager.events.add('click', function(e) {
                        var objectId = e.get('objectId'),
                        obj = objectManager.objects.getById(objectId);

                        $("#delivery_points option").each(function() {
                            if (this.value === obj["properties"]["code"]) {
                                this.selected = true
                            }
                        });
                        // console.log(obj)
                    });

                }

                $("#delivery_points").change(function(e) {
                    for (var i = 0; i < deliveryPoints.length; i++) {
                        if (deliveryPoints[i]["code"] === $(this).val()) {
                            $(".maps").empty();
                            $(".maps").append(
                                "<div class='delivery-title border-0'>\
                                    <h3>Пункты выдачи заказов</h3>\
                                    <div id=\"map\"></div>\
                                </div>"
                            )

                            var latitude = deliveryPoints[i]["location"]["latitude"]
                            var longitude = deliveryPoints[i]["location"]["longitude"]

                            ymaps.ready(function() {
                                // Создание карты.
                                var myMap = new ymaps.Map("map", {
                                    center: [latitude, longitude],
                                    zoom: 15
                                });

                                myMap.geoObjects.add(new ymaps.Placemark([latitude, longitude], {
                                    balloonContent: deliveryPoints[i]["location"]["address_full"]
                                }, {
                                    preset: 'islands#redDotIcon',
                                    // iconColor: 'green'
                                }))

                            });

                            break
                        }
                    }
                });
                // ui-menu
                $( "#search_point" ).autocomplete({
                  source: locations,
                  minLength: 2,
                  select: function( event, ui ) {
                    $("#delivery_points").html("<option value='"+ locationsCodes[ui.item.value] +"' selected>" + ui.item.value + "</option>")
                    $("#delivery_points").trigger("change")
                  },
                  open: function( event, ui ) {
                    var w = document.querySelector("#search_point").offsetWidth
                    $(".ui-menu").css({"width": w})
                    $(".ui-menu-item").css({"width": w})
                    $(".ui-menu-item-wrapper").css({"width": w})
                  }
                });
            }

            $("input[name=tariff]").change(function() {
                $("input[name=delivery_sum]").val(this.value)
            });

        } else {
            // $(".tariffs_list").html(tariffListHTML)
            console.log(tariffListHTML)
            $(".tariffs_list").html("<p style='color: black;'>Ничего не найдено!</p>")
        }
    };

    $("#order_create").submit(function(e) {
        // e.preventDefault()

        if ($("input[name=policy]").prop("checked") === false) {
            $(".policy").addClass("border-bottom border-danger")
            return false
        }
        $("input[name=payment_method]").each(function() {
            if (this.checked && this.value === "paynow") {

            }
        })

        var cdek = false
        var cdekV2 = false
        $("input[name=delivery_name]").each(function() {
            if (parseInt($(this).val()) === 2 && $(this).prop("checked")) {
                cdek = true
            }

            if (parseInt($(this).val()) === 1 && $(this).prop("checked")) {
                cdek = true
                cdekV2 = true
            }
        });
        if ( cdek ) {
            // cdek city point
            console.log('>>>??', $("input[name=city]").val())
            var cdekCity = $("input[name=city]")
            if (cdekCity.val() === "") {
                cdekCity.addClass("border border-danger")
                $([document.documentElement, document.body]).animate({
                    scrollTop: $("#ser").offset().top
                }, 1000);
                return false
            }

            // cdek delivery points
            var option = false
            $("select[name=delivery_points] option").each(function() {
                if ($(this).text() !== "выбрать адрес" && $(this).prop("selected")) {
                    option = $(this)
                }
            });

            if (option) {
                // PVZ address
                $("input[name=address]").val(option.text())
            } else {
                // если поле с пунктами выдачи скрыто
                if (!cdekV2) {
                    $("select[name=delivery_points]").addClass("border border-danger")
                    $([document.documentElement, document.body]).animate({
                        scrollTop: $("#ser").offset().top
                    }, 1000);
                    return false
                }
            }
        }

        if ($("select[name=delivery_points]").val()) {
            $("input[name=pvz_code]").val( $("select[name=delivery_points]").val() )
        }

    });



    $("input[name=payment_method]").change(function(e) {
        $(".payment_method_bacs").addClass("payment-box")

        $(this).next().next().removeClass("payment-box")
    });

    // вариации доставки
    $("input[name=delivery_name]").change(function(e) {

        var clientInfo = $("#client_info")
        var deliveryTypeInfoText = $("#delivery_type")
        // hidden input
        var hiddenInputDeliveryType = $("input[name=delivery_type]")

        resetCheckedPayment()
        setDefaultPayment()

        $(".maps").addClass("d-none");
        $("#Place-order").removeClass("d-none")
        $("#payment-method").removeClass("d-none")

        clientInfo.attr("hidden", true)

        $("#country").prop('required', false)
        $("#client_info input").each(function() {
                this.required = false
        });
        $(".field_hidden").each(function() {
            $(this).find("input").prop("required", true)
            this.hidden = false
        })
        $("#additional-info").removeClass("d-none")
        $("#order_create").removeClass("d-none")

        // До адреса клиента
        // if ( parseInt($(this).val()) === 1 ) {
        //     $("#country_point").trigger("change")
        //     $("#country").empty()
        //     clientInfo.attr("hidden", false)
        //     $("#cdek_hidden").prop("hidden", false)

        //     deliveryTypeInfoText.text("До адреса клиента")
        //     hiddenInputDeliveryType.val("До адреса клиента")

        //     $(".maps").removeClass("d-none");

        //     $("#country").prop('required', false)
        //     $("#client_info input").each(function() {
        //         this.required = true
        //     });

        //     $(".field_hidden").each(function() {
        //         $(this).find("input").prop("required", false)
        //         this.hidden = true
        //     })

        //     $(".payment_method_1").addClass('d-none')
        //     $("input[name=payment_method]").change(function(e) {
        //         var val = parseInt(this.value)
        //         if (val === PERCENT) {
        //             addPercent(val, 0)
        //         } else {
        //             addPercent(0, 0)
        //         }
        //     });
        //     if (document.getElementById("order_create")) {
        //         $([document.documentElement, document.body]).animate({
        //             scrollTop: $("#order_create").offset().top
        //         }, 1000);
        //     }
        // }
        // До пункта выдачи СДЭК или До адреса клиента
        $("#cdek_hidden").prop("hidden", true)
        if ( parseInt($(this).val()) === 2 || parseInt($(this).val()) === 1) {
            $("#country_point").trigger("change")
            $("#country").empty()
            clientInfo.attr("hidden", false)
            $("#cdek_hidden").prop("hidden", false)

            if (parseInt($(this).val()) === 2) {
                deliveryTypeInfoText.text("До пункта выдачи СДЭК")
                hiddenInputDeliveryType.val("До пункта выдачи СДЭК")
                $("#delivery_addresses").empty()
            }

            if (parseInt($(this).val()) === 1) {
                deliveryTypeInfoText.text("До адреса клиента")
                hiddenInputDeliveryType.val("До адреса клиента")

                $("#delivery_addresses").removeClass('d-none')
            }

            $(".maps").removeClass("d-none");

            $("#country").prop('required', false)
            $("#client_info input").each(function() {
                this.required = true
            });

            $(".field_hidden").each(function() {
                $(this).find("input").prop("required", false)
                this.hidden = true
            })

            $(".payment_method_1").addClass('d-none')

            $("input[name=payment_method]").change(function(e) {
                var paymentVal = parseInt($(this).val())
                var deliveryTax = parseFloat($("input[name=tariff]:checked").val())
                if (paymentVal === PERCENT) {
                    addPercent(paymentVal, deliveryTax)
                } else {
                    addPercent(0, deliveryTax)
                }
            })

            if (document.getElementById("delivery_poin")) {
                $([document.documentElement, document.body]).animate({
                    scrollTop: $("#delivery_poin").offset().top
                }, 1000);
            }
        }
        // Самовывоз
        $("#shoping_center").addClass("d-none")
        if ( parseInt($(this).val()) === 3 ) {
            $("#country").empty()
            clientInfo.attr("hidden", false)
            $("#shoping_center").removeClass("d-none")
            $("#delivery_addresses").empty()

            deliveryTypeInfoText.text("Самовывоз или установка")
            hiddenInputDeliveryType.val("Самовывоз или установка")

            $("#country").prop('required', false)
            $("#client_info input").each(function() {
                this.required = true
            });

            $(".field_hidden").each(function() {
                $(this).find("input").prop("required", false)
                this.hidden = true
            })
            $(".payment-method-2").addClass("d-none")
            $("input[name=address]").val("г Москва, ул Щорса, д 8, стр 1")
            // grand total
            addPercent(0, 0)

            setTimeout(function() {
                if (document.getElementById("base")) {
                    $([document.documentElement, document.body]).animate({
                        scrollTop: $("#base").offset().top
                    }, 1500);
                }
            }, 500)
        }

        $("input[name=delivery_name]").each(function() {
            if (!this.checked) {
                this.parentElement.hidden = true
            }
        });

        // setDefaultPayment()
    });
    //
    if ( parseInt($("#base").val()) === 3 && $("#base").prop("checked")) {
        // setDefaultPayment()
        var elem = document.querySelector("#base")
        var event = new Event("change");
        elem.dispatchEvent(event);
    }

    // cdek start
    // #city
    $("#city").suggestions({
      token: token,
      type: "ADDRESS",
      hint: false,
      bounds: "city",
      formatResult: formatResult,
      formatSelected: formatSelected,
      // token: token,
      // type: "ADDRESS",
      // hint: false,
      // bounds: "region-settlement",
      onSelect: function(suggestion) {
        resetCheckedPayment()

        $("input[name=address_full_info]").val(JSON.stringify((suggestion)) )
        console.log("START:", suggestion)

        var country = suggestion["data"]["country"] ? suggestion["data"]["country"] : ""
        var unrestricted_value = suggestion["unrestricted_value"] ? suggestion["unrestricted_value"] : ""
        var postal_code = suggestion["data"]["postal_code"] ? suggestion["data"]["postal_code"] : ""

        $(".info_list_country").text(country)
        $(".info_list_region").text(unrestricted_value)
        // $(".info_list_city").text(city_with_type)

        $("input[name=country]").val(country)
        $("input[name=region]").val(unrestricted_value)
        $("input[name=postal_code]").val(postal_code)

        $(".tariffs_list").html(
        '<div class="d-flex justify-content-center">\
            <div class="spinner-border" role="status">\
                <span class="sr-only">Loading...</span>\
            </div>\
        </div>')
        $(".delivery_points_list").addClass("d-none")

        var csrf = $("input[name=csrfmiddlewaretoken]")
        var city = suggestion["data"]["city_with_type"]
        var country_iso_code = suggestion["data"]["country_iso_code"]

        var request = {
            "csrfmiddlewaretoken": csrf.val(),
            'city': city,
            'country_iso_code': country_iso_code,
        }
        if (suggestion.data.kladr_id) {

            var kladr_id = suggestion.data.kladr_id;
            if (kladr_id.length > 13) {
                // план. структура
                kladr_id = kladr_id.substr(0, 11) + "00";

            }
            fetchDelivery(kladr_id)
            .done(function(response) {

                if (response.suggestions.length === 0) {
                    printErr("Данное направление в службе СДЕК отсутствует.")
                    console.log("ONLY RU: ничего не найдено")
                    return
                }

                if (response.suggestions[0].data.cdek_id) {
                    request['cdek_id'] = response.suggestions[0].data.cdek_id
                    console.log("RU:", response.suggestions[0].data.cdek_id)
                    // получаем список тарифов
                    // ветка работает по России
                    // получаем калькуляцию по тарифам
                    $.ajax({
                        url: CDEK_TARIFFLIST_URL,
                        method: "POST",
                        headers: { 'X-Requested-With': 'XMLHttpRequest' },
                        data: request,
                    }).done(function(response) {
                        try {
                            var response = JSON.parse(response)
                            // console.log("ONLY RU CALC RESULT:", response)
                        } catch(err) {
                            console.log(err)
                            return
                        }
                        // получен результат в расчетом
                        printTariffs(response, suggestion)
                    }).fail(function(err) {
                        serverError(err)
                    });

                } else {
                    printErr("Данное направление в службе СДЕК отсутствует.")
                }
            })
            .fail(function() {
                serverError(err)
            });
        } else {

            // пытаемся получить данные о населенном пункте
            // страны RU, BY, KZ - только города, если не найден cdek_id
            $.ajax({
                url: CDEK_CITY_URL,
                method: "POST",
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                data: request,
            })
            .done(function(response) {
                try {
                    var response = JSON.parse(response)
                    if (response.length !== 1) {
                        printErr("Данное направление в службе СДЕК отсутствует.")
                        console.log("ONLY RU BY KZ: Ничего не найдено")
                        return
                    }
                    // console.log("ONLY RU BY KZ", response)
                } catch(err) {
                    console.error(err)
                    return
                }

                var cdek_id = response[0]["code"]
                city = response[0]["city"]
                country_iso_code = response[0]["country_code"]
                console.log("RU BY KZ", city, cdek_id)
                // получаем калькуляцию по тарифам
                $.ajax({
                    url: CDEK_TARIFFLIST_URL,
                    method: "POST",
                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                    data: {
                        "csrfmiddlewaretoken": csrf.val(),
                        "cdek_id": cdek_id,
                        "city": city,
                        "country_iso_code": country_iso_code,
                    },
                })
                .done(function(response) {
                    try {
                        var response = JSON.parse(response)
                        // console.log("ONLY RU BY KZ: CALC RESULT", response)
                    } catch(err) {
                        console.log(err)
                        return
                    }
                    // получен результат в расчетом
                    printTariffs(response, suggestion)
                })
                .fail(function(err) {
                    serverError(err)
                });
            })
            .fail(function(err) {
                serverError(err)
            });
        }
      },
      constraints: {
         locations: [
            { country_iso_code: "RU" },
            { country_iso_code: "BY" },
            { country_iso_code: "KZ" },
         ],
      },
    });
    // cdek end
    // Все что ниже не работает



    // order create start
    // Инициализирует подсказки по ФИО на указанном элементе
    // function init($surname, $name) {
    //   var self = {};
    //   self.$surname = $surname;
    //   self.$name = $name;

    //   var fioParts = ["NAME", "SURNAME"];
    //   $.each([$surname, $name], function(index, $el) {
    //     var sgt = $el.suggestions({
    //       token: "17a564feb19fabf1391ab53059b81a6a2012b9a9",
    //       type: "NAME",
    //       triggerSelectOnSpace: false,
    //       hint: "",
    //       noCache: true,
    //       params: {
    //         // каждому полю --- соответствующая подсказка
    //         parts: [fioParts[index]]
    //       },
    //     });
    //   });
    // };


    // init($("#first_name"), $("#last_name"));

    // // Город, улица, дом, квартира
    // $("#address").suggestions({
    //   token: token,
    //   type: "ADDRESS",
    //   onSelect: function(suggestion) {
    //     $("#postal_code").val(suggestion['data']['postal_code'])
    //     $("input[name=address_full_info]").val(JSON.stringify((suggestion)) )
    //   },
    //   constraints: {
    //      locations: [
    //         { country_iso_code: "RU" },
    //         { country_iso_code: "BY" },
    //         { country_iso_code: "KZ" },
    //      ],
    //   },
    // });

    // $("#region").suggestions({
    //     token: token,
    //     type: "ADDRESS",
    //     onSelect: function(suggestion) {},
    //     constraints: {
    //      locations: [
    //         { country_iso_code: "RU" },
    //         { country_iso_code: "BY" },
    //         { country_iso_code: "KZ" },
    //      ],
    //   },
    // });

    // $("#postal_code").suggestions({
    //     token: token,
    //     type: "postal_unit"
    // });

    // $("#email").suggestions({
    //     token: token,
    //     type: "EMAIL",
    //     onSelect: function(suggestion) {}
    // });
    // order create end
    
    $("#country_point-x").change(function(e) {
        console.log($(this).val())
        $.ajax({
            url: CDEK_CITIES_URL,
            method: "POST",
            data: {
               "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
               "country_iso_code": $(this).val(),
            }
        }).done(function(response) {
            response = JSON.parse(response)
            console.log("length:", response.length)
            
            $( "#city" ).autocomplete({
                source: response,
                minLength: 3,
                delay: 500,
                select: function( event, ui ) {
                    // $(".search_cities").trigger("click")
                },
                open: function( event, ui ) {

                }
            });

            // $("#city").select(function(e) { cdekFN() })
        
        })
    })
    

    function tariffsListSpiner() {
        $(".tariffs_list").html(
        '<div class="d-flex justify-content-center">\
            <div class="spinner-border" role="status">\
                <span class="sr-only">Loading...</span>\
            </div>\
        </div>')
    }

    $(".search_cities-x").click(function(e) {
        cdekFN()
        $("input[name=cdek_city]").val( $("input[name=city]").val() ) 
        $("input[name=cdek_country_iso]").val( $("select[name=country_point]").val() ) 
    })

    function cdekFN() {
        tariffsListSpiner()
        var csrf = $("input[name=csrfmiddlewaretoken]").val()
        console.log($("#city").val().trim().replaceAll(" ", "-"))
        $.ajax({
            url: CDEK_CITY_URL,
            method: "POST",
            data: {
                "csrfmiddlewaretoken": csrf,
                "city": $("#city").val().trim().replaceAll(" ", "-"),
                "country_iso_code": $("select[name=country_point]").val(),
            },
        }).done(function(response) {
            return response
        }).done(function(data) {
            data = JSON.parse(data)
            if (!data.length) {
                printErr("Данное направление в службе СДЕК отсутствует.")
            }

            if (data.length === 1) {
                var info = data[0]
                var address = info.country + ", " + info.region + ", " + info.city
                var countryCode = info.country_code
                var cityCode = info.code

                $.ajax({
                    url: CDEK_TARIFFLIST_URL,
                    method: "POST",
                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                    data: {
                        "csrfmiddlewaretoken": csrf,
                        "cdek_id": cityCode,
                        "country_iso_code": countryCode,
                        "city": info.city,
                        "address": address,
                    },
                }).done(function(response) {
                    response = JSON.parse(response)
                    printTariffs(response, {
                        data: {geo_lat: info.latitude, geo_lon: info.longitude} 
                    })
                })

            } else {
                printErr("Данное направление в службе СДЕК отсутствует.")
            }

            // if (data.length > 1) {
            //     var infoList = {}
            //     var pointsListHTML = "<option>Уточните ваш Н/П</option>"
            //     for (var info of data) {
            //         var subRegion = (typeof info.sub_region !== "undefined") ? ", " + info.sub_region : ""
            //         var address = info.country + ", " + info.region + ", " + info.city + subRegion
            //         var countryCode = info.country_code
            //         var cityCode = info.code

            //         pointsListHTML += "<option value='"+cityCode+"'>"+address+"</option>"

            //         infoList[cityCode] = {
            //             city: info.city,
            //             address: address,
            //             countryCode: countryCode,
            //             cityCode: cityCode,
            //             geo: {geo_lat: info.latitude, geo_lon: info.longitude}
            //         }
            //     }

            //     $(".plist").removeClass("d-none")
            //     $("#points_list").html(pointsListHTML)

            //     $("#points_list").on("change", function(e) {
            //         var code = $(this).val()
            //         $.ajax({
            //             url: CDEK_TARIFFLIST_URL,
            //             method: "POST",
            //             headers: { 'X-Requested-With': 'XMLHttpRequest' },
            //             data: {
            //                 "csrfmiddlewaretoken": csrf,
            //                 "cdek_id": infoList[code].cityCode,
            //                 "country_iso_code": infoList[code].countryCode,
            //                 "city": infoList[code].city,
            //                 "address": infoList[code].address,
            //             },
            //         }).done(function(response) {

            //         })
            //     });
            // }
        })
    }
});

    // $("#country").suggestions({
    //     token: "17a564feb19fabf1391ab53059b81a6a2012b9a9",
    //     type: "country",
    //     onSelect: function(suggestion) {}
    // });
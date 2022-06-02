$( function() {
    var token = "17a564feb19fabf1391ab53059b81a6a2012b9a9";
    // $("#map").eq(0).css("all", "initial")
    // 55.645664,37.403028
    
    var PERCENT = 5

    // if (document.getElementById("delivery_title_scroll")) {
    //     $([document.documentElement, document.body]).animate({
    //         scrollTop: $("#delivery_title_scroll").offset().top
    //     }, 100);
    // }

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
        if ($("input[name=tariff]").length > 0) {
            $("input[name=tariff]").each(function() {
                if (this.checked) {
                   addPercent(0, this.value) 
                }
            });  
        }
        $("input[name=payment_method]").each(function() {
            if (this.value === "paynow") {
                this.checked = true
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

            if ("grand_total" in response) {
                $("#order_grand_total").text(response["grand_total"])
            }

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
                "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
            },
        }).done(function(response) {
            var response = JSON.parse(response)

            if ("grand_total" in response) {
                // $("#order_grand_total").text(response["grand_total"])
                addDeliveryTax(tax)
                console.log(response["grand_total"])
            }

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
    };

    function printErr(message) {
        // $(".search_city_err_msg").text(message)
        setTimeout(function() {
            // $(".search_city_err_msg").text("")
            $(".tariffs_list").html("<p>Ничего не найдено!</p>")
        }, 3000)
    };

    function printTariffs(tariffs, s) {
        if (!tariffs.length) {
            $(".tariffs_list").html("<p>Ничего не найдено</p>")
            return
        }
        var tariffs_list = $(".tariffs_list")
        var deliveryPoints = tariffs.pop()
        console.log(deliveryPoints)

        var tariffListHTML = "<h6 class='mt-0 pt-0 mb-2 text-danger'>Тип доставки</h6>"

        tariffs_loop:
        for (var i = 0; i < tariffs.length; i++) {
            // print tariff list
            if (tariffs[i]["errors"]) {
                console.log(tariffs[i])
                for (var e = 0; e < tariffs[i]["errors"].length; e++) {
                    tariffListHTML += "<li>"+ tariffs[i]["tariff_name"] + ": " + tariffs[i]["errors"][e]["message"] +"</li>"
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
                type="radio"\
                name="tariff"\
                value="'+ (totalSum ? totalSum : deliverySum) +'"\
                >'+ tariffName +' (до '+ periodMax +' дней) \
                <span>'+ CURRENCY + (totalSum ? totalSum : deliverySum) +'</span></li>'
            }
        }

        if (deliveryPoints.length) {
            $(".tariffs_list").html(tariffListHTML)
            $(".tariffs_list").find("input[data-tariff-code='136']").prop("checked", true)
            setDefaultPayment()

            // Пункты выдачи заказов
            var points = []
            var locations = []

            var deliveryPointsHTML = 
            '<label for="city">Пункты выдачи заказов <abbr style="color: red;" class="required" title="required">*</abbr></label>' 
            + '<select id="delivery_points" name="delivery_points" \
            class="form-control form-control-sm bg-light outline-none border border-secondary rounded-0">\
            <option>Выберите пункт</option>'
            for (var i = 0; i < deliveryPoints.length; i++) {
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


            $(".maps").empty();
            $(".maps").append(
                "<div class='delivery-title border-0'>\
                    <h3>Постаматы и Пункты выдачи заказов</h3>\
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
                            zoom: 12
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
                                    <h3>Постаматы и Пункты выдачи заказов</h3>\
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
                                    preset: 'islands#icon',
                                    iconColor: 'green'
                                }))

                            });

                            break
                        }
                    }
                });
            }

        } else {
            $(".tariffs_list").html(tariffListHTML)
            // $(".tariffs_list").html("<p>Пункты выдачи закозов не найдены.</p>")
        }
    };

    $("#order_create").submit(function(e) {
        e.preventDefault()

        $.ajax({
            url: CART_GET_GRAND_TOTAL_URL,
            method: "POST",
            data: {
                "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
            },
        }).done(function(response) {
            response = JSON.parse(response)
            if ("grand_total" in response) {
                console.log(response["grand_total"]["price"])
            }
        }).fail(function(err) {
            console.log(err)
        });
        

        var delivery = 0
        var varrios = {
            "1": "До адреса клиента",
            "2": "Службой доставки СДЭК",
            "3": "Самовывоз",
        };
        $("input[name=delivery_name]").each(function() {
            if (this.checked) {
                delivery = this.value
            }
        });
        var deliveryCity  = $("input[name=city]").val()
        var deliveryPoint = $("select[name=delivery_points]").val()
        if (deliveryPoint) {
            $("input[name=delivery_point]").val(deliveryPoint)
        }

        var firstName = $("input[name=first_name]").val()
        var lastName  = $("input[name=last_name]").val()
        var country   = $("select[name=country]").val()
        var region    = $("input[name=region]").val()
        var address   = $("input[name=address]").val()
        var postalCode= $("input[name=postal_code]").val()
        var phone     = $("input[name=phone]").val()
        var email     = $("input[name=email]").val()
        
        var paymentMethod = 0
        var paymentVarios = {
            "0": "Картой или наличными при самовывозе",
            "5": "Картой или наличными при получении товара (+5%) от стоимости товара",
            "paynow": "Банковской картой при оформлении заказа",
        }
        $("input[name=payment_method]").each(function() {
            if (this.checked) {
                paymentMethod = this.value
            }
        });
        var deliverySum = 0
        $("input[name=tariff]").each(function() {
            if (this.checked) {
                deliverySum = this.value
            }
        });
    });

    $("input[name=payment_method]").change(function(e) {
        var val = parseInt($(this).val())
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

        // del grand tottal session start or reload page
        $.ajax({
            url: DEL_GRAND_TOTAL_SESSION_URL,
            method: "POST",
            data: {
                "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
            },
        }).done(function(response) {
            console.log(response)
        }).fail(function(err) {
            serverError(err)
        });
        
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
        if ( parseInt($(this).val()) === 1 ) {
            clientInfo.attr("hidden", false)

            deliveryTypeInfoText.text("До адреса клиента")
            hiddenInputDeliveryType.val("До адреса клиента")

            $("#country").prop('required',true)
            $("#client_info input").each(function() {
                this.required = true
            });

            $(".payment_method_1").addClass('d-none')
            $("input[name=payment_method]").change(function(e) {
                var val = parseInt(this.value)
                if (val === PERCENT) {
                    addPercent(val, 0)
                } else {
                    addPercent(0, 0)
                }
            });
            setDefaultPayment()            
        }
        // Службой доставки СДЭК
        $("#cdek_hidden").prop("hidden", true)
        if ( parseInt($(this).val()) === 2 ) {
            clientInfo.attr("hidden", false)
            $("#cdek_hidden").prop("hidden", false)

            deliveryTypeInfoText.text("Службой доставки СДЭК")
            hiddenInputDeliveryType.val("Службой доставки СДЭК")

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
                var val = parseInt($(this).val()) 

                $("input[name=tariff]").each(function() {
                    console.log(this.value)
                    if (this.checked) {
                        if (val === PERCENT) {
                            addPercent(val, this.value)                    
                        } else {
                            addPercent(0, this.value)
                        }
                    }
                });
            })
        }
        // Самовывоз
        $("#shoping_center").addClass("d-none")
        if ( parseInt($(this).val()) === 3 ) {
            clientInfo.attr("hidden", false)
            $("#shoping_center").removeClass("d-none")
            
            deliveryTypeInfoText.text("Самовывоз")
            hiddenInputDeliveryType.val("Самовывоз")

            $("#country").prop('required', false)
            $("#client_info input").each(function() {
                this.required = true
            });

            $(".field_hidden").each(function() {
                $(this).find("input").prop("required", false)
                this.hidden = true
            })
            $(".payment-method-2").addClass("d-none")
        }

        $("input[name=delivery_name]").each(function() {
            if (!this.checked) {
                this.parentElement.hidden = true
            }
        });

        setDefaultPayment()
    });

    // cdek start        
    $("#city").suggestions({
      // token: token,
      // type: "ADDRESS",
      // hint: false,
      // bounds: "city",
      // formatResult: formatResult,
      // formatSelected: formatSelected,
      token: token,
      type: "ADDRESS",
      hint: false,
      bounds: "region-settlement",
      onSelect: function(suggestion) {
        resetCheckedPayment()
        console.log("START:", suggestion)
        $(".tariffs_list").html(
        '<div class="d-flex justify-content-center">\
            <div class="spinner-grow" role="status">\
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



    // order create start
    // Инициализирует подсказки по ФИО на указанном элементе
    function init($surname, $name) {
      var self = {};
      self.$surname = $surname;
      self.$name = $name;
      
      var fioParts = ["NAME", "SURNAME"];
      $.each([$surname, $name], function(index, $el) {
        var sgt = $el.suggestions({
          token: "17a564feb19fabf1391ab53059b81a6a2012b9a9",
          type: "NAME",
          triggerSelectOnSpace: false,
          hint: "",
          noCache: true,
          params: {
            // каждому полю --- соответствующая подсказка
            parts: [fioParts[index]]
          },
        });
      });
    };


    init($("#first_name"), $("#last_name"));

    // // Город, улица, дом, квартира
    $("#address").suggestions({
      token: "17a564feb19fabf1391ab53059b81a6a2012b9a9",
      type: "ADDRESS",
      onSelect: function(suggestion) {
        $("#postal_code").val(suggestion['data']['postal_code'])
      },
      constraints: {
         locations: [
            { country_iso_code: "RU" },
            { country_iso_code: "BY" },
            { country_iso_code: "KZ" },
         ],
      },
    });

    // $("#country").suggestions({
    //     token: "17a564feb19fabf1391ab53059b81a6a2012b9a9",
    //     type: "country",
    //     onSelect: function(suggestion) {}
    // });

    $("#region").suggestions({
        token: "17a564feb19fabf1391ab53059b81a6a2012b9a9",
        type: "ADDRESS",
        onSelect: function(suggestion) {},
        constraints: {
         locations: [
            { country_iso_code: "RU" },
            { country_iso_code: "BY" },
            { country_iso_code: "KZ" },
         ],
      },
    });

    $("#postal_code").suggestions({
        token: "17a564feb19fabf1391ab53059b81a6a2012b9a9",
        type: "postal_unit"
    });

    $("#email").suggestions({
        token: "17a564feb19fabf1391ab53059b81a6a2012b9a9",
        type: "EMAIL",
        onSelect: function(suggestion) {}
    });
    // order create end
});
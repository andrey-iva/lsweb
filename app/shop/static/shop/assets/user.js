$(function($) {
	$(".object-tools").append("<li><a href='' class='addlink update_map'>Обновить карту</a></li>")
	var save_btn = $("div.submit-row")
	var csrf = $("input[name=csrfmiddlewaretoken]")

	function make_product_map_xml(e) {
		e.preventDefault()
		$.ajax({
			url: "/make/map/",
			method: "POST",
			data: {
				"csrfmiddlewaretoken": csrf.val(),
			}
		}).done(function(response) {
			alert("Карта товаров обновлена: " + response)
		})
	}

	$(".update_map").on("click", function(e) {
		make_product_map_xml(e)
	});
	
	// $("div a.deletelink").on("click", function(e) {
	// 	make_product_map_xml(e)
	// }); 
	
	// save_btn.find("input[name=_addanother]").on("click", function(e) {
	// 	make_product_map_xml(e)
	// });
	// save_btn.find("input[name=_continue]").on("click", function(e) {
	// 	make_product_map_xml(e)
	// });
	// $("input[name=_save]").on("click", function(e) {
	// 	make_product_map_xml(e)
	// });
})
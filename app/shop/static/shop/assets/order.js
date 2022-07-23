$(function($) {
	$(".field-retail_crm_status").each(function() {
		var field_text = $(this).text()
		if (field_text !== "FAIL" || field_text !== "WAIT PAY") {
			$(this).text("")
			$(this).append(
				"<a href='https://isofix-msk.retailcrm.ru/orders/" + field_text + "/edit' target='_blank'><b>" + field_text + "</b></a>"
			)
		}
	});
})
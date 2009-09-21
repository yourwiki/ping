$(document).ready(function() {
	$("#update_body").focus();
	
	$("#update_form").submit(function() {
		$.ajax({
			type: "POST",
			url: "/ajax/update",
			data: $("#update_form").serialize(),
			dataType: "json",
			complete: function(req, status) {
				console.log("Request complete (" + status + ")");
			},
			success: function(data) {
				console.log("Update posted successfully");
				$("#update_body").val('');
				update_character_count();
				var update = $( data.update );
				update.hide();
				$("#updates").prepend( update );
				update.slideDown();
			}
		});
		
		return false;
	});
	
	$("#update_body").keyup(update_character_count);
});

var update_character_count = function() {
	body_length = $("#update_body").val().length;
	char_left = (140 - body_length);
	
	if( char_left < 10 ) {
		$("#character_count").css('color', '#D40C13');
	} else if( char_left < 20 ) {
		$("#character_count").css('color', '#5C0002');
	} else {
		$("#character_count").css('color', '#000');
	}
	
	$("#character_count").text(char_left);
}

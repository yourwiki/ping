$(document).ready(function() {
	$("#update_body").focus();
	
	$("#update_form").submit(function() {
		$("#character_count").html('<img src="/static/spinner.gif" alt="Posting..." />');
		
		$.ajax({
			type: "POST",
			url: "/ajax/update",
			data: $("#update_form").serialize(),
			dataType: "json",
			complete: function(req, status) {
				console.log("Request complete (" + status + ")");
				update_character_count(); // remove spinner
			},
			success: function(data) {
				console.log("Update posted successfully");
				$("#update_body").val('');
				update_character_count();
				var update = $( data.update );
				update.hide();
				$("#updates").prepend( update );
				update.slideDown();
			},
			error: function() {
				updater.fail();
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
	updater.reset();
}

var updater = {
	default_message: "What are you working on?",
	retry: false,
	
	reset: function() {
		if( this.retry ) {
			$("#update_body").css('background-color', '');
			$("#question").css('color', '');
			$("#question").html( this.default_message );
			this.retry = false;
		}
	},
	
	fail: function(message) {
		if(!message) {
			message = "Can't connect to Ping. <a href=\"#wee\">Try again?</a>";
		}

		$("#update_body").css('background-color', '#DB707F');
		$("#question").css('color', '#5C0002');
		$("#question").html(message);
		
		this.retry = true;
	}
}
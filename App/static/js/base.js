$(document).on({
	ajaxStart: function() {
		$(".modal").fadeIn();
	},
	ajaxStop: function() {
		$(".modal").fadeOut();
	},
});

// globally useful js
$(document).ready(function(){
	$('.dropdown-toggle').dropdown()
});

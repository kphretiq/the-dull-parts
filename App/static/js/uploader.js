function preview(file, url) {
	var preview = $("#preview").empty();
	var file_type = file.type.split("/")[0];
	if (file_type == "image") {
		$("#preview")
			.append(
				$("<img></img>")
				.attr("src", url)
				.attr("alt", "preview of "+file.type)
				);
	} else if (file_type == "video") {
		$("#preview")
			.append(
				$("<div id='vidpreviewwrap'></div>").append(
					$("<video id='vidpreview' controls></video>")
					.append(
						$("<source>")
						.attr("src", url)
						.attr("type", file.type)
						.attr("alt", "preview of "+file.type)
						)
					)
				);
	} else {
		$("#preview")
			.append(
				$("<audio controls></audio>")
				.append(
					$("<source></source>")
					.attr("src", url)
					.attr("type", file.type)
					.attr("alt", "preview of "+file.type)
					)
				);
	}
}

function upload_file(file, signed_request, url) {
	var xhr = new XMLHttpRequest();
	xhr.open("PUT", signed_request);
	xhr.setRequestHeader('x-amz-acl', 'public-read');
	xhr.onload = function() {
		if (xhr.status === 200) {
			$("#input-uri").attr("value", url);
			$("#input-mime-type").attr("value", file.type);
			preview(file, url);
		}
    };

	xhr.onerror = function (err) {
		console.log(err);
		console.log("could not upload");
	};
	xhr.send(file);
}


function get_signed_request(file) {
	var url = "/api/media/request?filepath=" + file.name + "&mimetype=" + file.type;
	console.log(url)
	$.ajax({
		method: "GET",
		url: url
	})
	.success(function(res) {
		console.log(res.signed_request);
		console.log(res.url);
		upload_file(file, res.signed_request, res.url);
	})
	.fail(function(error) {
		console.log(error);
	});
}

$(document).ready(function(){
	$('#input-name').on("change", function () {
		get_signed_request(document.getElementById("input-name").files[0]);
	});
});

var load = function() {
	var redier_img = document.getElementById("redier_img");
	var img = new Image();
	var container = document.getElementById("container");
	img.src = redier_img.src;
	
	container.style.width = img.width + "px";
};
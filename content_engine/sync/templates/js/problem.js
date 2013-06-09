var load = function() {
	var problem_img = document.getElementById("problem_img");
	var img = new Image();
	var container = document.getElementById('container');
	img.src = problem_img.src;

	container.style.width = img.width + "px";
};
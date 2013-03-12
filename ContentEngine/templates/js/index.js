$(document).ready(function(){
	$('#add_hotgames').click(function(){
		window.open('/games/add/', '添加精品游戏推荐');
		return false;
	});
	$('#add_gamerediers').click(function(){
		window.open('/rediers/add/', '添加小兵变大咖');
		return false;
	});
});
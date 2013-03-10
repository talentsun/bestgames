$(document).ready(function(){
	$('#add_hotgames').click(function(){
		window.open('http://cow.bestgames7.com/admin/api/entities/add/', '添加精品游戏推荐');
		return false;
	});
	$('#add_gamerediers').click(function(){
		window.open('http://cow.bestgames7.com/admin/api/gamerediers/add/', '添加小兵变大咖');
		return false;
	});
});
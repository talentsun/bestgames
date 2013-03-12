$(document).ready(function(){
	$('#cancel').click(function(){
		window.close();
		return false;
	});
	$('#save').click(function(){
		$('#add_games_form').submit();
		return false;
	});
});
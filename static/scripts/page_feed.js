$(document).ready(function(){
	$(document).on('click', '.j_feed_reply', function(){
		var cId = $(this).attr('data-comment-id')
			, uName = $(this).attr('data-usrname')
			, sWill = '#-回复给'+ uName + '-# '
			, rootId = $(this).attr('data-root-id');
			
		$('input[name=cId]').val(cId);
		$('input[name=rootId]').val(rootId);
		$('textarea[name=content]').focus().val(sWill);
		return true;
	});
	
	var $bub = $('#J_FeedBub');
	if($bub.html() != 0){
		$bub.show();
	}
});
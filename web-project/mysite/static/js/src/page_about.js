(function(root, $){
	
	var Slider = function(){
		this.init();
	}
	Slider.prototype = {
		init : function(){
			var _ = this;
			_.slider = $('#J_slider');
			_.thumnails = $('#J_thumnails');
			_.current = 0;
			_.running = false;
			_.items = [];
			
			_.thumnails.children('section').each(function(idx){
				var item = $(this);
				_.items.push({
					id : idx,
					h : item.height()
				});
			});
			
			_.slider.children().click(function(){
				_.moveTo($(this).index());
			});
		},
		moveTo : function(position){
			var _ = this;
			
			if(_.running){
				return;
			}
			if(position === _.current){
				return;
			}
			if(position <= -1 || position >= _.items.length){
				return;
			}
			
			if(position >= 0){
				_.current = position;
			}else{
				_.current++;
			}
						
			var t = 0;
			$.each(_.items, function(idx, item){
				if(idx === _.current){
					return false;
				}
	
				t += item.h;
			});
			
			_.running = true;
			_.thumnails.animate({
				top : '-' + t + 'px'
			}, 900, 'easeInOutCirc', function(){
				_.running = false;
				_.turnOnSlider();
			});
		},
		turnOnSlider : function(){
			this.slider.children('li:eq('+ this.current +')').addClass('active').siblings().removeClass('active');
		}
	}
	
	var slider = new Slider();
	
	$(root).bind('mousewheel', function(e){
		if(e.deltaY < 0){
			var i = slider.current + 1;
			slider.moveTo(i);
		}else{
			var i = slider.current - 1;
			slider.moveTo(i);
		}
	});
	
}(window, jQuery));
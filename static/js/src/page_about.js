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
				_.items.push(new SliderItem({
					id : idx,
					obj : item
				}));
			});
			
			_.slider.children().click(function(){
				_.moveTo($(this).index());
			});
			
			$(root).resize(function(){
				_.doAnimation();
			});
			
			_.doAnimation();
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
			
			_.items[_.current].quit.call(_.items[_.current]);
			if(position >= 0){
				_.current = position;
			}else{
				_.current++;
			}
						
			_.doAnimation();
		},
		turnOnSlider : function(){
			this.slider.children('li:eq('+ this.current +')').addClass('active').siblings().removeClass('active');
		},
		doAnimation : function(){
			var _ = this;
			var t = 0;
			$.each(_.items, function(idx, item){
				if(idx === _.current){
					return false;
				}
	
				t += item.obj.height();
			});
			
			_.running = true;
			_.thumnails.animate({
				top : '-' + t + 'px'
			}, 900, 'easeInOutCirc', function(){
				_.running = false;
				_.items[_.current].doAnimation.call(_.items[_.current]);
				_.turnOnSlider();
			});
		}
	}
	
	var SliderItem = function(option){
		this.id = option.id;
		this.h = option.h;
		this.obj = option.obj;
		return this;
	}
	SliderItem.prototype = {
		doAnimation : function(){
			this.obj.children('.inner').addClass('j_enter').removeClass('j_leave');
		},
		quit : function(){
			this.obj.children('.inner').addClass('j_leave').removeClass('j_enter');
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
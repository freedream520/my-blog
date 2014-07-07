/*! lpgray-site 2014-01-02 */
$(function( win ){
  win.gtmap = {};
  win.gtmap.formbiz_config = {
    'atleast' : {
      'exp' : '',
      'tip' : '至少选中一个选项'
    },
    'select':{
      'exp' : '',
      'tip' : '您还没有选择'
    },
    'required' : {
      'exp' : /^\S+$/,
      'tip' : '不能为空'
    },
    'number' : {
      'exp' : /^([+-]?)\d*\.?\d+$/,
      'tip' : '无效数字'
    },
    'chs' : {
      'exp' : /^[\u4e00-\u9fa5]+$/,
      'tip' : '无效中文'
    },
    'eng' : {
      'exp' : /^[a-zA-Z\ \']+$/,
      'tip' : '无效英文'
    },
    'email' : {
      'exp' : /\w+((-w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+/,
      'tip' : '无效英文'
    }
  };
  
  win.gtmap.project_code_template = {
    'jingjiang1' : '(靖)地呈字[##]第##号',
    'nanjing' : '(宁)地供字[##]第##号，第##次'
  }
}(window));
/*
 * @name: jquery 表单验证插件
 * @author: zhangyang
 */
(function($){
  
  var Element = function( elem, ruleIds, options ){
    this.elem = elem;
    this.options = options;
    this.$elem = $(elem);
    this.rules = [];
    this.init( ruleIds );
  };
  Element.prototype = {
    init : function( ruleIds ){
      var self = this;
      var nodeName = self.$elem[0].nodeName;
      
      var ruleIdArray = $.trim(ruleIds).split(',');
      for( var i in ruleIdArray ){
        this.rules.push( this.options.ruleMap[$.trim(ruleIdArray[i])] );
      }
      
      if( nodeName === "INPUT" || nodeName === "TEXTAREA"){
        self.$elem.blur(function(){
          setTimeout(function(){
            self.check();
          }, 200);
        });
        
      } else if( nodeName === "DIV" ){
        self.$elem.find('input[type]').each(function(){
          $(this).mouseup(function(){
            setTimeout(function(){
              self.check();
            }, 200);
          });
        });  
      } else if( nodeName === "SELECT" ) {
        self.$elem.change(function(){
          setTimeout(function(){
            self.check();
          }, 200);
        });
      }
    },
    check : function(){
      var self = this;
      var nodeName = this.$elem[0].nodeName;
      
      if( nodeName === "INPUT" || nodeName === "TEXTAREA"){
        var val = $.trim( this.$elem.val() );
        
        for( var i in this.rules ){
          if( this.rules[i].exp.test( val.replace(/\s/g,'') ) ){
            this.options.onSuccess( this.elem );
          }else{
            this.options.onFailure( this.elem, this.rules[i].tip );
            return false;
          }
        }
        return true;
        
      } else if( nodeName === "DIV" ) {
        if( self.$elem.find(':checked').length ){
          this.options.onSuccess( this.elem );
          return true;
        }
        this.options.onFailure( this.elem, this.rules[0].tip );
        return false;
        
      } else if( nodeName === "SELECT" ){
        if( self.$elem.children(':selected').val() ){
          this.options.onSuccess( this.elem );
          return true;
        }
        this.options.onFailure( this.elem, this.rules[0].tip );
        return false;
      }
    }
  };
  
  var Form = function( elem, options ){
    this.$elem = $(elem);
    this.options = options;
    this.list = [];
    this.init();
  };
  Form.prototype = {
    init : function(){
      var self = this;
      self.$elem.find('[data-validate]').each(function(){
        var rules = $(this).data('validate');
        if( /^\S+$/.test( rules ) ){
          self.list.push( new Element( this, rules, self.options ) );
        }
      });
    },
    validateAll : function(){
      var back = [];
      for( var i in this.list ){
        back.push( this.list[i].check() );
      }
      return $.inArray(false, back) === -1;
    }
  };
  
  $.fn.formvalidate = function( options ){
    return this.each(function(){
      var opts = $.extend(true, $.fn.formvalidate.defaults, options);
      var form = new Form(this, opts);
      $(this).data('form', form);
      $(this).submit(function(){
        return form.validateAll();
      });
    });
  };
  
  $.fn.formvalidate.defaults = {
    onSuccess : function( elem ){
      
    },
    onFailure : function( elem, tip ){
      
    },
    ruleMap : gtmap.formbiz_config
  };
  
}(jQuery));
document.getElementsByClassName || (document.getElementsByClassName = function(searchClass,node,tag){
    node = node || document;
	tag = tag || '*';
	var returnElements = []
	var els =  (tag === "*" && node.all)? node.all : node.getElementsByTagName(tag);
	var i = els.length;
	searchClass = searchClass.replace(/\-/g, "\\-");
	var pattern = new RegExp("(^|\\s)"+searchClass+"(\\s|$)");
	while(--i >= 0){
		if (pattern.test(els[i].className) ) {
			returnElements.push(els[i]);
		}
	}
	return returnElements;
});
(function(root){
	var u = root.Utils = {};
	u.hasFeature = function(str){
	  return document.getElementsByTagName('html')[0].className.indexOf(str) > -1;
	};
	
	u.filterFileName = function(fullPath){
	  if (fullPath) {
	    var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
	    var filename = fullPath.substring(startIndex);
	    if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
	      filename = filename.substring(1);
	    }
	    return filename;
	  }
	};
	
	u.isMobile = function(){
	  return /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent);
	};
	
	u.encodeXML = function(code){
	  return code.replace(/</g,'&lt;').replace(/>/g,'&gt;');
	};
}(window));

(function(root, $){
	// Avoid `console` errors in browsers that lack a console.
	(function() {
	    var method;
	    var noop = function () {};
	    var methods = [
	        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
	        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
	        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
	        'timeStamp', 'trace', 'warn'
	    ];
	    var length = methods.length;
	    var console = (window.console = window.console || {});
	
	    while (length--) {
	        method = methods[length];
	
	        // Only stub undefined methods.
	        if (!console[method]) {
	            console[method] = noop;
	        }
	    }
	}());
	
	// stop default link behavior
	$(document).on('click', '[href="#"],.disabled', function(e) {
	  e.preventDefault();
	});
	
	function pagin(page, size, count, pre) {
	  Array.prototype.contains = function(needle) {
	    for (i in this) {
	      if (this[i] == needle)
	        return true;
	    }
	    return false;
	  }
	  var maxnum = 5, pagin = $('#J_PAGIN'), pagePre = 'page.page', sizePre = 'page.size', prev = pagin.children('.prev'), next = pagin.children('.next'), href = location.href, prefix = '?';
	
	  if (!pre) {
	    if (href.indexOf('?') > -1 && href.indexOf(pagePre) == -1) {
	      prefix = href + '&';
	    } else if (href.indexOf(pagePre) > -1) {
	      prefix = href.substring(0, href.indexOf(pagePre));
	    } else {
	      prefix = '?';
	    }
	  } else {
	    prefix = pre;
	  }
	
	  var total = Math.ceil(count / size);
	
	  if (page == 1) {
	    prev.addClass('disabled');
	  }
	  if (page == total) {
	    next.addClass('disabled');
	  }
	
	  pagin.children('span').children().remove();
	  for ( i = 1; i <= total; i++) {
	    var a = $('<a />').attr({
	      'href' : prefix + pagePre + '=' + i + '&' + sizePre + '=' + size + ''
	    }).html(i);
	    pagin.children('span').append(a);
	    if (i == page) {
	      a.addClass('active');
	      a.attr('href', '#');
	    }
	  }
	
	  prev.attr({
	    'href' : prefix + pagePre + '=' + (page - 1) + '&' + sizePre + '=' + size + ''
	  });
	  next.attr({
	    'href' : prefix + pagePre + '=' + (page + 1) + '&' + sizePre + '=' + size + ''
	  });
	
	  function simplify(page) {
	    var items = pagin.children('span').children('a'), active = pagin.children('span').children('.active'), aIndex, disNum = [], max = 10;
	    if (items.length > max) {
	      // get active index
	      aIndex = active.index() + 1;
	
	      items.each(function(i, link) {
	        if (disNum.length >= max)
	          return false;
	
	        i = i + 1;
	
	        if (i === aIndex || i === aIndex - 1 || i === aIndex + 1 || i === 1 || i === 2 || i === items.length - 1 || i === items.length) {
	          disNum.push(i);
	          return;
	        }
	      })
	      for (var i = aIndex - 2; i > 2; i--) {
	        if (disNum.length >= max)
	          break;
	        disNum.contains(i) || disNum.push(i);
	      }
	
	      for (var i = aIndex + 2; i < items.length - 1; i++) {
	        if (disNum.length >= max)
	          break;
	        disNum.contains(i) || disNum.push(i);
	      }
	
	      disNum.sort(function(a, b) {
	        return a > b;
	      });
	
	      items.each(function(i, link) {
	        i = i + 1;
	        disNum.contains(i) || $(this).remove();
	      });
	
	      items = pagin.children('span').children('a');
	
	      for (var i = 1; i < disNum.length; i++) {
	        if (disNum[i] - disNum[i - 1] > 1) {
	          $(items[i - 1]).after('<strong> ... </strong>');
	        }
	      }
	    }
	  }
	
	  simplify(page);
	  pagin.find('a').addClass('j_pagin_link');
	}
	
	function prettyCode(ctn){
	  ctn && $(ctn).find('.codearea').addClass('prettyprint');
	  root.prettyPrint && prettyPrint();
	}
	
	function bindFormValidate() {
	  var set = {
	    onFailure : function(ui) {
	      $(ui).length && $(ui).removeClass('success').addClass('error');
	    },
	    onSuccess : function(ui) {
	      $(ui).length && $(ui).removeClass('error').addClass('success');
	    }
	  };
	  
	  $.fn.formvalidate.defaults = $.extend({}, $.fn.formvalidate.defaults, set);
	  $('.j_vali_form').formvalidate();
	}
	
	$(document).ready(function(){
	  bindFormValidate();
	});
	
	root.pagin = pagin;
	root.prettyCode = prettyCode;
	
}(window, jQuery));
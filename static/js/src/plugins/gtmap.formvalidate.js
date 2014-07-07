/*
 * @name: gtmap formbiz config
 * @author: zhangyang
 * @datetime: 2013-09-13
 * @description: 表单组件验证及文案配置
 */
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
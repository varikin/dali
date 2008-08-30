var dali = function() {
  var _public = {
    prettify_list : function(selector) {
      var change_list = $(selector);
      var width = _private.get_width(change_list);
      _private.set_width(change_list, width, 20);
    }  
  };

  var _private = {
    
    get_width : function(selector) {
      var width = new Array();
      selector.each(function(i) {
        $(this).children().each(function(j) {
          if(i == 0) {
            width[j] = $(this).width();
          } else if($(this).width() > width[j]) {
            width[j] = $(this).width();
          }
        });
      });
      return width;            
    },
    
    set_width : function(selector, width, offset) {
      selector.each(function(i) {
        $(this).children().each(function(j) {
          $(this).css("padding-right", width[j] - $(this).width() + offset);
        });
      });
    },
    
    update_order : function(selector) {
      return null;
    }
    
  }

  return _public;
}();

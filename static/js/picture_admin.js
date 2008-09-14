var dali = function() {
  var _public = {
    
    order : {},
        
    prettify_list : function(selector) {
      var change_list = $(selector);
      var width = _private.get_width(change_list);
      _private.set_width(change_list, width, 20);
    }, //End prettify_list
    
    update_order : function(e, ui) {
      var galleries = new Object();
      var change_list = $("#sortable_change_list");
      change_list.children().each(function(i) {
        var gallery = $(this).find(".gallery").text();
        var max_order = galleries[gallery];
        if(max_order === undefined) { 
          max_order = 0; 
        }
        galleries[gallery] = ++max_order;
        $(this).find(".order").text(max_order);
        var pk = $(this).find(".name a").attr('href');
        if(pk.charAt(pk.length-1) == '/') {
          pk = pk.substring(0, pk.length-1);
        }
        _public.order[pk] = max_order;
      }); //End change_list each
    } //End update_order
  }; //End _public

  var _private = {
    
    get_width : function(selector) {
      var width = [];
      selector.each(function(i) {
        $(this).children().each(function(j) {
          if(i == 0) {
            width[j] = $(this).width();
          } else if($(this).width() > width[j]) {
            width[j] = $(this).width();
          } //End if
        }); //End children each
      }); //End selector each
      return width;            
    }, //End get_width
    
    set_width : function(selector, width, offset) {
      selector.each(function(i) {
        $(this).children().each(function(j) {
          $(this).css("padding-right", width[j] - $(this).width() + offset);
        }); //End children each
      }); //End selector each
    }, //End set_width
  } //End _private

  return _public;
}();

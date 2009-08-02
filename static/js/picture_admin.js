var gallery = function() {
  var _public = {
    
    update_picture_order : function(table, row) {
      var galleries = {};
      $("#changelist tbody").children().each(function() {
        var gallery = $(this).find("select[id$='gallery']").val();
        var max_order = galleries[gallery];
        if(max_order === undefined) {
          max_order = 0; 
        }
        galleries[gallery] = ++max_order;
        
        $(this).find("input[id$='order']").val(max_order);
        var pk = $(this).find("input[id$='id']").val();
        _private.order[pk] = max_order;
      }); //End change_list each
    }, //End update_picture_order
    
    update_gallery_order : function(table, row) {
      var current = 0;
      $("#changelist tbody").children().each(function() {
        $(this).find("input[id$='order']").val(++current)
        var pk = $(this).find("input[id$='id']").val();
        _private.order[pk] = current;
      }); //End change_list each
    }, //End update_gallery_order
  }; //End _public
  
  var _private = {
    order : {}
  };

  return _public;
}();

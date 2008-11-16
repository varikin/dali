var gallery = function() {
  var _public = {
    update_order : function(table, row) {
      var galleries = {};
      var change_list = $("#changelist tbody");
      change_list.children().each(function(i) {
        var tds = $(this).children();
        var gallery = $(tds.get(2)).text();
        var max_order = galleries[gallery];
        if(max_order === undefined) { 
          max_order = 0; 
        }
        galleries[gallery] = ++max_order;
        $(tds.get(3)).text(max_order);
        var pk = $(tds.get(0)).find('a').attr('href');
        if(pk.charAt(pk.length-1) == '/') {
          pk = pk.substring(0, pk.length-1);
        }
        _private.order[pk] = max_order;
      }); //End change_list each
    }, //End update_order
    
    save_order : function(url) {
      $.post(url, 
        _private.order,
		    function(xml) {
		      $("#footer").text("Order saved!").hide().fadeIn(2000).fadeOut(2000);
		  });
    } //End save_order
  }; //End _public
  
  var _private = {
    order : {}
  };

  return _public;
}();

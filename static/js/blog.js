var dali_blog = function() {
  var _public = {
    update_post : function(value, settings) {
      _private.fields[settings.id] = value;
      return value;
    }, //End update_post
    
    save_post : function(url) {
      $.post(url, _private.fields, _private.save_callback, 'text');
    }, //End save_post
  }; //End _public
  
  var _private = {
    fields : {},
    
    save_callback : function(data) {
      var status = '';
      if(data == "Success") {
        status = 'success'; 
      } else {
        status = 'error'
      }
      
      _private.show_status(data, status);
    }, //End save_callback
    
    show_status : function(message, type) {
      var statusbar = $("<div id='status'></div>")
        .addClass(type)
        .text(message)
        .appendTo(document.body)
        .hide()
        .fadeIn('slow');
      
      setTimeout(function() { 
        statusbar.fadeOut('slow', function() { statusbar.remove(); }); 
      }, 10000);                
    }, // End show_status
  }; //End _private

  return _public;
}();

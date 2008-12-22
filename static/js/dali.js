var dali = function() {
  var _public = {
    update_post : function(value, settings) {
      _private.post_fields[settings.id] = value;
      return value;
    }, //End update_post
    
    save_post : function(url) {
      $.post(url, _private.post_fields, _private.save_callback, 'text');
    }, //End save_post
    
    slide_right : function(div) {
       if(_private.slide_counter > 0) {
          _private.slide_counter--;
          $(div).animate({right: 2 * _private.slide_counter * _private.slide_increment}, 1000);
       }
    }, //End slide_right

    slide_left : function(div) {
       if(_private.slide_counter < 8) {
          _private.slide_counter++;
          $(div).animate({right: 2 * _private.slide_counter * _private.slide_increment}, 1000);
       }
    }, //End slide_left
    
  }; //End _public
  
  var _private = {
    
    slide_increment : 75,
    slide_counter : 0,
    
    post_fields : {},
    
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

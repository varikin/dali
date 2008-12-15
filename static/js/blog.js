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
      _private.show_status(data, 10000);
    }, //End save_callback
    
    show_status : function(message,timeout) {        
      var statusbar = $("<div class='statusbar'></div>")
        .text(message)
        .appendTo(document.body)
        .hide()
        .fadeIn('slow');
      
      if (timeout) {
        setTimeout(function() { 
          statusbar.fadeOut('slow', function() { statusbar.remove(); }); 
        }, timeout);
      }                
    }, // End show_status
  }; //End _private


  function showStatus(message,timeout,add)
  {        
      if (typeof _statusbar == "undefined")
      {
         // ** Create a new statusbar instance as a global object
          _statusbar = 
              $("<div id='_statusbar' class='statusbar'></div>")
                      .appendTo(document.body)                   
                      .show();
      }

      if (add)              
         // *** add before the first item    
          _statusbar.prepend( "<div style='margin-bottom: 2px;' >" + message + "</div>")[0].focus();
      else    
          _statusbar.text(message)
      _statusbar.show();        

      if (timeout)
      {
          _statusbar.addClass("statusbarhighlight");
          setTimeout( function() { _statusbar.removeClass("statusbarhighlight"); },timeout);
      }                
  }

  return _public;
}();

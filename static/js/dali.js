var dali = function() {
  
  var slide_increment = 75;
  var slide_counter = 0;
  var post_fields = {};
  
  var save_callback = function(data) {
    var status = 'success';
    if(data != "Success") {
      status = 'error';
    }
    dali.show_status(data, status);
  };
  
  return {
    
    show_lightbox: function() {
      var ctrl = $('<div id="lightbox_control"></div>')
        .text('close')
        .click(dali.hide_lightbox);
      $("<div id='lightbox'></div>")
        .appendTo(document.body)
        .append(ctrl)
        .hide()
        .fadeIn('slow');
    },
    
    hide_lightbox : function() {
      $("#lightbox").fadeOut('slow', function(){
        $(this).remove();
      });
    },
    
    update_post : function(value, settings) {
      post_fields[settings.id] = value;
      return value;
    },
    
    save_post : function(url) {
      if(dali.object_size(post_fields) > 0) {
        $.post(url, post_fields, save_callback, 'text');
        post_fields = {};
      } else {
        dali.show_status('Nothing to save', 'info');
      }
    },
    
    slide_right : function(div) {
       if(slide_counter > 0) {
          slide_counter--;
          $(div).animate({right: 2 * slide_counter * slide_increment}, 1000);
       }
    },

    slide_left : function(div) {
       if(slide_counter < 8) {
          slide_counter++;
          $(div).animate({right: 2 * slide_counter * slide_increment}, 1000);
       }
    },
    
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
    },
        
    object_size : function(obj) {
      var count = 0;
      for(var p in obj) {
        if(obj.hasOwnProperty(p)) {
          count++;
        }
      }
      return count;
    }
  };
}();

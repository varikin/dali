var dali = function() {
  
  var slide_increment = 85;
  var slide_counter = 0;
  var post_fields = {};
  var lightbox_url = "/gallery/choose_picture/";
  
  var save_callback = function(data) {
    var status = 'success';
    if(data != "Success") {
      status = 'error';
    }
    dali.show_status(data, status);
  };
  
  return {
    
    update_post : function(value, settings) {
      post_fields[settings.id] = value;
      return value;
    },
    
    toggle_publish : function(event) {
      if(event.target.alt != 'Published') {
        event.target.alt = 'Published';
        event.target.title = 'Published';
        event.target.src = '/static/icons/accept.png';
        dali.update_post('True', { id: 'published' });
      } else {
        event.target.alt = 'Not Published';
        event.target.title = 'Not Published';
        event.target.src = '/static/icons/exclamation.png';
        dali.update_post('False', { id: 'published' });
      }
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

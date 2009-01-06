var dali = function() {
  
  var slide_increment = 75;
  var slide_counter = 0;
  var post_fields = {};
  var lightbox_url = "/gallery/choose_picture/";
  var lightbox_status = "";
  
  var save_callback = function(data) {
    var status = 'success';
    if(data != "Success") {
      status = 'error';
    }
    dali.show_status(data, status);
  };
  
  return {
    
    show_lightbox: function() {
      $("<div id='lightbox'></div>")
        .appendTo(document.body)
        .hide()
        .fadeIn('slow')
        .load(lightbox_url, {}, function() {
          $("#lb_control").click(dali.hide_lightbox);   
          $("#lb_galleries").click(dali.select_lightbox_gallery);
        });
    },
      
    select_lightbox_gallery : function(event) {
      var url = lightbox_url + $(event.target).attr('id') + "/";
      $("#lightbox")
        .empty()
        .load(url, {}, function() {
          $("#lb_control").click(dali.hide_lightbox);
          $("#lb_pictures > img").hover(
            function (event) {
              $("#lb_status").text($(event.target).attr('title'));
            },
            function () {
              $("#lb_status").text(lightbox_status);
            }
          );
          $("#lb_pictures > img").click(function (event) {
            $('#lb_pictures > .selected').removeClass('selected');
            var target = $(event.target);
            lightbox_status = target.attr('title');
            target.addClass('selected');
            
          });
        });
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

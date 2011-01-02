var dali = function() {
  
  var slide_increment = 85;
  var slide_counter = 0;
  return {
    
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
    }
  };
}();

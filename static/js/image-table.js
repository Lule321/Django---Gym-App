$(document).ready(function() {
  $("<td></td>").append(
                    $("<div>").attr("class","overlay")
                                .text("Overlay")
                                .css({
                                    "width" : "100%",
                                    "height" : "250%",
                                    "background-color": "rgba(0,0,0,0.5)",
                                    "z-index": "2",
                                }).hide()
                );

  $(".slika").on({
      mouseenter : function() {
          $($(this).parent()).parent().filter(".overlay").show();
      },

      mouseleave : function (){
        $($(this).parent()).parent().filter(".overlay").hide();
      }
  });

});
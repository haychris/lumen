//Constants
var oneRating = "Hate";
var twoRating = "Dislike";
var threeRating = "Neutral";
var fourRating = "Like";
var fiveRating = "Amazing";

// Initial slider rendering function
$(function() {
  $( ".slider" ).each(function() {
    $(this).slider({
      range: "min",
      value: 3,
      min: 1,
      max: 5,
      step: 1,
      slide: function( event, ui ) {
        if (ui.value == 1)
          $(this).parent().next().text(oneRating);
        else if (ui.value == 2)
          $(this).parent().next().text(twoRating);
        else if (ui.value == 3)
          $(this).parent().next().text(threeRating);
        else if (ui.value == 4)
          $(this).parent().next().text(fourRating);
        else if (ui.value == 5)
          $(this).parent().next().text(fiveRating);
        else
          $(this).parent().next().text("ERROR");
      }
    });
  });
});

// Slider rendering function for courses later added
/*function showSlider(id) {
console.log("showSlider called on " + id);

  $(function() {
    $( "#"+id+"S" ).slider({
      range: "min",
      value: 3,
      min: 1,
      max: 5,
      step: 1,
      slide: function( event, ui ) {
        if (ui.value == 1)
          $( "#"+id ).parent().next().text(oneRating);
        else if (ui.value == 2)
          $( "#"+id ).parent().next().text(twoRating);
        else if (ui.value == 3)
          $( "#"+id ).parent().next().text(threeRating);
        else if (ui.value == 4)
          $( "#"+id ).parent().next().text(fourRating);
        else if (ui.value == 5)
          $( "#"+id ).parent().next().text(fiveRating);
        else
          $( "#"+id ).parent().next().text("ERROR");
      }
    });
  });
}*/

function updateSlider(id, rating) {
  var sliderID = '#' + id + "S";
  console.log("HERE");
  $(function() {
    ratingSlider = $(sliderID).slider();
    ratingSlider.slider('option', 'value', rating);
    ratingSlider.slider('option','slide')
       .call(ratingSlider,null,{ handle: $('.slider', ratingSlider), value: rating });

  });
}
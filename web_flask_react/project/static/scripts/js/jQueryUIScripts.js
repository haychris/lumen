function showSlider() {
  $( ".slider" ).slider({
    range: "min",
    value: 3,
    min: 1,
    max: 5,
    step: 1,
    slide: function( event, ui ) {
      $( "#amount" ).val( "$" + ui.value );
    }
  });
  $( "#amount" ).val( "$" + $( ".slider" ).slider( "value" ) );
}
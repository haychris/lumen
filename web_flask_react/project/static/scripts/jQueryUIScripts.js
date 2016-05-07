var oneRating = "Hate";
var twoRating = "Dislike";
var threeRating = "OK";
var fourRating = "Like";
var fiveRating = "Amazing";

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

function showSlider(id) {
  $(function() {
    $( "#"+id ).slider({
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
}

function saveToCookie() {
  allCourseNames = document.getElementsByTagName('input');
  allCourseRatings = document.getElementsByClassName('showRating');
  if (allCourseNames.length != allCourseRatings.length)
    console.log("ERROR: Number of courses not equal to number of ratings");

  var d = new Date();
  d.setTime(d.getTime() + (30*24*60*60*1000));
  var expiration = "expires=" + d.toUTCString();

  var courseCount = allCourseNames.length;
  var cookieContent = "";

  for (var i = 0; i < courseCount; i++) {
    courseName = allCourseNames[i].value;
    courseRating = ratingTextToNum(allCourseRatings[i].innerHTML);

    if (courseName != "") {
      cookieContent = cookieContent + "n" + i + "=" + courseName + "; " + "r" + i + "=" + courseRating + "; ";
    }
  }
  console.log(cookieContent);
  document.cookie = cookieContent + expiration;
  getCookie();
}

function ratingTextToNum(text) {
  if (text == oneRating)
    return 1;
  else if (text == twoRating)
    return 2;
  else if (text == threeRating)
    return 3;
  else if (text == fourRating)
    return 4;
  else if (text == fiveRating)
    return 5;
  else
    return -1;
}

function getCookie() {
  var cookieData = document.cookie.split(";");

  for (var i = 0; i < cookieData.length; i++) {
    console.log(cookieData[i]);
  }
}
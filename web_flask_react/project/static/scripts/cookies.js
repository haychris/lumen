//Constants
var oneRating = "Hate";
var twoRating = "Dislike";
var threeRating = "OK";
var fourRating = "Like";
var fiveRating = "Amazing";

// Saves all course names and corresponding ratings to a cookie with 30d expiry
function saveToCookie() {
  allCourseNames = document.getElementsByTagName('input');
  allCourseRatings = document.getElementsByClassName('showRating');

  var d = new Date();
  d.setTime(d.getTime() + (30*24*60*60*1000));

  var courseCount = allCourseNames.length;
  var cookieContent = "";

  for (var i = 0; i < courseCount; i++) {
    var courseName = allCourseNames[i].value;
    var courseRating = ratingTextToNum(allCourseRatings[i].innerHTML);

    if (courseName != "")
      cookieContent = cookieContent + allCourseNames[i].id + ":" + courseName + "," + "r:" + courseRating + "|";

  }
  cookieContent = cookieContent.substring(0, cookieContent.length-1);

  document.cookie = "CourseInfo=" + cookieContent+ "; expires=" + d.toUTCString();
  console.log("Cookie set:" + hasCookie());
}

// Converts between text and numerical ratings
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

function hasCookie() {
  if (document.cookie.split("=")[0] != "CourseInfo") {
    return false;
  }

  else
    return true;
}
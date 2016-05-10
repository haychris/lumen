function registrarRedirect(courseID, termID) {
	var url = "https://registrar.princeton.edu/course-offerings/course_details.xml?courseid=" + courseID + "&term=" + termID;
	window.open(url, "_blank");
}
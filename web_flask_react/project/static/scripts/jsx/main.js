/***********************************************
 * Adds a semester div to courseHistInput.html *
 * Disables itself after being clicked twice   *
 ***********************************************/
var AddSemester = React.createClass({
  getInitialState: function() {
    return{clickCount: 0};
  },
  appendSemester: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });

    if (this.state.clickCount == 0)
      document.getElementById('sophomoreYear').setAttribute("style", "");
    else if (this.state.clickCount == 1)
      document.getElementById('juniorYear').setAttribute("style", "");

    else return;
  },
  render: function() {
    if (this.state.clickCount > 1)
      return null;
    return (
      <div id="addSemesterButton" onClick={this.appendSemester}>ADD SEMESTER</div>
    );
  }
});

/*****************************************************************************
Returns a courseEntry div equivalent to:

  <div class="courseEntry">
    <div class="courseName">
        <input id="FF1N" class="courseName" type="text" placeholder="Course {{number}}"/>
    </div>

    <div class="courseRating">
      <div id="FF1S" class="slider"></div>
    </div>
    
    <div id="FF1R" class="showRating">OK</div>
  </div>
 *****************************************************************************/
function genCourseEntry(semester, count) {
  var entry = document.createElement("div");
  entry.setAttribute("class", "courseEntry");
  var courseName = entry.appendChild(document.createElement("div"));
  var courseRating = entry.appendChild(document.createElement("div"));
  var showRating = entry.appendChild(document.createElement("div"));

  courseName.setAttribute("class", "courseName");
  var inputField = courseName.appendChild(document.createElement("input"));
  inputField.setAttribute("class", "courseName");
  inputField.type = "text";
  inputField.placeholder = "Course " + count;
  inputField.id = semester + count + "N";

  courseRating.setAttribute("class", "courseRating");
  var slider = courseRating.appendChild(document.createElement("div"));
  slider.setAttribute("class", "slider");
  slider.id = semester + count + "S";

  showRating.id = semester + count + "R";
  showRating.setAttribute("class", "showRating");
  showRating.innerHTML = "OK";
  return entry;
}

/***************************************************************************
 * Adds a course entry field with ratings slider to FRESHMAN FALL semester *
 * Button disabled after there are 7 courses                               *
 ***************************************************************************/
var AddCourseFF = React.createClass({
  getInitialState: function() {
    return{clickCount: 5};
  },
  appendCourse: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });
    var entry = genCourseEntry("FF", this.state.clickCount);
    document.getElementById('appendFF').appendChild(entry);
    showSlider("FF"+this.state.clickCount+"S");
  },
  render: function () {
    if (this.state.clickCount > 7) {
      document.getElementById('FFAddButton').removeAttribute("class");
      return null;
    }
    else return (
      <div onClick={this.appendCourse}>ADD BUTTON</div>
    );
  }
});

/*****************************************************************************
 * Adds a course entry field with ratings slider to FRESHMAN SPRING semester *
 * Button disabled after there are 7 courses                                 *
 *****************************************************************************/
var AddCourseFS = React.createClass({
  getInitialState: function() {
    return{clickCount: 5};
  },
  appendCourse: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });
    var entry = genCourseEntry("FS", this.state.clickCount);
    document.getElementById('appendFS').appendChild(entry);
    showSlider();
  },
  render: function () {
    if (this.state.clickCount > 7) {
      document.getElementById('FSAddButton').removeAttribute("class");
      return null;
    }
    else return (
      <div onClick={this.appendCourse}>ADD BUTTON</div>
    );
  }
});

/****************************************************************************
 * Adds a course entry field with ratings slider to SOPHOMORE FALL semester *
 * Button disabled after there are 7 courses                                *
 ****************************************************************************/
var AddCourseSF = React.createClass({
  getInitialState: function() {
    return{clickCount: 5};
  },
  appendCourse: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });
    var entry = genCourseEntry("SF", this.state.clickCount);
    document.getElementById('appendSF').appendChild(entry);
    showSlider();
  },
  render: function () {
    if (this.state.clickCount > 7) {
      document.getElementById('SFAddButton').removeAttribute("class");
      return null;
    }
    else return (
      <div onClick={this.appendCourse}>ADD BUTTON</div>
    );
  }
});

/******************************************************************************
 * Adds a course entry field with ratings slider to SOPHOMORE SPRING semester *
 * Button disabled after there are 7 courses                                  *
 ******************************************************************************/
var AddCourseSS = React.createClass({
  getInitialState: function() {
    return{clickCount: 5};
  },
  appendCourse: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });
    var entry = genCourseEntry("SS", this.state.clickCount);
    document.getElementById('appendSS').appendChild(entry);
    showSlider();
  },
  render: function () {
    if (this.state.clickCount > 7) {
      document.getElementById('SSAddButton').removeAttribute("class");
      return null;
    }
    else return (
      <div onClick={this.appendCourse}>ADD BUTTON</div>
    );
  }
});

/**************************************************************************
 * Adds a course entry field with ratings slider to  JUNIOR FALL semester *
 * Button disabled after there are 7 courses                              *
 **************************************************************************/
var AddCourseJF = React.createClass({
  getInitialState: function() {
    return{clickCount: 5};
  },
  appendCourse: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });
    var entry = genCourseEntry("JF", this.state.clickCount);
    document.getElementById('appendJF').appendChild(entry);
    showSlider();
  },
  render: function () {
    if (this.state.clickCount > 7) {
      document.getElementById('JFAddButton').removeAttribute("class");
      return null;
    }
    else return (
      <div onClick={this.appendCourse}>ADD BUTTON</div>
    );
  }
});

/***************************************************************************
 * Adds a course entry field with ratings slider to JUNIOR SPRING semester *
 * Button disabled after there are 7 courses                               *
 ***************************************************************************/
var AddCourseJS = React.createClass({
  getInitialState: function() {
    return{clickCount: 5};
  },
  appendCourse: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });
    var entry = genCourseEntry("JS", this.state.clickCount);
    document.getElementById('appendJS').appendChild(entry);
    showSlider();
  },
  render: function () {
    if (this.state.clickCount > 7) {
      document.getElementById('JSAddButton').removeAttribute("class");
      return null;
    }
    else return (
      <div onClick={this.appendCourse}>ADD BUTTON</div>
    );
  }
});

ReactDOM.render(<AddSemester />, document.getElementById('addSemester'), showSlider);
ReactDOM.render(<AddCourseFF />, document.getElementById('FFAddButton'));
ReactDOM.render(<AddCourseFS />, document.getElementById('FSAddButton'));
ReactDOM.render(<AddCourseSF />, document.getElementById('SFAddButton'));
ReactDOM.render(<AddCourseSS />, document.getElementById('SSAddButton'));
ReactDOM.render(<AddCourseJF />, document.getElementById('JFAddButton'));
ReactDOM.render(<AddCourseJS />, document.getElementById('JSAddButton'));
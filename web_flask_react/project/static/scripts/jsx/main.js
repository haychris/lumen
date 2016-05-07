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
    if (this.state.clickCount > 1) {
      return null;
    }
    return (
      <div id="addSemesterButtonStyle" onClick={this.appendSemester}>ADD SEMESTER</div>
    );
  }
});

function genCourseEntry(count) {
  var entry = document.createElement("div");
  entry.setAttribute("class", "courseEntry");
  var courseName = entry.appendChild(document.createElement("div"));
  var courseRating = entry.appendChild(document.createElement("div"));

  courseName.setAttribute("class", "courseName");
  courseName.appendChild(document.createElement("form"));
  courseName.firstChild.action = "query";
  var inputField = courseName.firstChild.appendChild(document.createElement("input"));
  inputField.setAttribute("class", "courseName");
  inputField.type = "text";
  inputField.placeholder = "Course " + count;

  courseRating.setAttribute("class", "courseRating");
  courseRating.appendChild(document.createElement("div"));
  courseRating.firstChild.setAttribute("class", "slider");
  return entry;
}

var AddCourseFF = React.createClass({
  getInitialState: function() {
    return{clickCount: 5};
  },
  appendCourse: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });
    var entry = genCourseEntry(this.state.clickCount);
    document.getElementById('appendFF').appendChild(entry);
    showSlider();
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

var AddCourseFS = React.createClass({
  getInitialState: function() {
    return{clickCount: 5};
  },
  appendCourse: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });
    var entry = genCourseEntry(this.state.clickCount);
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

var AddCourseSF = React.createClass({
  getInitialState: function() {
    return{clickCount: 5};
  },
  appendCourse: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });
    var entry = genCourseEntry(this.state.clickCount);
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

var AddCourseSS = React.createClass({
  getInitialState: function() {
    return{clickCount: 5};
  },
  appendCourse: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });
    var entry = genCourseEntry(this.state.clickCount);
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

var AddCourseJF = React.createClass({
  getInitialState: function() {
    return{clickCount: 5};
  },
  appendCourse: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });
    var entry = genCourseEntry(this.state.clickCount);
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

var AddCourseJS = React.createClass({
  getInitialState: function() {
    return{clickCount: 5};
  },
  appendCourse: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });
    var entry = genCourseEntry(this.state.clickCount);
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

ReactDOM.render(<AddSemester />, document.getElementById('addSemesterButton'), showSlider);
ReactDOM.render(<AddCourseFF />, document.getElementById('FFAddButton'));
ReactDOM.render(<AddCourseFS />, document.getElementById('FSAddButton'));
ReactDOM.render(<AddCourseSF />, document.getElementById('SFAddButton'));
ReactDOM.render(<AddCourseSS />, document.getElementById('SSAddButton'));
ReactDOM.render(<AddCourseJF />, document.getElementById('JFAddButton'));
ReactDOM.render(<AddCourseJS />, document.getElementById('JSAddButton'));
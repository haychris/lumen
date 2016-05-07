(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);throw new Error("Cannot find module '"+o+"'")}var f=n[o]={exports:{}};t[o][0].call(f.exports,function(e){var n=t[o][1][e];return s(n?n:e)},f,f.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var AddSemester = React.createClass({displayName: "AddSemester",
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
      React.createElement("div", {id: "addSemesterButtonStyle", onClick: this.appendSemester}, "ADD SEMESTER")
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

var AddCourseFF = React.createClass({displayName: "AddCourseFF",
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
      React.createElement("div", {onClick: this.appendCourse}, "ADD BUTTON")
    );
  }
});

var AddCourseFS = React.createClass({displayName: "AddCourseFS",
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
      React.createElement("div", {onClick: this.appendCourse}, "ADD BUTTON")
    );
  }
});

var AddCourseSF = React.createClass({displayName: "AddCourseSF",
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
      React.createElement("div", {onClick: this.appendCourse}, "ADD BUTTON")
    );
  }
});

var AddCourseSS = React.createClass({displayName: "AddCourseSS",
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
      React.createElement("div", {onClick: this.appendCourse}, "ADD BUTTON")
    );
  }
});

var AddCourseJF = React.createClass({displayName: "AddCourseJF",
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
      React.createElement("div", {onClick: this.appendCourse}, "ADD BUTTON")
    );
  }
});

var AddCourseJS = React.createClass({displayName: "AddCourseJS",
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
      React.createElement("div", {onClick: this.appendCourse}, "ADD BUTTON")
    );
  }
});

ReactDOM.render(React.createElement(AddSemester, null), document.getElementById('addSemesterButton'), showSlider);
ReactDOM.render(React.createElement(AddCourseFF, null), document.getElementById('FFAddButton'));
ReactDOM.render(React.createElement(AddCourseFS, null), document.getElementById('FSAddButton'));
ReactDOM.render(React.createElement(AddCourseSF, null), document.getElementById('SFAddButton'));
ReactDOM.render(React.createElement(AddCourseSS, null), document.getElementById('SSAddButton'));
ReactDOM.render(React.createElement(AddCourseJF, null), document.getElementById('JFAddButton'));
ReactDOM.render(React.createElement(AddCourseJS, null), document.getElementById('JSAddButton'));

},{}]},{},[1])
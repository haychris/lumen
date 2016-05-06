(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);throw new Error("Cannot find module '"+o+"'")}var f=n[o]={exports:{}};t[o][0].call(f.exports,function(e){var n=t[o][1][e];return s(n?n:e)},f,f.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var YearSelect = React.createClass({displayName: "YearSelect",
  getInitialState: function() {
    return {year: null};
  },
  freshmanSelect: function(event) {
    this.setState({year: "frosh"});
  },
  sophomoreSelect: function(event) {
    this.setState({year: "soph"});
  },
  juniorSelect: function(event) {
    this.setState({year: "junr"});
  },
  render: function() {
    //If a freshman, highlight that box and hide the sophomore/junior course input divs
    if (this.state.year == "frosh") {
      document.getElementById('freshman').setAttribute("style", "background-color: white;");
      document.getElementById('sophomore').setAttribute("style", "background-color: gray;");
      document.getElementById('junior').setAttribute("style", "background-color: gray;");
      document.getElementById('freshmanYear').setAttribute("style", "");
      document.getElementById('sophomoreYear').setAttribute("style", "display:none;");
      document.getElementById('juniorYear').setAttribute("style", "display:none;");
    }
    //If a sophomore, highlight that box and hide the junior course input divs
    if (this.state.year == "soph") {
      document.getElementById('freshman').setAttribute("style", "background-color: gray;");
      document.getElementById('sophomore').setAttribute("style", "background-color: white;");
      document.getElementById('junior').setAttribute("style", "background-color: gray;");
      document.getElementById('freshmanYear').setAttribute("style", "");
      document.getElementById('sophomoreYear').setAttribute("style", "");
      document.getElementById('juniorYear').setAttribute("style", "display:none;");
    }
    //If a junior, highlight that box and show all course input divs
    if (this.state.year == "junr") {
      document.getElementById('freshman').setAttribute("style", "background-color: gray;");
      document.getElementById('sophomore').setAttribute("style", "background-color: gray;");
      document.getElementById('junior').setAttribute("style", "background-color: white;");
      document.getElementById('freshmanYear').setAttribute("style", "");
      document.getElementById('sophomoreYear').setAttribute("style", "");
      document.getElementById('juniorYear').setAttribute("style", "");
    }
    return (
      React.createElement("div", null, 
      "What year are you?", React.createElement("br", null), 
        React.createElement("div", {id: "freshman", onClick: this.freshmanSelect}, 
          "2019"
        ), 
        React.createElement("div", {id: "sophomore", onClick: this.sophomoreSelect}, 
          "2018"
        ), 
        React.createElement("div", {id: "junior", onClick: this.juniorSelect}, 
          "2017"
        )
      )
    );
  }
});

var AddCourseFF = React.createClass({displayName: "AddCourseFF",
  getInitialState: function() {
    return{clickCount: 5};
  },
  appendCourse: function(event) {
    this.setState(function(previousState, currentProps) {
      return {clickCount: previousState.clickCount + 1};
    });
    var input = document.createElement("p");
    input.appendChild(document.createElement("input"));
    input.firstChild.type = "query";
    input.firstChild.placeholder = "Course " + this.state.clickCount;
    document.getElementById('appendFroshFall').appendChild(input);
  },
  render: function () {
    if (this.state.clickCount > 7)
      return null;
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
    var input = document.createElement("p");
    input.appendChild(document.createElement("input"));
    input.firstChild.type = "query";
    input.firstChild.placeholder = "Course " + this.state.clickCount;
    document.getElementById('appendFroshSpring').appendChild(input);
  },
  render: function () {
    if (this.state.clickCount > 7)
      return null;
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
    var input = document.createElement("p");
    input.appendChild(document.createElement("input"));
    input.firstChild.type = "query";
    input.firstChild.placeholder = "Course " + this.state.clickCount;
    document.getElementById('appendSophFall').appendChild(input);
  },
  render: function () {
    if (this.state.clickCount > 7)
      return null;
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
    var input = document.createElement("p");
    input.appendChild(document.createElement("input"));
    input.firstChild.type = "query";
    input.firstChild.placeholder = "Course " + this.state.clickCount;
    document.getElementById('appendSophSpring').appendChild(input);
  },
  render: function () {
    if (this.state.clickCount > 7)
      return null;
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
    var input = document.createElement("p");
    input.appendChild(document.createElement("input"));
    input.firstChild.type = "query";
    input.firstChild.placeholder = "Course " + this.state.clickCount;
    document.getElementById('appendJuniorFall').appendChild(input);
  },
  render: function () {
    if (this.state.clickCount > 7)
      return null;
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
    var input = document.createElement("p");
    input.appendChild(document.createElement("input"));
    input.firstChild.type = "query";
    input.firstChild.placeholder = "Course " + this.state.clickCount;
    document.getElementById('appendJuniorSpring').appendChild(input);
  },
  render: function () {
    if (this.state.clickCount > 7)
      return null;
    else return (
      React.createElement("div", {onClick: this.appendCourse}, "ADD BUTTON")
    );
  }
});

ReactDOM.render(React.createElement(YearSelect, null), document.getElementById('yearInput'));
ReactDOM.render(React.createElement(AddCourseFF, null), document.getElementById('froshFallAddButton'));
ReactDOM.render(React.createElement(AddCourseFS, null), document.getElementById('froshSpringAddButton'));
ReactDOM.render(React.createElement(AddCourseSF, null), document.getElementById('sophFallAddButton'));
ReactDOM.render(React.createElement(AddCourseSS, null), document.getElementById('sophSpringAddButton'));
ReactDOM.render(React.createElement(AddCourseJF, null), document.getElementById('juniorFallAddButton'));
ReactDOM.render(React.createElement(AddCourseJS, null), document.getElementById('juniorSpringAddButton'));

},{}]},{},[1])
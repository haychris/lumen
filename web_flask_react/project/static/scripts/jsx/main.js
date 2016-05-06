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

var AddCourseFF = React.createClass({
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
      <div onClick={this.appendCourse}>ADD BUTTON</div>
    );
  }
});

ReactDOM.render(<AddSemester />, document.getElementById('addSemesterButton'));
ReactDOM.render(<AddCourseFF />, document.getElementById('froshFallAddButton'));
ReactDOM.render(<AddCourseFS />, document.getElementById('froshSpringAddButton'));
ReactDOM.render(<AddCourseSF />, document.getElementById('sophFallAddButton'));
ReactDOM.render(<AddCourseSS />, document.getElementById('sophSpringAddButton'));
ReactDOM.render(<AddCourseJF />, document.getElementById('juniorFallAddButton'));
ReactDOM.render(<AddCourseJS />, document.getElementById('juniorSpringAddButton'));
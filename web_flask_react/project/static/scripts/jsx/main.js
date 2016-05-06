var YearSelect = React.createClass({
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
      <div>
      What year are you?<br/>
        <div id="freshman" onClick={this.freshmanSelect}>
          2019
        </div>
        <div id="sophomore" onClick={this.sophomoreSelect}>
          2018
        </div>
        <div id="junior" onClick={this.juniorSelect}>
          2017
        </div>
      </div>
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

ReactDOM.render(<YearSelect />, document.getElementById('yearInput'));
ReactDOM.render(<AddCourseFF />, document.getElementById('froshFallAddButton'));
ReactDOM.render(<AddCourseFS />, document.getElementById('froshSpringAddButton'));
ReactDOM.render(<AddCourseSF />, document.getElementById('sophFallAddButton'));
ReactDOM.render(<AddCourseSS />, document.getElementById('sophSpringAddButton'));
ReactDOM.render(<AddCourseJF />, document.getElementById('juniorFallAddButton'));
ReactDOM.render(<AddCourseJS />, document.getElementById('juniorSpringAddButton'));
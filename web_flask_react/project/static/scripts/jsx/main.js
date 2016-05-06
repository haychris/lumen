/*var FreshmanSelected = React.createClass({
  getInitialState: function() {
    return {showMe: false};
  },
  onClick: function(event) {
    this.setState({showMe: !this.state.showMe});
    console.log("CLICK");
  },
  render: function() {
    if (this.state.showMe) {
      document.getElementById('yr1L').setAttribute("style", "");
      document.getElementById('yr1R').setAttribute("style", "");
      return <p onClick={this.onClick}>Visible</p>;
    }
    else {
      document.getElementById('yr1L').setAttribute("style", "display:none;");
      document.getElementById('yr1R').setAttribute("style", "display:none;");
      return <p onClick={this.onClick}>Not visible</p>;
    }
  }
});

var SophomoreSelected = React.createClass({
  getInitialState: function() {
    return {showMe: false};
  },
  onClick: function(event) {
    this.setState({showMe: !this.state.showMe});
    FreshmanSelected.setState({showMe: false});
    console.log("CLICK");
  },
  render: function() {
    if (this.state.showMe) {
      document.getElementById('yr2L').setAttribute("style", "");
      document.getElementById('yr2R').setAttribute("style", "");
      return <p onClick={this.onClick}>Visible</p>;
    }
    else {
      document.getElementById('yr2L').setAttribute("style", "display:none;");
      document.getElementById('yr2R').setAttribute("style", "display:none;");
      return <p onClick={this.onClick}>Not visible</p>;
    }
  }
});

ReactDOM.render(<FreshmanSelected />, document.getElementById('freshman'));
ReactDOM.render(<SophomoreSelected />, document.getElementById('sophomore'));
*/

var YearSelect = React.createClass({
  getInitialState: function() {
    return {year: null};
  },
  freshmanSelect: function(event) {
    this.setState({year: "frosh"});
    console.log("FROSH");
  },
  sophomoreSelect: function(event) {
    this.setState({year: "soph"});
    console.log("SOPH");
  },
  juniorSelect: function(event) {
    this.setState({year: "junr"});
    console.log("JUNR");
  },
  render: function() {
    if (this.state.year == "frosh") {
      document.getElementById('yr1L').setAttribute("style", "");
      document.getElementById('yr1R').setAttribute("style", "");
      document.getElementById('yr2L').setAttribute("style", "display:none;");
      document.getElementById('yr2R').setAttribute("style", "display:none;");
      document.getElementById('yr3L').setAttribute("style", "display:none;");
      document.getElementById('yr3R').setAttribute("style", "display:none;");
    }
    if (this.state.year == "soph") {
      document.getElementById('yr1L').setAttribute("style", "");
      document.getElementById('yr1R').setAttribute("style", "");
      document.getElementById('yr2L').setAttribute("style", "");
      document.getElementById('yr2R').setAttribute("style", "");
      document.getElementById('yr3L').setAttribute("style", "display:none;");
      document.getElementById('yr3R').setAttribute("style", "display:none;");
    }
    if (this.state.year == "junr") {
      document.getElementById('yr1L').setAttribute("style", "");
      document.getElementById('yr1R').setAttribute("style", "");
      document.getElementById('yr2L').setAttribute("style", "");
      document.getElementById('yr2R').setAttribute("style", "");
      document.getElementById('yr3L').setAttribute("style", "");
      document.getElementById('yr3R').setAttribute("style", "");
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
ReactDOM.render(<YearSelect />, document.getElementById('yearInput'));


/*var ShowCourseHistInput = React.createClass({
  getInitialState: function() {
    return {clicked: false};
  },
  handleClick: function(event) {
    this.setState({clicked: !this.state.clicked});
    console.log("CLICK");
  },
  render: function() {
    var text = this.state.clicked ? 'like' : 'haven\'t liked';
    return (
      <div onClick={this.handleClick}>
        You {text} this. Click to toggle.
      </div>
      <div onClick={this.handleClick}>
        {this.state.clicked ? <Year /> : null}
      </div>
    );
  }
});

var Year = React.createClass({
  render: function() {
    return (
      <div id="yr1L">TEXT</div>
    );
  }
});

var Search = React.createClass({
    getInitialState: function() {
        return { showResults: false };
    },
    onClick: function() {
        this.setState({ showResults: !this.state.showResults});
    },
    render: function() {
        return (
            <div>
                <input type="submit" value="Search" onClick={this.onClick} />
                { this.state.showResults ? <Results /> : null }
            </div>
        );
    }
});

var Results = React.createClass({
    render: function() {
        return (
            <div id="results" className="search-results">
                Some Results
            </div>
        );
    }
});

ReactDOM.render(<Search />, document.getElementById('freshman'));*/


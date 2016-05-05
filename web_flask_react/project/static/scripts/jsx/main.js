var showCourseInputForms = React.createClass({
  getInitialState: function() {
    return {liked: false};
  },
  handleClick: function(event) 
    this.setState({liked: !this.state.liked});
  },

  render: function() {
    return (
      <div onclick={this.handleClick}>
        YAY
      </div>
    );
  }
});

ReactDOM.render(
  <showCourseInputForms />,
  document.getElementById('freshman')
);
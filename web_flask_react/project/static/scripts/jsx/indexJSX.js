var InputCourseHist = React.createClass({
  checkCookie: function() {
    if (hasCookie())
      window.location = 'recommend';
    else
      window.location = 'userratings';
    return;
  },
  render: function() {
    return (
      <div id="courseHistButtonStyle" onClick={this.checkCookie}>Explore Recommendations</div>
    );
  }
});

ReactDOM.render(<InputCourseHist />, document.getElementById('courseHistButton'));
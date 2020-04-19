import React from 'react';

const __html = require('./676_website/index.html');
const template = { __html: __html };

React.module.exports = React.createClass({
  render: function() {
    return(
      <div dangerouslySetInnerHTML={template} />
    );
  }
});
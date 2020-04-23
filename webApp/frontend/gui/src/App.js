import React, { Component, Fragment } from 'react';
import MainFunc from './mainFunction'
import Header from './header'
import Footer from './footer'
import data from './dataStore'

const axios = require('axios');
const url = "http://ec2-3-84-85-14.compute-1.amazonaws.com/recommender/?user_id=";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      userID: "",
      isIdInvalid: false,
      errorText:"",
      topics: {
        labels : [],
        data : [],
      },
      posts: []
    };
    this.handleSend = this.handleSend.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.getPosts = this.getPosts.bind(this)
  }

  getPosts = () => {
    axios.get(url + this.state.userID)
      .then((response) => {
        this.setState({
          posts: response.data.posts,
          topics : {
            labels : response.data.topics.labels,
            data : response.data.topics.data,
          }
        })
      })
      .catch((error) => {
        // handle error
        console.log(error);
        this.setState({
          isIdInvalid : true,
          errorText : "Invalid/Private account ID",
        })
      })
  }

  handleSend = (event) => {
    this.getPosts()
    this.setState({
      isIdInvalid : false,
      errorText : "",
      topics: {
        labels : [],
        data : [],
      },
      posts: []
    })
  }

  handleChange = (event) => {
    this.setState({
      userID: event.target.value
    })
  }

  render() {
    return (
      <Fragment>
        <Header />
        <MainFunc
          userID={this.state.userID}
          handleChange={this.handleChange}
          handleSend={this.handleSend}
          posts={this.state.posts}
          topics={this.state.topics}
          isIdInvalid={this.state.isIdInvalid}
          errorText={this.state.errorText}
        />
      </Fragment>
    );
  }
}

export default App;

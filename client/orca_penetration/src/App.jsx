import React, { Component } from 'react';
import './App.css';
// import {
//   BrowserRouter as Router,
//   Route,
//   Link,
//   Switch,
//   Redirect,
// } from 'react-router-dom';
// import Button from '@material-ui/core/Button/index';
import MyMap from "./components/MyMap";

class App extends Component {
  /* eslint-disable jsx-a11y/control-has-associated-label */

  render() {
    return <MyMap />
  }
}

export default App;

import React, { Component } from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Route,
  Link,
  Switch,
  Redirect,
} from 'react-router-dom';

import MapPage from "./components/MapPage";
import HomePage from "./components/HomePage";
import Estimator from "./components/Estimator";
import Nav from "./components/Nav";

class App extends Component {
  render() {
    return (
      <Router>
        <div className='App'>
          <Nav />
          <div>
            <Switch>
              <Route exact path='/' component={HomePage} />
              <Route path='/Estimator' component={Estimator} />
            </Switch>
          </div>
        </div>
      </Router>
    );
  }
}

export default App;

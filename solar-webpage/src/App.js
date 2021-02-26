import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import Layout from './components/Layout';
import Batteries from './pages/Batteries';
import Summary from './pages/Summary';
import Temperatures from './pages/Temperatures';
import GPS from './pages/GPS';

function App() {
  return (
    // <div className="App">
    //   <header className="App-header">
    //     <img src={logo} className="App-logo" alt="logo" />
    //     <p>
    //       Edit <code>src/App.js</code> and save to reload.
    //     </p>
    //     <a
    //       className="App-link"
    //       href="https://reactjs.org"
    //       target="_blank"
    //       rel="noopener noreferrer"
    //     >
    //       Learn React
    //     </a>
    //   </header>
    // </div>
    <Layout>
      <Router>
        <Switch>
          <Route path="/gps">
            <GPS />
          </Route>
          <Route path="/temps">
            <Temperatures />
          </Route>
          <Route path="/batteries">
            <Batteries />
          </Route>
          <Route path="/">
            <Summary />
          </Route>
        </Switch>
      </Router>
    </Layout>
  );
}

export default App;

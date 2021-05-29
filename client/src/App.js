import React from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import WorldCharity from "./components/WorldCharity";
import Transfer from "./components/Transfer";
import Govern from "./components/Govern";
import Rule from "./components/Rule";
import HeaderMenu from "./components/HeaderMenu";


function App() {
  return (
    <div className="App">
     
      <Router>
      <HeaderMenu />

        <Switch>
          <Route path="/transfer">
            <Transfer />
          </Route>
          <Route path="/rule">
            <Rule />
          </Route>
          <Route path="/govern">
            <Govern />
          </Route>
          <Route path="/">
            <WorldCharity />
          </Route>


        </Switch>
      </Router>
    </div>
  );
}

export default App;

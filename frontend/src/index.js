import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {BrowserRouter as Router, Route,  Switch} from 'react-router-dom';
import Chat from './Components/Chat';
import Login from './authentification/Login';

// ReactDOM.render(
//   <App />,
//   document.getElementById('root')
// );

ReactDOM.render(<Router>
  <Switch>
      <Route exact path='/' component={Login}></Route>
      <Route exact path='/home' component={App}></Route>
      <Route exact path='/chat' component={Chat}></Route>
  </Switch>
</Router>,
document.getElementById('root') 
);

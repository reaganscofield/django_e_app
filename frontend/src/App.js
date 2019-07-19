import React, { Component } from 'react';
import Chat from './Components/Chat';
import axios from 'axios';

class App extends Component {
  constructor(props) {
    super(props)
  
    this.state = {
       
    }
  }

  componentWillMount(){
    try {
      const User = JSON.parse(sessionStorage.getItem("User"));
      if(!User){
        window.location.replace("/");
      }
      const token =  User.token;
      const config = {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`
        }
      }
     axios.get('http://localhost:4500/api/system/is_logged_in', config).then((response) => {
       sessionStorage.setItem("UserObj", JSON.stringify(response.data));
     }).catch(error => {
       console.log(" eeee ", error)
     })
    } catch(err) {
      console.log(err)
    }
  }
  
  render() {
    return (
      <div>
       <Chat />
      </div>
    );
  }
}

export default App;

import React, { Component } from 'react'

export default class Product extends Component {
    constructor(props) {
        super(props)
      
        this.state = {
          username: '',
          message: '',
          messages: [],
          id: '26882308-ljksdfljkl-rl;l'
        }
    
        this.socket = io('http://localhost:8281',   { transport : ['websocket'] });
       
        this.socket.on('RECEIVE_MESSAGE', function(data){
          console.log(data);
          addMessage(data);
        });
    
        const addMessage = data => {
          this.setState({messages: [...this.state.messages, data]});
          console.log(this.state.messages);
        };
    
        this.sendMessage = ev => {
          ev.preventDefault();
          this.socket.emit('SEND_MESSAGE', {
              
              author: this.state.username,
              message: this.state.message
          });
          this.setState({message: ''});
        }
    
    
    }
    
    render() {
        return (
            <div>
                
            </div>
        )
    }
}

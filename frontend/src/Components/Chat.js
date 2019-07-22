import React, { Component } from 'react'
import './Chat.css'
import axios from 'axios'
import JWTDecoder from 'jwt-decode';
import io from "socket.io-client";


import { w3cwebsocket as Socket} from "websocket";

export default class Chat extends Component {
    constructor(props) {
        super(props)
    
        this.state = {
             receiverStories: [],
             senderStories: [],
             users: [],
             selectedContact: {},
             message: '',
             UserObj: {},
        }
    }

    componentWillMount(){
        const User = JSON.parse(sessionStorage.getItem("User"));
        if(User){
          const UserObj = JSON.parse(sessionStorage.getItem("UserObj"));
          this.setState({ UserObj: UserObj });
        }
        this.queryUsers();

        //const socket = 'ws://';
       // console.log("my socket ", socket, window.location.host, window.location.pathname)

        const { selectedContact } = this.state;
        //this.queryReceiver(User.id, selectedContact.id);
    }

    queryUsers = () => {
        axios.get('http://localhost:4500/api/users_message/').then(response => {
            if(response){
              this.setState({
                  users: response.data
              });
            }
        });
    }

    queryReceiver = (sender, receiver) => {
        const socket_host = 'ws://';
        const host = '127.0.0.1:4500/' // window.location.host;
        const path = 'api/messages/' // window.location.pathname;
        const url_chat = `${socket_host}${host}${path}${receiver}`;

        const clientSocket = new Socket(url_chat);

        clientSocket.onopen = (e) => {
          // console.log("connection etablished", e);
        }

        // clientSocket.onmessage = (event) => {
        //   console.log(event)
        // }
        //  console.log("uuu ", url_chat)


     
    }


    handleEnter = (e) => {
      const { message, selectedContact } = this.state;
      if(e.charCode === 13){

        const messageData = {
          sender: this.state.UserObj.username, 
          receiver: selectedContact.username,
          message: message
        }

        const socket_host = 'ws://';
        const host = '127.0.0.1:4500/' 
        const path = 'api/messages/';
        const url_chat = `${socket_host}${host}${path}${selectedContact.id}`;

        const clientSocket = new Socket(url_chat);

        clientSocket.onopen = function(event) {
          clientSocket.send(JSON.stringify(messageData));
        }


        clientSocket.onmessage = function(event) {
          // clientSocket.send(messageData);
          console.log(" on message ", event.data);
        }



        clientSocket.onoerror = function(e)  {
          console.log(" on error", e);
        }
        clientSocket.onclose = function(e)  {
          console.log(" on close ", e);
        }

      
        this.setState({
          message: ''
        })
      }
    }

    // queryReceiver = (sender, receiver) => {
    //     // axios.get(`http://localhost:4500/api/messages/${sender}/${receiver}/`).then(response => {
    //     //     if(response){
    //     //       this.setState({
    //     //           receiverStories: response.data
    //     //       });
    //     //     }
    //     // });
    // }

    handleChange = (e)  => {
      this.setState({ [e.target.name]: e.target.value });
    }

    // handleEnter = (e) => {
    //   const { message, selectedContact } = this.state;
    //   if(e.charCode === 13){
    //     const messageData = {
    //       sender: this.state.UserObj.username, 
    //       receiver: selectedContact.username,
    //       message: message
    //     }
    //     axios.post(`http://localhost:4500/api/messages/`, messageData).then((response) => {
    //       const sent = response.data;
    //       this.state.receiverStories.push(sent);
    //     }) 
    //     this.setState({
    //       message: ''
    //     })
    //   }
    // }

    selectedContact = (selectedContact) => {
        const currentUserToken = this.state.UserObj
        if(Object.entries(selectedContact).length > 0){
            this.setState({ selectedContact });
            this.queryReceiver(currentUserToken.id, selectedContact.id);
        }
    }
    
    render() {




       
        return (
            <div>
            <div id="chat">
          {/* parent */}
          <div className="left" id="conversations-list">
 
            <div className="list-container d-flex flex-column">

              <div className="chat__search bg-light text-white d-flex flex-column">
                <div className="text-dark text-center p-2 d-flex flex-row">
                  <h5 className="w-100 m-0">Conversations</h5>
                  <a href="/" className="text-danger ml-auto">
                    <i className="far fa-trash-alt" />
                  </a>
                </div>
                <div className="d-flex flex-row px-2 py-1">
                  <input
                    id="search__input"
                    type="text"
                    placeholder="type here..."
                    className="mr-2 w-100"
                  />
                  <a href="/" id="chat__search-button">
                    <i className="fas fa-search text-secondary" />
                  </a>
                </div>
              </div>
           
              <div id="conversations__list" className="scroll-style-1">
                {this.state.users.map((element, index) => (
                    <div key={index} onClick={() => this.selectedContact(element)} className="p-2 conversations__item cusror-pointer" >
                        <span className="d-flex flex-row justify-content-around text-dark">
                      <div className="chat__item__avatar bg-dark mr-2 align-self-center" />
                      <div className="conversations__meta-info align-self-center p-2">
                        <p className="m-0 align-self-center">{element.first_name}</p>
                        <small className="align-self-center">
                          <i>Lorem ipsum dolor..</i>
                        </small>
                      </div>
                      <p className=" m-0 text-right">
                        <small>
                          <i>10 minutes</i>
                        </small>
                      </p>
                    </span>
                  </div>
                ))}
              </div>


            </div>
          </div>


          <div className="right" id="conversation">

     
            {Object.entries(this.state.selectedContact).length > 0 ? 
              <div className="chat-header d-flex align-items-center p-2 bg-light">
                <div className="chat__item__avatar bg-dark mr-2" />
                <div className="meta-info w-100 text-center">
                  <p className="m-0">
                    <strong>{this.state.selectedContact.first_name}</strong>
                  </p>
                  <div className="chat__header-meta">
                    <small>
                      <i>9 minutes ago</i>
                    </small>
                  </div>
                </div>
                <a href="/" className="mr-2 ml-auto">
                  <i className="fas fa-video fa-2x" />
                </a>
                <a href="/" className="text-dark">
                  <i className="fas fa-ellipsis-v" />
                </a>
              </div>
              : null
            }
        
    
          <div className="chat-body p-2  scroll-style-1">
            {this.state.receiverStories.map((element, index) => (
              <div key={index}>
                  {element.sender === "reaganscofield" ?
                     <div className="chat__item-wrapper d-flex flex-row mb-3">
                     <div className="chat__item chat__item-right ml-auto text-right">
                         <p className="mb-0">
                             {element.message}
                         </p>
                         <div className="meta text-dark mt-2">
                             <small>
                                 <i>{element.timestamp}</i>
                             </small>
                         </div>
                     </div>
                     <div className="chat__item__avatar bg-dark" />
                 </div>
                 :
                 <div className="chat__item-wrapper d-flex flex-row mb-3">
                 <div className="chat__item__avatar bg-dark" />
                     <div className="chat__item chat__item-left mr-auto">
                         <p className="mb-0">
                             {element.message}
                         </p>
                     <div className="meta text-dark mt-2">
                         <small>
                             <i>{element.timestamp}</i>
                         </small>
                     </div>
                 </div>
             </div>
                  }
              </div>    
            ))}
          </div>
       
          {Object.entries(this.state.selectedContact).length !== 0 ?
            <div className="chat-footer bg-light d-flex flex-row justify-content-around p-2">
              <textarea
                name="message"
                onChange={this.handleChange}
                onKeyPress={this.handleEnter}
                value={this.state.message}
                className="w-100 mx-1"
                placeholder="Type ......."
                id="chat-input"
              />
              <a href="/" className="mx-1 align-self-center">
                <i className="fas fa-camera fa-2x" />
              </a>
              <a href="/" className="mx-1 align-self-center">
                <i className="far fa-image fa-2x" />
              </a>
              <a href="/" className="mx-1 align-self-center">
                <i className="far fa-grin fa-2x" />
              </a>
            </div>
            : null
          }

 

        </div>
      </div> 
    </div>
        )
    }
}

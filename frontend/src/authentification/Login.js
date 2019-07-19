import React, { Component } from 'react'
import axios from 'axios';

export default class Login extends Component {
    constructor(props) {
        super(props)
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmission = this.handleSubmission.bind(this);
        this.state = {
           username: null,
           password: null,
           check: null,
           usernameErorr: {},
           passwordError: {},
           usernameFlash: null,
           passwordFlash: null
        }
      }
  
    handleChange = (e) => {
      this.setState({ [e.target.name]: e.target.value });
    };
  
    handleSubmission = (e) => {
      e.preventDefault();
      const { password, username } = this.state;
      if(username === null ){ 
        this.setState({ 
          usernameError: {
            border: '1px solid red'
          }, usernameFlash: 'please enter your username'
        }); 
      } else if(password === null ) {
          this.setState({ 
          passwordError: {
            border: '1px solid red'
          }, passwordFlash: 'please enter your password'
        }); 
      } else {
         const user = {
             username: username,
             password: password
         }
         axios.post('http://localhost:4500/api/system/login', user).then((response) => {
            const User = response.data;
            sessionStorage.setItem("User", JSON.stringify(User));
            window.location.replace("/home")
         })
      }
    }
  
    forgetPassword = () => {
      this.props.passwordForgetComponents();
    }
    render() {
        return (
            <div>
                 <div className="text-light container mg-top">
        <div className="row">
            <div className="col-lg-4" />
            <div className="col-lg-4">
                 <form>
                    <div className="form-group">
                        <label>Username</label>
                        <input
                          style={this.state.usernameError}
                          onChange={this.handleChange} 
                          value={this.state.username || ''}
                          name="username"
                          type="text" className="form-control" 
                          aria-describedby="emailHelp" 
                          placeholder="Username" />
                        {this.state.usernameFlash === null ?
                          <small className="form-text text-muted">
                            We'll never share your email with anyone else.
                          </small>
                          :
                          <small className="form-text text-danger">
                           {this.state.usernameFlash}
                          </small>
                        }
                      
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input
                          style={this.state.passwordError}
                          value={this.state.password || ''}
                          onChange={this.handleChange} 
                          type="password" 
                          name="password"
                          className="form-control" 
                          placeholder="Password" />
                        <small className="form-text text-danger">
                           {this.state.passwordFlash}
                        </small>
                    </div>
                    <div className="form-group form-check">
                        <input
                          value={this.state.check || ''}
                          onChange={this.handleChange} 
                          type="checkbox" 
                          name="check"
                          className="form-check-input" 
                        />
                          <label className="form-check-label">Check me out</label>
                          <span 
                              onClick={this.forgetPassword} 
                              className="form-check-label float-right cursorOn"
                          >
                            Forget Password
                          </span>
                    </div>
                    <button onClick={this.handleSubmission} className="btn btn-info btn-block">Submit</button>
                </form>
            </div>
            <div className="col-lg-4" />
        </div>
      </div>
            </div>
        )
    }
}

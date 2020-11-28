import React, { Component } from 'react';
import { Header } from '../components';

// redux
import { connect } from 'react-redux';
import { getStatusRequest, logoutRequest } from '../actions/authentication';

class App extends Component { 
    componentDidMount() {
        // get cookie by name
        function getCookie(name) {
            var value = "; " + document.cookie;
            var parts = value.split("; " + name + "=");
            if (parts.length === 2) return parts.pop().split(";").shift();
        }

        let loginData = getCookie('key');

        // if loginData is undefined, do nothing
        if (typeof loginData === "undefined") return;

        // decode and parse
        loginData = JSON.parse(atob(loginData));
        
        // if not logged in, do nothing
        if(!loginData.isLoggedIn) return;

        this.props.getStatusRequest().then(
            () => {
                // if session is not valid
                if(!this.props.status.valid) {
                    // logout the session
                    loginData = {
                        isLoggedIn: false,
                        userid: '',
                        role: ''
                    };

                    document.cookie = 'key=' +btoa(JSON.stringify(loginData));

                    // and notify
                    let $toastContent = window.$('<span style="color: #FFB4BA">Your session is expired, please log in again</span>');
                    window.Materialize.toast($toastContent, 4000);
                }
            }
        )
    }

    handleLogout = () => {
        this.props.logoutRequest().then(
            () => {
                window.Materialize.toast('Good Bye!', 2000);

                // Clear session
                let loginData = {
                    isLoggedIn: false,
                    userid: '',
                    role: ''
                };

                document.cookie = 'key=' + btoa(JSON.stringify(loginData));
            }
        )
    }

    render() {
        // don't render at /login or /register
        let re = /(login|register)/;
        let isAuth = re.test(this.props.location.pathname);

        return (
            <div>
                {isAuth ? undefined : <Header isLoggedIn={this.props.status.isLoggedIn}
                                                onLogout={this.handleLogout}
                />}
            </div>
        )
    }
}

// ==================================================
// can use redux state and thunk like component props
const mapStateToProps = (state) => {
    return {
        status: state.authentication.status,
        errorMessage: state.authentication.error
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        getStatusRequest: () => {
            return dispatch(getStatusRequest());
        },
        logoutRequest: () => {
            return dispatch(logoutRequest());
        }
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(App);
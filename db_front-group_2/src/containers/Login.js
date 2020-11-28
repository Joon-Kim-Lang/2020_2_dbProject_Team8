import React, { Component } from 'react';
import { Authentication } from '../components';

// redux
import { connect } from 'react-redux';
import { loginRequest } from '../actions/authentication';

class Login extends Component {
    handleLogin = (id, password) => {
        return this.props.loginRequest(id, password).then(
            () => {
                if(this.props.status === "SUCCESS") {
                    let loginData = {
                        isLoggedIn: true,
                        userid: id,
                        role: this.props.role
                    };

                    document.cookie = 'key=' + btoa(JSON.stringify(loginData));

                    window.Materialize.toast('Welcome, ' + id + '!', 2000);
                    if (this.props.role === "A")
                        this.props.history.push('/admin');
                    else if (this.props.role === "S")
                        window.location.assign("http://localhost:3000/submitter?id=" + id)
                    else
                        window.location.assign("http://localhost:3000/evaluator?id=" + id)
                    return true;
                } else {
                    let $toastContent = window.$('<span style="color: #FFB4BA">' + this.props.errorMessage + '</span>');
                    window.Materialize.toast($toastContent, 2000);
                    return false;
                }
            }
        )
    }

    render() {
        return (
            <div>
                <Authentication mode={true}
                    onLogin={this.handleLogin}
                />
            </div>
        )
    }
}

// ==================================================
// can use redux state and thunk like component props
const mapStateToProps = (state) => {
    return {
        status: state.authentication.login.status,
        errorMessage: state.authentication.login.error,
        role: state.authentication.status.role
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        loginRequest: (id, password) => {
            return dispatch(loginRequest(id, password));
        }
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Login);
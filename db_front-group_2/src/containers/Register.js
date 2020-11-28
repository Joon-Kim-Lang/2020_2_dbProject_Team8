import React, { Component } from 'react';
import { Authentication } from '../components';

// redux
import { connect } from 'react-redux';
import { registerRequest } from '../actions/authentication';

class Register extends Component {
    handleRegister = (id, password, name, address, gender, phone, birth, role) => {
        return this.props.registerRequest(id, password, name, address, gender, phone, birth, role).then(
            () => {
                if (this.props.status === "SUCCESS") {
                    window.Materialize.toast('Success! Please log in.', 2000);
                    this.props.history.push('/login');
                    return true;
                } else {
                    let $toastContent = window.$('<span style="color: #FFB4BA">' + this.props.errorMessage + '</span>');
                    window.Materialize.toast($toastContent, 2000);
                    return false;
                }
            }
        );
    }

    render() {
        return (
            <div>
                <Authentication mode={false}
                    onRegister={this.handleRegister}
                />
            </div>
        );
    }
}

// ==================================================
// can use redux state and thunk like component props
const mapStateToProps = (state) => {
    return {
        status: state.authentication.register.status,
        errorMessage: state.authentication.register.error
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        registerRequest: (id, password, name, address, gender, phone, birth, role) => {
            return dispatch(registerRequest(id, password, name, address, gender, phone, birth, role));
        }
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Register);
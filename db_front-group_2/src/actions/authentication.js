import axios from 'axios';
import {
    AUTH_REGISTER,
    AUTH_REGISTER_SUCCESS,
    AUTH_REGISTER_FAILURE,
    AUTH_LOGIN,
    AUTH_LOGIN_FAILURE,
    AUTH_LOGIN_SUCCESS,
    AUTH_GET_STATUS,
    AUTH_GET_STATUS_FAILURE,
    AUTH_GET_STATUS_SUCCESS,
    AUTH_LOGOUT
} from './ActionTypes';

// Logout
export function logoutRequest() {
    return (dispatch) => {
        return axios.post(
            'http://localhost:3000/api/logout/'
        ).then((response) => {
            dispatch(logout());
        });
    }
}

// Session
export function getStatusRequest() {
    return (dispatch) => {
        // get status API starting
        dispatch(getStatus());

        return axios.get('http://localhost:3000/api/getinfo/')
        .then((response) => {
            dispatch(getStatusSuccess(response.data.info.username));
        }).catch((error) => {
            dispatch(getStatusFailure());
        });
    }
}

// Login
export function loginRequest(id, password) {
    return (dispatch) => {
        // Login API starting
        dispatch(login());

        // Request
        return axios.post(
            'http://localhost:3000/api/login/', {
                'userid': id,
                'password': password
        }).then((response) => {
            let role = response.data['role'];
            dispatch(loginSuccess(id, role));
        }).catch((error) => {
            console.log(error);
            dispatch(loginFailure(error.response.data.code));
        });
    }
}

// Register
export function registerRequest(id, password, name, address, gender, phone, birth, role) {
    return (dispatch) => {
        // Register API starting
        dispatch(register());

        // Request
        return axios.post(
            'http://localhost:3000/api/register/', {
                'userid': id,
                'password': password,
                'name': name,
                'address': address,
                'gender': gender,
                'phone': phone,
                'birth': birth,
                'role': role
        }).then((response) => {
                dispatch(registerSuccess());
        }).catch((error) => {
            console.log(error);
            dispatch(registerFailure(error.response.data.code));
        });
    };
}


export function logout() {
    return {
        type: AUTH_LOGOUT
    };
}
export function getStatus() {
    return {
        type: AUTH_GET_STATUS
    };
}

export function getStatusSuccess(id, role) {
    return {
        type: AUTH_GET_STATUS_SUCCESS,
        id,
        role
    };
}

export function getStatusFailure() {
    return {
        type: AUTH_GET_STATUS_FAILURE
    };
}

export function login() {
    return {
        type: AUTH_LOGIN
    };
}

export function loginSuccess(id, role) {
    return {
        type: AUTH_LOGIN_SUCCESS,
        id,
        role
    };
}

export function loginFailure(error) {
    return {
        type: AUTH_LOGIN_FAILURE,
        error
    };
}

export function register() {
    return {
        type: AUTH_REGISTER
    };
}

export function registerSuccess() {
    return {
        type: AUTH_REGISTER_SUCCESS,
    };
}

export function registerFailure(error) {
    return {
        type: AUTH_REGISTER_FAILURE,
        error
    };
}
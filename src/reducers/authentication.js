import * as types from '../actions/ActionTypes';

const initialState = {
    login: {
        status: 'INIT',
        error: -1
    },
    register: {
        status: 'INIT',
        error: -1
    },
    status: {
        valid: false,
        isLoggedIn: false,
        currentUser: '',
        role: ''
    }
}

export default function authentication(state = initialState, action) {
    switch(action.type) {
        case types.AUTH_REGISTER:
            return {
                ...state,
                register: {
                    status: 'WAITING',
                    error: -1
                }
            }
        case types.AUTH_REGISTER_SUCCESS:
            return {
                ...state,
                register: {
                    ...state.register,
                    status: 'SUCCESS'
                }
            }
        case types.AUTH_REGISTER_FAILURE:
            return {
                ...state,
                register: {
                    status: 'FAILURE',
                    error: action.error
                }
            }
        case types.AUTH_LOGIN:
            return {
                ...state,
                login: {
                    status: 'WAITING',
                    error: -1
                }
            }
        case types.AUTH_LOGIN_SUCCESS:
            return {
                ...state,
                login: {
                    ...state.login,
                    status: 'SUCCESS',
                },
                status: {
                    ...state.status,
                    isLoggedIn: true,
                    currentUser: action.id,
                    role: action.role
                }
            }
        case types.AUTH_LOGIN_FAILURE:
            return {
                ...state,
                login: {
                    status: 'FAILURE',
                    error: action.error
                }
            }
        case types.AUTH_GET_STATUS:
            return {
                ...state,
                status: {
                    ...state.status,
                    isLoggedIn: true
                }
            }
        case types.AUTH_GET_STATUS_SUCCESS:
            return {
                ...state,
                status: {
                    ...state.status,
                    valid: true,
                    currentUser: action.id,
                    role: action.role
                }
            }
        case types.AUTH_GET_STATUS_FAILURE:
            return {
                ...state,
                status: {
                    ...state.status,
                    valid: false,
                    isLoggedIn: false
                }
            }
        case types.AUTH_LOGOUT:
            return {
                ...state,
                status: {
                    ...state.status,
                    isLoggedIn: false,
                    currentUser: '',
                    role: ''
                }
            }
        default:
            return state;
    }
};
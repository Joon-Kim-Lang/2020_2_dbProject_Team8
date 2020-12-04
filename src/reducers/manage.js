import * as types from '../actions/ActionTypes';

const initialState = {
    manage: {
        status: 'INIT',
        error: -1
    },
    allowsubmitter: {
        status: 'INIT',
        error: -1
    },
    addord: {
        status: 'INIT',
        error: -1
    }
}



export default function manage(state = initialState, action) {
    switch(action.type) {
        case types.MANAGE_MAIN:
            return {
                ...state,
                manage: {
                    ...state.register
                    status: 'SUCCESS'
                }
            }
        case types.PARTICIPANT_ADD:
            return {
                ...state,
                allowsubmitter: {
                    status: 'WAITING',
                    error: -1
                }
            }
        case types.PARTICIPANT_ADD_SUCCESS:
            return {
                ...state,
                allowsubmitter: {
                    ...state.register,
                    status: 'SUCCESS'
                }
            }
        case types.PARTICIPANT_ADD_FAILURE:
            return {
                ...state,
                allowsubmitter: {
                    status: 'FAILURE',
                    error: action.error
                }
            }
        case types.DATATYPE_ADD:
            return {
                ...state,
                addord: {
                    status: 'WAITING',
                    error: -1
                }
            }
        case types.DATATYPE_ADD_SUCCESS:
            return {
                ...state,
                addord: {
                    ...state.register,
                    status: 'SUCCESS'
                }
            }
        case types.DATATYPE_ADD_FAILURE:
            return {
                ...state,
                addord: {
                    status: 'FAILURE',
                    error: action.error
                }
            }
        case types.PASSVAL_SET:
            return {
                ...state,
                status: {
                    status: 'WAITING',
                    error: -1
                }
            }
        case types.PASSVAL_SET_SUCCESS:
            return {
                ...state,
                status: {
                    ...state.register,
                    status: 'SUCCESS'
                }
            }
        case types.PASSVAL_SET_FAILURE:
            return {
                ...state,
                status: {
                    status: 'FAILURE',
                    error: action.error
                }
            }

        default:
            return state;
    }
};

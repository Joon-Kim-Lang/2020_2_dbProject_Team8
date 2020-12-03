import * as types from '../actions/ActionTypes';

const initialState = {
    manage: {
        status: 'INIT',
        error: -1
    },
    allow: {
        status: 'INIT',
        error: -1
    },
    addto: {
        status: 'INIT',
        error: -1
    }
}



export default function manage(state = initialState, action) {
    switch(action.type) {
        case types.PARTICIPANT_ADD:
            return {
                ...state,
                allow: {
                    status: 'WAITING',
                    error: -1
                }
            }
        case types.PARTICIPANT_ADD_SUCCESS:
            return {
                ...state,
                allow: {
                    ...state.register,
                    status: 'SUCCESS'
                }
            }
        case types.PARTICIPANT_ADD_FAILURE:
            return {
                ...state,
                allow: {
                    status: 'FAILURE',
                    error: action.error
                }
            }
        case types.DATATYPE_ADD:
            return {
                ...state,
                addto: {
                    status: 'WAITING',
                    error: -1
                }
            }
        case types.DATATYPE_ADD_SUCCESS:
            return {
                ...state,
                addto: {
                    ...state.register,
                    status: 'SUCCESS'
                }
            }
        case types.DATATYPE_ADD_FAILURE:
            return {
                ...state,
                addto: {
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

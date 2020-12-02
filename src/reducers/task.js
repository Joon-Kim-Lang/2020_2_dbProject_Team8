import * as types from '../actions/ActionTypes';

const initialState = {
    submit: {
        status: 'INIT',
        error: -1
    },
}

export default function task(state = initialState, action) {
    switch(action.type) {
        case types.TASK_CREATE:
            return {
                ...state,
                submit: {
                    status: 'WAITING',
                    error: -1
                }
            }
        case types.TASK_CREATE_SUCCESS:
            return {
                ...state,
                submit: {
                    ...state.register,
                    status: 'SUCCESS'
                }
            }
        case types.TASK_CREATE_FAILURE:
            return {
                ...state,
                submit: {
                    status: 'FAILURE',
                    error: action.error
                }
            }
        default:
            return state;
    }
};
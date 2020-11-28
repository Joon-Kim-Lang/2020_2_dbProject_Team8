import axios from 'axios';
import {
    TASK_CREATE,
    TASK_CREATE_SUCCESS,
    TASK_CREATE_FAILURE
} from './ActionTypes';

// Register
export function taskCreateRequest(name, description, minuploadcycle, tdtname, tdtschema) {
    return (dispatch) => {
        // Register API starting
        dispatch(taskCreate());

        return axios.post(
            'http://localhost:3000/api/task/create/', {
                'name': name,
                'description': description,
                'minuploadcycle': minuploadcycle,
                'tdtname': tdtname,
                'tdtschema': tdtschema
        }).then((response) => {
            dispatch(taskCreateSuccess());
        }).catch((error) => {
            console.log(error);
            dispatch(taskCreateFailure(error.response.data.code));
        });
    };
}

export function taskCreate() {
    return {
        type: TASK_CREATE
    };
}

export function taskCreateSuccess() {
    return {
        type: TASK_CREATE_SUCCESS,
    };
}

export function taskCreateFailure(error) {
    return {
        type: TASK_CREATE_FAILURE,
        error
    };
}
import axios from 'axios';
import {
    MANAGE_MAIN,
    PARTICIPANT_ADD,
    PARTICIPANT_ADD_SUCCESS,
    PARTICIPANT_ADD_FAILURE,
    DATATYPE_ADD,
    DATATYPE_ADD_SUCCESS,
    DATATYPE_ADD_FAILURE
} from './ActionTypes';

//main for managing task
export function manageMainRequest() {
    return (dispatch) => {
        return axios.post(
            'http://localhost:3000/task/manage/'
        ).then((response) => {
            dispatch(manageMain());
        });
    }
}


// add submitter to task
export function addParticipantRequest(member_id, taskname) {
    return (dispatch) => {
        // Register API starting
        dispatch(participantAdd());

        return axios.post(
            'http://localhost:3000/api/member/allow/', {
                'member_id': member_id,
                'taskname': taskname
        }).then((response) => {
            if (response.data['state'] === 'success')
                dispatch(participantAddSuccess());
            else
                dispatch(participantAddFailure(response.data['code']))
        }).catch((error) => {
            console.log(error);
            dispatch(participantAddFailure(error.response.data.code));
        });
    };
}


// add original data type to task
export function addDatatypeRequest(taskname, datatypename, mappingschema) {
    return (dispatch) => {
        // Register API starting
        dispatch(datatypeAdd());

        return axios.post(
            'http://localhost:3000/api/task/allowodt/', {
                'taskname': taskname,
                'datatypename': taskname,
                'mappingschema': mappingschema
        }).then((response) => {
            if (response.data['state'] === 'success')
                dispatch(datatypeAddSuccess());
            else
                dispatch(datatypeAddFailure(response.data['code']))
        }).catch((error) => {
            console.log(error);
            dispatch(datatypeAddFailure(error.response.data.code));
        });
    };
}

//SET PASS VALUE FOR TASK
export function setPassvalRequest(taskname, passval) {
    return (dispatch) => {
        // Register API starting
        dispatch(register(passvalSet()));

        // Request
        return axios.post(
            'http://localhost:3000/task/setpass/', {
                'taskname': taskname,
                'passval': passval
        }).then((response) => {
          if (response.data['state'] === 'success')
                dispatch(passvalSetSuccess());
          else
                dispatch(passvalSetFailure(response.data['code']))

        }).catch((error) => {
            console.log(error);
            dispatch(passvalSetFailure(error.response.data.code));
        });
    };
}



export function manageMain() {
    return {
        type: MANAGE_MAIN
    };
}

export function participantAdd() {
    return {
        type: PARTICIPANT_ADD
    };
}

export function participantAddSuccess() {
    return {
        type: PARTICIPANT_ADD_SUCCESS,
    };
}

export function participantAddFailure(error) {
    return {
        type: PARTICIPANT_ADD_FAILURE,
        error
    };
}

export function datatypeAdd() {
    return {
        type: DATATYPE_ADD
    };
}

export function datatypeAddSuccess() {
    return {
        type: DATATYPE_ADD_SUCCESS,
    };
}

export function datatypeAddFailure(error) {
    return {
        type: DATATYPE_ADD_FAILURE,
        error
    };
}

export function passvalSet() {
    return {
        type: PASSVAL_SET
    };
}

export function passvalSetSuccess() {
    return {
        type: PASSVAL_SET_SUCCESS,
    };
}

export function passvalSetFailure(error) {
    return {
        type: PASSVAL_SET_FAILURE,
        error
    };
}

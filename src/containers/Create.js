import React, { Component } from 'react';
import { CreateTask } from '../components';

// redux
import { connect } from 'react-redux';
import { taskCreateRequest } from '../actions/task';

class Create extends Component {
    handleCreate = (id, password, name, address, gender, phone, birth, role) => {
        return this.props.taskCreateRequest(id, password, name, address, gender, phone, birth, role).then(
            () => {
                if (this.props.status === "SUCCESS") {
                    window.Materialize.toast('태스크 생성이 완료되었습니다.', 2000);
                    this.props.history.push('/admin');
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
                <CreateTask
                    onCreate={this.handleCreate}
                />
            </div>
        );
    }
}

// ==================================================
// can use redux state and thunk like component props
const mapStateToProps = (state) => {
    return {
        status: state.task.submit.status,
        errorMessage: state.task.submit.error
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        taskCreateRequest: (id, password, name, address, gender, phone, birth, role) => {
            return dispatch(taskCreateRequest(id, password, name, address, gender, phone, birth, role));
        }
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Create);
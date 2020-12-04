import React, { Component } from 'react';

import axios from "axios";

import { BrowserRouter as Link } from 'react-router-dom';

class Pop extends Component {
    state = {
        loading: false,
        ItemList: []
    };

    loadData = async () => {
        axios.post("http://localhost:3000/api/task/now/", {
            "taskname": this.props.taskname,
            "submittername": this.props.submittername,
        }).then((response) => {
            this.setState({
                loading: true,
                ItemList: response.data.task_now,
            })
            console.log(this.state);
        }).catch(e => {
            console.error(e);
            this.setState({
                loading: false
            });
        });
    }



    componentDidMount() {
        this.loadData();
    }

    render() {
        const adminView = (
            <div>

                    <div>
                        <nav>
                            <ul>
                                <li>
                                    <Link to="/admin/adminhome">관리자 홈</Link>
                                </li>
                                <li>
                                    <Link to="/admin/taskstatistics/">태스크 통계</Link>
                                </li>
                            </ul>
                        </nav>

                    </div>

                <div className="body">
                    <header>테스크 통계 화면(제출자 검색)</header>

                    <div className="wrapper">
                        <h3>
                            제출자가 참여 중인 테스크
                        </h3>
                        <div className="table">
                            <div className="row2-header">
                                <div className="cell">파일 개수</div>
                            </div>
                            {this.state.ItemList &&
                                this.state.ItemList.map((itemdata) => {
                                    return (
                                        <div className="row2" key={itemdata[1]}>
                                            <div className="cell" data-title="FileCount">{itemdata[1]}</div>
                                        </div>
                                    );
                                })
                            }
                        </div>
                    </div>

                </div>
            </div>
        );

        const nonadminView = (
            <div>{this.state.ItemList}</div>
        );

        return (
            <div className='popup'>
                <div className='popup_inner'>
                    <div className="modal-header">
                        <h3>{id}</h3>
                    </div>
                    <div className="modal-body">
                        {(role === 'A' ? adminView : nonadminView)}
                    </div>
                    <div className="button_round" onClick={this.props.closePopup}>Close</div>
                </div>
            </div>
        );
    }
}

class TaskNow extends Component {
    state = {
        toggle: false,
        id: '',
        role: ''
    };

    togglePop = (taskname, submittername) => {
        this.setState({
            toggle: !this.state.toggle,
            id: id,
            role: role
        });
    };

    render() {
        const { Itemcard } = this.props;
        return (
            <div className="wrapper">
                <div className="table">
                    <div className="row2-header">
                        <div className="cell">taskname</div>
                        <div className="cell">submittername</div>
                    </div>
                    {Itemcard &&
                        Itemcard.map((itemdata5) => {
                            return (
                                <div className="row2" onClick={this.togglePop.bind(this, itemdata5[1])} key={itemdata5[0]}>
                                    <div className="cell" data-title="taskname">{itemdata5[0]}</div>
                                    <div className="cell" data-title="submittername">{itemdata5[1]}</div>
                                </div>
                            );
                        })
                    }
                    {this.state.toggle ? <Pop taskname={this.state.taskname} submittername={this.state.submittername} closePopup={this.togglePop.bind(this)} /> : null}
                </div>
            </div>
        );
    }
}
export default TaskNow;

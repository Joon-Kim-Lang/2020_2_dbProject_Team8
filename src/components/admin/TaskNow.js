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
        return (
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
                    <header>태스크 통계 화면(제출자 검색)</header>
                    <div className="wrapper">
                        <h6>
                            제출자가 참여 중인 태스크
                        </h6>
                        <div className="table">
                            <div className="row2-header">
                                <div className="cell">태스크명</div>
                            </div>
                            {this.state.ItemList &&
                                this.state.ItemList.map((itemdata) => {
                                    return (
                                        <div className="row2" key={itemdata[0]}>
                                            <div className="cell" data-title="FileCount">{itemdata[0]}</div>
                                        </div>
                                    );
                                })
                            }
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

class TaskNow extends Component {
    state = {
        toggle: false,
        submittername: ''
    };

    togglePop = (submittername) => {
        this.setState({
            toggle: !this.state.toggle,
            submittername: submittername
        });
    };

    render() {
        const { Itemcard } = this.props;
        return (
            <div className="wrapper">
                <h6>
                    각 태스크에 참여 중인 제출자들의 목록
                </h6>
                <div className="table">
                    <div className="row2-header">
                        <div className="cell">태스크명</div>
                        <div className="cell">제출자명</div>
                    </div>
                    {Itemcard &&
                        Itemcard.map((itemdata5) => {
                            return (
                                <div className="row2" onClick={this.togglePop.bind(this, itemdata5[2])} key={itemdata5[0]}>
                                    <div className="cell" data-title="taskname">{itemdata5[0]}</div>
                                    <div className="cell" data-title="submittername">{itemdata5[2]}</div>
                                </div>
                            );
                        })
                    }
                    {this.state.toggle ? <Pop submittername={this.state.submittername} closePopup={this.togglePop.bind(this)} /> : null}
                </div>
            </div>
        );
    }
}
export default TaskNow;
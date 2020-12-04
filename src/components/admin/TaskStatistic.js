import React, { Component } from 'react';

import axios from "axios";

import TaskNow from "./TaskNow";

import { BrowserRouter as Link } from 'react-router-dom';


class TaskStatistic extends Component {
    state = {
        loading: false,
        ItemList: [],
        ItemList1: [],
        ItemList2: [],
        ItemList3: [],
        ItemList4: [],
        ItemList5: []
    };

    loadData = async () => {

        axios.post("http://localhost:3000/api/task/statistics/", {

        }).then((response) => {
            this.setState({
                loading: true,
                ItemList1: response.data.file_task,
                ItemList2: response.data.tuple_task,
                ItemList3: response.data.file_original,
                ItemList4: response.data.tuple_original,
                ItemList5: response.data.submitter_now
            })
            console.log(this.state);
        }).catch(e => {
            console.error(e);
            this.setState({
                loading: false
            });
        });

        this.setState({
            loading: true,
            ItemList: ['Admin info is not visible']
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
                        </ul>
                    </nav>
                </div>

                <div className="body body-s">
                    <div action="" className="sky-form">

                        <header>태스크 통계 화면</header>

                        <div className="wrapper">
                            <h6>
                                각 태스크 별로 전체 제출된 파일 수
                            </h6>
                            <div className="table">

                                <div className="row2-header">

                                    <div className="cell">태스크명</div>
                                    <div className="cell">파일 개수</div>
                                </div>
                                {this.state.ItemList1 &&
                                    this.state.ItemList1.map((itemdata1) => {
                                        return (
                                            <div className="row2" key={itemdata1[0]}>
                                                <div className="cell" data-title="TaskName">{itemdata1[0]}</div>
                                                <div className="cell" data-title="FileCount">{itemdata1[1]}</div>
                                            </div>
                                        );
                                    })
                                }
                            </div>
                        </div>

                        <div className="wrapper">
                            <h6>
                                각 태스크별로 pass되어 테스크 데이터 테이블에 저장된 tupel 수
                            </h6>
                            <div className="table">
                                <div className="row2-header">
                                    <div className="cell">태스크명</div>
                                    <div className="cell">tuple 수</div>
                                </div>
                                {this.state.ItemList2 &&
                                    this.state.ItemList2.map((itemdata2) => {
                                        return (
                                            <div className="row2" key={itemdata2[0]}>
                                                <div className="cell" data-title="TaskName">{itemdata2[0]}</div>
                                                <div className="cell" data-title="TupleCount">{itemdata2[1]}</div>
                                            </div>
                                        );
                                    })
                                }
                            </div>
                        </div>

                        <div className="wrapper">
                            <h6>
                                각 원본 데이터 타입별로 전체 제출된 파일 수
                            </h6>
                            <div className="table">
                                <div className="row2-header">
                                    <div className="cell">원본 데이터 타입명</div>
                                    <div className="cell">파일 개수</div>
                                </div>
                                {this.state.ItemList1 &&
                                    this.state.ItemList3.map((itemdata3) => {
                                        return (
                                            <div className="row2" key={itemdata3[0]}>
                                                <div className="cell" data-title="ODTName">{itemdata3[0]}</div>
                                                <div className="cell" data-title="FileCount">{itemdata3[1]}</div>
                                            </div>
                                        );
                                    })
                                }
                            </div>
                        </div>

                        <div className="wrapper">
                            <h6>
                                각 원본 데이터 타입별로 pass되어 태스크 데이터 테이블에 저장된 tuple 수
                            </h6>
                            <div className="table">
                                <div className="row2-header">
                                    <div className="cell">원본 데이터 타입명</div>
                                    <div className="cell">tuple 수</div>
                                </div>
                                {this.state.ItemList4 &&
                                    this.state.ItemList4.map((itemdata4) => {
                                        return (
                                            <div className="row2" key={itemdata4[0]}>
                                                <div className="cell" data-title="ODTName">{itemdata4[0]}</div>
                                                <div className="cell" data-title="TupleCount">{itemdata4[1]}</div>
                                            </div>
                                        );
                                    })
                                }
                            </div>
                        </div>

                        <TaskNow Itemcard={this.state.ItemList5} />
                    </div>
                </div>
            </div>
        );
    }
}


export default TaskStatistic;
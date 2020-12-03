import React, { Component } from 'react';

import axios from "axios";


import { BrowserRouter as Link} from 'react-router-dom'


class AdminHome extends Component {
    state = {
        loading: false
    };

    loadData = async () => {
        axios.post("http://localhost:3000/api/adminmain/", {
            "taskname": this.props.taskname,
            "submittername": this.props.submittername,
        }).then((response) => {
            this.setState({
                loading: true
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
            <div className="body body-s">
                <div action="" className="sky-form">
                    <header>관리자 메인 화면</header>

                    <fieldset>
                        <h3>
                            어느 기능을 사용하고 싶습니까?
                        </h3>
                        <div>
                            <nav>
                                <ul>
                                    <li>
                                        <Link to="/admin/createtask/">태스크 생성</Link>
                                    </li>
                                    <li>
                                        <Link to="/admin/managetask/">태스크 관리</Link>
                                    </li>
                                    <li>
                                        <Link to="/admin/taskstatistics/">태스크 통계</Link>
                                    </li>
                                    <li>
                                        <Link to="/admin/user/">맴버 관리 및 통계</Link>
                                    </li>
                                </ul>
                            </nav>
                        </div>
                    </fieldset>
                </div>
            </div>
        );
    }
}

export default AdminHome;
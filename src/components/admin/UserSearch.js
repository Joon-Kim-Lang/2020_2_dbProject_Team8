import React, { Component } from "react";
import axios from "axios";
import { BrowserRouter as Link } from 'react-router-dom';

class Popup extends Component {
    state = {
        loading: false,
        ItemList: []
    };

    loadData = async () => {
        if (this.props.id === "admin") {
            this.setState({
                loading: true,
                ItemList: ['Admin info is not visible']
            });
        }
        else {
            axios.post("http://localhost:3000/api/member/info/", {
                "userid": this.props.id,
                "role": this.props.role,
            }).then((response) => {
                this.setState({
                    loading: true,
                    ItemList: response.data.result
                })
                console.log(this.state);
            }).catch(e => {
                console.error(e);
                this.setState({
                    loading: false
                });
            });
        }
    }

    componentDidMount() {
        this.loadData();
    }

    render() {
        const { id, role } = this.props;

        const adminView = (
            <div>{this.state.ItemList}</div>
        );

        const submitterView = (
            <div>
                <div>
                    <nav>
                        <ul>
                            <li>
                                <Link to="/admin/">관리자 홈</Link>
                            </li>
                            <li>
                                <Link to="/admin/user/">맴버 관리 및 통계</Link>
                            </li>
                        </ul>
                    </nav>
                </div>
                <div className="wrapper">
                    <div className="table">
                        <div className="row2-header">
                            <div className="cell">TaskID</div>
                            <div className="cell">DataID</div>
                            <div className="cell">Order</div>
                            <div className="cell">FileName</div>
                            <div className="cell">P/NP</div>
                            <div className="cell">Score</div>
                        </div>
                        {this.state.ItemList &&
                            this.state.ItemList.map((itemdata) => {
                                return (
                                    <div className="row2" key={itemdata[1]}>
                                        <div className="cell" data-title="TaskID">{itemdata[0]}</div>
                                        <div className="cell" data-title="DataID">{itemdata[1]}</div>
                                        <div className="cell" data-title="Order">{itemdata[2]}</div>
                                        <div className="cell" data-title="FileName">{itemdata[3]}</div>
                                        <div className="cell" data-title="P/NP">{itemdata[4]}</div>
                                        <div className="cell" data-title="Score">{itemdata[5]}</div>
                                    </div>
                                );
                            })
                        }
                    </div>
                </div>
            </div>
        );

        const evaluatorView = (
            <div>
                <div>
                    <nav>
                        <ul>
                            <li>
                                <Link to="/admin/">관리자 홈</Link>
                            </li>
                            <li>
                                <Link to="/admin/user/">맴버 관리 및 통계</Link>
                            </li>
                        </ul>
                    </nav>
                </div>
                <div className="wrapper">
                    <div className="table">
                        <div className="row2-header">
                            <div className="cell">ID</div>
                            <div className="cell">FileName</div>
                            <div className="cell">P/NP</div>
                            <div className="cell">Total tuple</div>
                            <div className="cell">Dup tuple</div>
                            <div className="cell">Null ratio</div>
                            <div className="cell">Quality</div>
                            <div className="cell">Score</div>
                            <div className="cell">Eval ID</div>
                        </div>
                        {this.state.ItemList &&
                            this.state.ItemList.map((itemdata) => {
                                return (
                                    <div className="row2" key={itemdata[0]}>
                                        <div className="cell" data-title="ID">{itemdata[0]}</div>
                                        <div className="cell" data-title="FileName">{itemdata[1]}</div>
                                        <div className="cell" data-title="P/NP">{itemdata[2]}</div>
                                        <div className="cell" data-title="Total tuple">{itemdata[3]}</div>
                                        <div className="cell" data-title="Dup tuple">{itemdata[4]}</div>
                                        <div className="cell" data-title="Null Ratio">{itemdata[5]}</div>
                                        <div className="cell" data-title="Quality">{itemdata[6]}</div>
                                        <div className="cell" data-title="Score">{itemdata[7]}</div>
                                        <div className="cell" data-title="Eval ID">{itemdata[8]}</div>
                                    </div>
                                );
                            })
                        }
                    </div>
                </div>
            </div>
        );

        return (
            <div className='popup'>
                <div className='popup_inner'>
                    <div className="modal-header">
                        <h3>{id}</h3>
                    </div>
                    <div className="modal-body">
                        {(role === 'A') ? adminView
                            : (role === 'S' ? submitterView : evaluatorView)
                        }
                    </div>
                    <div className="button_round" onClick={this.props.closePopup}>Close</div>
                </div>
            </div>
        );
    }
}

class UserSearch extends Component {
    state = {
        toggle: false,
        id: '',
        role: ''
    };

    togglePop = (id, role) => {
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
                        <div className="cell">ID</div>
                        <div className="cell">Gender</div>
                        <div className="cell">Age</div>
                        <div className="cell">Role</div>
                    </div>
                    {Itemcard &&
                        Itemcard.map((itemdata) => {
                            return (
                                <div className="row2" onClick={this.togglePop.bind(this, itemdata[0], itemdata[3])} key={itemdata[0]}>
                                    <div className="cell" data-title="id">{itemdata[0]}</div>
                                    <div className="cell" data-title="gender">{itemdata[1]}</div>
                                    <div className="cell" data-title="age">{itemdata[2]}</div>
                                    <div className="cell" data-title="role">{itemdata[3]}</div>
                                </div>
                            );
                        })
                    }
                    {this.state.toggle ? <Popup id={this.state.id} role={this.state.role} closePopup={this.togglePop.bind(this)} /> : null}
                </div>
            </div>
        );
    }
}

export default UserSearch;
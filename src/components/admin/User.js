import React, { Component } from 'react';

import axios from "axios";

import UserSearch from "./UserSearch";

import { BrowserRouter as Link } from 'react-router-dom';


class User extends Component {
    state = {
        loading: false,
        userid: '',
        gender: '',
        ageFrom: '',
        ageTo: '',
        role: '',
        task: '',
        ItemList: []
    };

    loadData = async () => {
        axios.post("http://localhost:3000/api/member/search/", {
            "userid": this.state.userid,
            "gender": this.state.gender,
            "ageFrom": this.state.ageFrom,
            "ageTo": this.state.ageTo,
            "role": this.state.role,
            "task": this.state.task
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

    handleChange = (e) => {
        let nextState = {};
        nextState[e.target.name] = e.target.value;
        this.setState(nextState);
    }

    handleSearch = () => {
        this.loadData();
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

                        <fieldset>
                            <div className="row">
                                <div className="column">
                                    <section className="col col-6">
                                        <label className="label">ID</label>
                                        <label className="input">
                                            <input name="userid" type="text" placeholder="ID"
                                                onChange={this.handleChange} value={this.state.userid}
                                            />
                                        </label>
                                    </section>
                                </div>
                                <div className="column">
                                    <section className="col col-3">
                                        <label className="label">Age From</label>
                                        <label className="input">
                                            <input name="ageFrom" type="number" placeholder="Age ~"
                                                min="01" max="99"
                                                onChange={this.handleChange} value={this.state.ageFrom}
                                            />
                                        </label>
                                    </section>
                                </div>
                                <div className="column">
                                    <section className="col col-3">
                                        <label className="label">Age To</label>
                                        <label className="input">
                                            <input name="ageTo" type="number" placeholder="~ Age"
                                                min="01" max="99"
                                                onChange={this.handleChange} value={this.state.ageTo}
                                            />
                                        </label>
                                    </section>
                                </div>
                            </div>

                            <div className="row">
                                <div className="column">
                                    <section className="col col-6">
                                        <label className="label">Task ID</label>
                                        <label className="input">
                                            <input name="task" type="number" placeholder="Task ID"
                                                onChange={this.handleChange} value={this.state.task}
                                            />
                                        </label>
                                    </section>
                                </div>
                                <div className="column">
                                    <section className="col col-3">
                                        <label className="label">Gender</label>
                                        <label className="select">
                                            <select name="gender" onChange={this.handleChange} value={this.state.gender}>
                                                <option value="">Gender</option>
                                                <option value="M">Men</option>
                                                <option value="W">Women</option>
                                            </select>
                                            <i></i>
                                        </label>
                                    </section>
                                </div>
                                <div className="column">
                                    <section className="col col-3">
                                        <label className="label">Role</label>
                                        <label className="select">
                                            <select name="role" onChange={this.handleChange} value={this.state.role}>
                                                <option value="">Role</option>
                                                <option value="S">Submitter</option>
                                                <option value="E">Evaluater</option>
                                            </select>
                                            <i></i>
                                        </label>
                                    </section>
                                </div>
                            </div>
                        </fieldset>

                        <footer>
                            <button onClick={this.handleSearch} className="button">Search</button>
                        </footer>
                    </div>

                    <UserSearch Itemcard={this.state.ItemList} />

                </div>
            </div>
        );
    }
}

export default User;
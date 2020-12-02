import React, { Component } from 'react';
import PropTypes from 'prop-types';

import '../style.css';
 
class Authentication extends Component {
    state = {
        id: "",
        password: "",
        name: "",
        address: "",
        gender: "M",
        phone: "",
        year: "2000",
        month: "01",
        day: "01",
        role: "S"
    }

    handleChange = (e) => {
        let nextState = {};
        nextState[e.target.name] = e.target.value;
        this.setState(nextState);
    }

    handleRegister = () => {
        let id = this.state.id;
        let password = this.state.password;
        let name = this.state.name;
        let address = this.state.address;
        let gender = this.state.gender;
        let phone = this.state.phone;
        let birth = this.state.year + "-" + this.state.month + "-" + this.state.day;
        let role = this.state.role;

        this.props.onRegister(id, password, name, address, gender, phone, birth, role).then(
            (result) => {
                if (!result) {
                    this.setState({
                        id: "",
                        password: "",
                        name: "",
                        address: "",
                        gender: "M",
                        phone: "",
                        year: "2000",
                        month: "01",
                        day: "01",
                        role: "S"
                    })
                }
            }
        )
    }

    render() {

        const loginView = (
            <fieldset>
                <section>
                    <label className="input">
                        <label className="label">ID</label>
                        <input name="id" type="text" placeholder="user ID"
                            onChange={this.handleChange} value={this.state.id}
                        />
                    </label>
                </section>
                
                <section>
                    <label className="input">
                        <label className="label">Password</label>
                        <input name="password" type="password" placeholder="user password"
                            onChange={this.handleChange} value={this.state.password}
                        />
                    </label>
                </section>

                <p className="message">Not registered? <a href="/register">Create an account</a></p>
            </fieldset>
        );
 
        const registerView = (
            <fieldset>					
                <section>
                    <label className="input">
                        <label className="label">ID</label>
                        <input name="id" type="text" placeholder="user ID"
                            onChange={this.handleChange} value={this.state.id}
                        />
                    </label>
                </section>
                
                <section>
                    <label className="input">
                        <label className="label">Password</label>
                        <input name="password" type="password" placeholder="user password"
                            onChange={this.handleChange} value={this.state.password}
                        />
                    </label>
                </section>

                <section>
                    <label className="input">
                        <label className="label">Name</label>
                        <input name="name" type="text" placeholder="Name"
                            onChange={this.handleChange} value={this.state.name}
                        />
                    </label>
                </section>

                <section>
                    <label className="input">
                        <label className="label">Address</label>
                        <input name="address" type="text" placeholder="Address"
                            onChange={this.handleChange} value={this.state.address}
                        />
                    </label>
                </section>

                <section>
                    <label className="label">Gender</label>
                    <section>
                        <label className="select">
                            <select name="gender" onChange={this.handleChange} value={this.state.gender}>
                                <option value="M">Male</option>
                                <option value="W">Female</option>
                            </select>
                            <i></i>
                        </label>
                    </section>
                </section>

                <section>
                    <label className="input">
                        <label className="label">Phone</label>
                        <input name="phone" type="text" placeholder="Phone (Please enter without '-')"
                            onChange={this.handleChange} value={this.state.phone}
                        />
                    </label>
                </section>

                <label className="label">Birth</label>
                <div className="row">
                    <section className="col col-4">
                        <label className="input">
                            <input name="year" type="number" placeholder="Year"
                                min="1900" max="2020"
                                onChange={this.handleChange} value={this.state.year}
                            />
                        </label>
                    </section>
                    <section className="col col-4">
                        <label className="input">
                            <input name="month" type="number" placeholder="Month"
                                min="01" max="12"
                                onChange={this.handleChange} value={this.state.month}
                            />
                        </label>
                    </section>
                    <section className="col col-4">
                        <label className="input">
                            <input name="day" type="number" placeholder="Day"
                                min="01" max="31"
                                onChange={this.handleChange} value={this.state.day}
                            />
                        </label>
                    </section>
                </div>

                <section>
                    <label className="label">Role</label>
                    <section>
                        <label className="select">
                            <select name="role" onChange={this.handleChange} value={this.state.role}>
                                <option value="S">Submitter</option>
                                <option value="E">Evaluater</option>
                            </select>
                            <i></i>
                        </label>
                    </section>
                </section>

                <p className="message">Already registered? <a href="/login">Sign In</a></p>
            </fieldset>
        );

        const loginBtn = (
            <footer>
                <button className="button">Login</button>
            </footer>
        );

        const registerBtn = (
            <footer>
                <button onClick={this.handleRegister} className="button">Register</button>
            </footer>
        );


        return (
            <div className="body">
                <div action="" className="sky-form">
                    <header>
                        {this.props.mode ? "LOGIN" : "REGISTER"}
                    </header>
                    {this.props.mode ? loginView : registerView }
                    {this.props.mode ? loginBtn : registerBtn}
                </div>
            </div>
        );
    }
}
 
Authentication.propTypes = {
    mode: PropTypes.bool,
    onRegister: PropTypes.func
};
 
Authentication.defaultProps = {
    mode: true,
    onRegister: (id, password, name, address, gender, phone, birth, role) => { console.error("register function not defined"); }
};
 
export default Authentication;
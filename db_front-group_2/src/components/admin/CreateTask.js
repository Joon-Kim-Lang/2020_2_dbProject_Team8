import React, { Component } from 'react';
import PropTypes from 'prop-types';

import '../../style.css'
 
class CreateTask extends Component {
	state = {
		taskname: "",
		description: "",
		hour: "",
		min: "",
		sec: "",
		tdtname: "",
		tdtschema: ""
	}

	handleChange = (e) => {
        let nextState = {};
        nextState[e.target.name] = e.target.value;
        this.setState(nextState);
	}
	
	handleSubmit = () => {
		let minuploadcycle = this.state.hour + ":" + this.state.min + ":" + this.state.sec;

		this.props.onCreate(
			this.state.taskname, this.state.description, minuploadcycle,
			this.state.tdtname, this.state.tdtschema
		)
	}

    render() {
        return (
            <div className="body body-s">
            
                <div action="" className="sky-form">
				<header>Create New Task</header>
				
				<fieldset>					
					<section>
						<label className="input">
                            <label className="label">Task Name</label>
							<input name="taskname" type="text" placeholder="Task name"
								onChange={this.handleChange} value={this.state.taskname}
							/>
							<b className="tooltip tooltip-bottom-right">Only latin characters and numbers</b>
						</label>
					</section>
					
					<section>
						<label className="input">
                            <label className="label">Description</label>
							<label className="textarea">
                                <i className="icon-append icon-comment"></i>
                                <textarea name="description" rows="4"
									onChange={this.handleChange} value={this.state.description}
								></textarea>
                            </label>
							<b className="tooltip tooltip-bottom-right">Needed to verify your account</b>
						</label>
					</section>

                    <label className="label">Minimum Upload Cycle</label>
                    <div className="row">
						<section className="col col-4">
							<label className="input">
								<input name="hour" type="text" placeholder="Hour"
									onChange={this.handleChange} value={this.state.hour}
								/>
							</label>
						</section>
						<section className="col col-4">
							<label className="input">
								<input name="min" type="text" placeholder="Minute"
									onChange={this.handleChange} value={this.state.min}
								/>
							</label>
						</section>
                        <section className="col col-4">
							<label className="input">
								<input name="sec" type="text" placeholder="Second"
									onChange={this.handleChange} value={this.state.sec}
								/>
							</label>
						</section>
					</div>
					
					<section>
                        <label className="label">Task Data Table Name</label>
						<label className="input">
							<input name="tdtname" type="text" placeholder="Task Data Table Name"
								onChange={this.handleChange} value={this.state.tdtname}
							/>
							<b className="tooltip tooltip-bottom-right">Only latin characters and numbers</b>
						</label>
					</section>
					
					<section>
                        <label className="label">Task Data Table Schema</label>
						<label className="input">
                            <label className="textarea">
                                <i className="icon-append icon-comment"></i>
                                <textarea name="tdtschema" rows="4"
									onChange={this.handleChange} value={this.state.tdtschema}
								></textarea>
                            </label>
							<b className="tooltip tooltip-bottom-right">Only latin characters and numbers</b>
						</label>
					</section>
				</fieldset>
					
				<footer>
					<button onClick={this.handleSubmit} className="button">Submit</button>
				</footer>
			</div>
			
		    </div>
        );
    }
}

CreateTask.propTypes = {
    onCreate: PropTypes.func
};
 
CreateTask.defaultProps = {
    onCreate: (id, password) => { console.error("create function not defined"); }
};
 
export default CreateTask;
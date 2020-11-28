import React from 'react';
import ReactDOM from 'react-dom';

import './style.css';

// Routing
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { Register, Login, Create, App } from './containers';
import { AdminHome, ManageTask, TaskStatistic, User } from './components';

// Redux
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import reducers from './reducers';
import thunk from 'redux-thunk';

const store = createStore(reducers, applyMiddleware(thunk));

ReactDOM.render(
  <Provider store={store}>
    <Router>
      <div>
        <Route path="/" component={App}/>

        <Route path="/register" component={Register}/>
        <Route path="/login" component={Login}/>

        <Route path="/admin" exact={true} component={AdminHome} />
        <Route path="/admin/createtask" component={Create} />
        <Route path="/admin/managetask" component={ManageTask} />
        <Route path="/admin/taskstatistic" component={TaskStatistic} />
        <Route path="/admin/user" component={User} />
      </div>
    </Router>
  </Provider>
  ,
  document.getElementById('root')
);

module.hot.accept();
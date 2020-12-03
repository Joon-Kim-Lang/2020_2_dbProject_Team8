/*
    file for combining all reducers from this project.
*/

import { combineReducers } from 'redux';

import authentication from './authentication';
import task from './task';
import manage from './manage'

export default combineReducers({
    authentication, task, manage
});
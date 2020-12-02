import React, { Component } from 'react';

import { BrowserRouter as Link } from 'react-router-dom';


class ManageTask extends Component {
    render() {
        return (
            <div>
                <text>ManageTask page</text>
                <div>
                    <nav>
                        <ul>
                            <li>
                                <Link to="/admin/adminhome">관리자 홈</Link>
                            </li>
                        </ul>
                    </nav>
                </div>
            </div>
        );
    }
}

export default ManageTask;
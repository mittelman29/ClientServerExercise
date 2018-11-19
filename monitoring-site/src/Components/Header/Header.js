import React, { Component } from 'react';
import { Row } from 'react-bootstrap';
import './Header.css';

class Header extends Component {
    constructor(){
        super();


    }


    render() {
        return (
            <Row className="header">
                <h2>Monitoring Site</h2>
            </Row>
        );
    }
}

export default Header;
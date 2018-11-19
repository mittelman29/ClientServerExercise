import React, { Component } from 'react';
import { Col } from 'react-bootstrap';
import './Item.css';

const classNames = require('classnames');
const testJSON = {"jojo": "funny", "amy": "kind", "mike": "fun", "isaiah": "hilarity"}

class Item extends Component {
    constructor(props){
        super(props);

        this.showHide = this.showHide.bind(this);
        this.delete = this.delete.bind(this);

        this.state = {
            showValue: false
        }
    }

    showHide = () => {
        this.setState({ showValue: !this.state.showValue })
    }

    delete = (key) => {
        this.props.delete(key)
    }
    
    render() {
        let valueClass=classNames('value', {'value-closed': !this.state.showValue, 'value-open': this.state.showValue});
        let linkClass=classNames('fa', {'fa-eye': !this.state.showValue, 'fa-eye-slash':this.state.showValue});
        
        return (
            <Col xs={6} sm={4} md={3} className="item">
                <div className="content">
                    <div className="action-row">
                        <i className="fa fa-times delete" onClick={() => this.delete(this.props.itemKey)}></i>
                    </div>
                    <h3>{this.props.itemKey}</h3>
                    <div className="value-row">
                        <div className={valueClass}>
                            <span>{this.props.itemValue}</span>
                        </div>
                    </div>
                    <div className="show-hide">
                        <span className="show-hide-link" onClick={this.showHide}><i className={linkClass}></i> { this.state.showValue ? 'hide' : 'show' }</span>
                    </div>
                </div>
            </Col>
        );
    }
}

export default Item;
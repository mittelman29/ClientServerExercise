import React, { Component } from 'react';
import { Row, Col, Form, FormGroup, FormControl, ControlLabel, Button } from 'react-bootstrap';
import Item from '../Item/Item';
import './ItemList.css';

const axios = require('axios');

class ItemList extends Component {
    constructor(props){
        super(props);

        this.delete = this.delete.bind(this)
        this.handleChange = this.handleChange.bind(this)
        this.submitNew = this.submitNew.bind(this)

        this.state = {
            data: [],
            newKey: '',
            newVal: ''
        }
    }

    componentWillMount(){
        axios.get(
            'http://localhost:11211/'
        ).then( (response) => {
            console.log("RESPONSE: ",response);
            this.setState({ data: response.data })
        }).catch( (error) => {
            console.log("ERROR: ",error);
        });
    }

    delete = (key) => {
        if( window.confirm("Would you really like to delete the key: " + key) ){
            axios.delete(
                'http://localhost:11211/del/' + key
            ).then( (response) => {
                console.log("RESPONSE: ",response);
                this.setState({ data: response.data })
            }).catch( (error) => {
                console.log("ERROR: ",error);
            });
        }
    }

    handleChange = (e) => {
        var state = this.state;
        
        state[e.target.name] = e.target.value;

        this.setState(state);
    }

    submitNew = () => {
        axios.post(
            'http://localhost:11211/set?' + this.state.newKey + '=' + this.state.newVal
        ).then( (response) => {
            console.log("RESPONSE: ",response);
            this.setState({ data: response.data, newKey: '', newVal: '' })
        }).catch( (error) => {
            console.log("ERROR: ",error);
        });
    }

    render() {
        return (
            <Row>
            {
                Object.keys(this.state.data).map( (key) => {
                    return <Item key={key} itemKey={key} itemValue={this.state.data[key]} delete={this.delete} />
                })
            }
                <Col xs={12}>
                    <Form inline>

                        <FormGroup>
                            <ControlLabel>Key</ControlLabel>
                            <FormControl 
                                componentClass="input"
                                value={this.state.newKey}
                                name='newKey'
                                className='new-item-form-input'
                                placeholder="Enter Key"
                                onChange={(e) => this.handleChange(e)}
                            />
                        </FormGroup>

                        <FormGroup>
                            <ControlLabel>Value</ControlLabel>
                            <FormControl 
                                componentClass="input"
                                value={this.state.newVal}
                                name='newVal'
                                className='new-item-form-input'
                                placeholder="Enter Value"
                                onChange={(e) => this.handleChange(e)}
                            />
                        </FormGroup>

                        <FormGroup>
                            <Button onClick={this.submitNew} disabled={!this.state.newKey || !this.state.newVal}>Submit</Button>
                        </FormGroup>
                        
                    </Form>
                </Col>
            </Row>
        );
    }
}

export default ItemList;
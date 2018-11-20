import React, { Component } from 'react';
import { Grid } from 'react-bootstrap';
import Header from '../Header/Header';
import ItemList from '../ItemList/ItemList';
import './Home.css';

class Home extends Component {

    render() {
        return (
            <Grid>
                <Header />
                <ItemList />
            </Grid>
        );
    }
    
}

export default Home;
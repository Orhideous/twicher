require('./styles/index.styl');

import React from 'react';
import ReactDOM from 'react-dom';

import {List} from './app/components.jsx';

const quotes = [
  {id: 1, excerpt: 'First', text: 'First quote'},
  {id: 2, excerpt: 'Second', text: 'Second quote'},
];


ReactDOM.render(
    <List quotes={quotes}/>,
    document.getElementById('list')
);

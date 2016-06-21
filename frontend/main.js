require('./styles/index.styl');

import Rx from 'rx';
import React from 'react';
import ReactDOM from 'react-dom';

import {List} from './app/components.jsx';
import {init_bus} from './app/logic';

const bus = new Rx.Subject();

ReactDOM.render(
    <List bus={bus}/>,
    document.getElementById('list')
);

init_bus(bus);

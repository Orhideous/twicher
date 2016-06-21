require('./styles/index.styl');

import Rx from 'rx';
import React from 'react';
import ReactDOM from 'react-dom';

import {List, Editor} from './app/components.jsx';
import {init_bus} from './app/logic';

const bus = new Rx.Subject();

ReactDOM.render(
    <List bus={bus}/>,
    document.getElementById('list')
);
ReactDOM.render(
    <Editor bus={bus}/>,
    document.getElementById('editor')
);

init_bus(bus);

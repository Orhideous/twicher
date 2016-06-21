//noinspection JSUnresolvedVariable
import _ from 'lodash';
import React from "react";
import classNames from 'classnames';

import ReactQuill from 'react-quill';

import {send, SIGNALS} from "./logic";


class Quote extends React.Component {
    constructor(props) {
        super(props);
        this.state = {selected: false};
    }

    componentDidMount() {
        this.props.bus
            .filter(
                ({tell}) => {
                    return tell == SIGNALS.QUOTE_LOADED
                }
            )
            .subscribe(
                ({data}) => {
                    this.setState({
                        selected: data.id == this.props.quote.id
                    });
                }
            )
    }

    render() {
        //noinspection JSUnresolvedVariable,JSUnresolvedVariable
        return (
            <div
                className={classNames("list-group-item", {active: this.state.selected})}
                onClick={
                    () => send(
                        this.props.bus,
                        SIGNALS.QUOTE_SELECTED,
                        {id: this.props.quote.id}
                    )
                }
            >
                <p className="list-group-item-text">
                    <span className="badge badge-id">
                        {this.props.quote.id}
					</span>
                   {this.props.quote.snippet}
                </p>
            </div>
        )
    }
}

export class List extends React.Component {
    constructor(props) {
        super(props);
        this.state = {quotes: []};
        // Load quotes on signal
        this.props.bus
            .filter(
                ({tell}) => {
                    return tell == SIGNALS.QUOTES_FETCHED
                }
            )
            .subscribe(
                ({data}) => {
                    this.setState({quotes: data})
                }
            )
    }

    render() {
        return (
            <div className="cite-list list-group">
                 {_.map(
                     this.state.quotes,
                     (quote) => <Quote
                         key={quote.id}
                         quote={quote}
                         bus={this.props.bus}
                     />
                 )}
            </div>
        )
    }
}


var defaultContent = (
    '<div><span style="font-size: 18px;">Quill Rich Text Editor</span>' +
    '</div><div><br></div><div>Quill is a free, <a href="https://githu' +
    'b.com/quilljs/quill/">open source</a> WYSIWYG editor built for th' +
    'e modern web. With its <a href="http://quilljs.com/docs/modules/"' +
    '>extensible architecture</a> and a <a href="http://quilljs.com/do' +
    'cs/api/">expressive API</a> you can completely customize it to fu' +
    'lfill your needs. Some built in features include:</div><div><br><' +
    '/div><ul><li>Fast and lightweight</li><li>Semantic markup</li><li' +
    '>Standardized HTML between browsers</li><li>Cross browser support' +
    ' including Chrome, Firefox, Safari, and IE 9+</li></ul><div><br><' +
    '/div><div><span style="font-size: 18px;">Downloads</span></div><d' +
    'iv><br></div><ul><li><a href="https://quilljs.com">Quill.js</a>, ' +
    'the free, open source WYSIWYG editor</li><li><a href="https://zen' +
    'oamaro.github.io/react-quill">React-quill</a>, a React component ' +
    'that wraps Quill.js</li></ul>'
);


const toolbarItems = [

    {
        label: 'Text',
        type: 'group',
        items: [
            {type: 'bold', label: 'Bold'},
            {type: 'italic', label: 'Italic'},
            {type: 'strike', label: 'Strike'},
            {type: 'underline', label: 'Underline'},
            {type: 'separator'},
            {type: 'link', label: 'Link'},
            {type: 'image', label: 'Image'},
        ]
    },

    {
        label: 'Blocks',
        type: 'group',
        items: [
            {type: 'bullet', label: 'Bullet'},
            {type: 'separator'},
            {type: 'list', label: 'List'},
            {type: 'separator'},
            {
                label: 'Alignment',
                type: 'align',
                items: [
                    {label: '', value: 'left', selected: true},
                    {label: '', value: 'center'},
                    {label: '', value: 'right'},
                    {label: '', value: 'justify'}
                ]

            }
        ]
    },
];

/*
 A simple editor component, with a real-time preview
 of the generated HTML content.
 */
export class Editor extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: defaultContent
        };
    }

    onEditorChange(value) {
        this.setState({value: value});
    }

    render() {
        return (
            <div>
                <ReactQuill
                    className="editor"
                    theme="snow"
                    toolbar={toolbarItems}
                    value={this.state.value}
                    onChange={this.onEditorChange.bind(this)}
                />
            </div>
        )
    }

}

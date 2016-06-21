import _ from 'lodash';
import React from "react";
import classNames from 'classnames';

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
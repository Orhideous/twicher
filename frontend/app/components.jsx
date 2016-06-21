import _ from 'lodash';
import React from "react";
import {SIGNALS} from "./logic";


class Quote extends React.Component {
    render() {
        return (
            <div className="list-group-item">
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
                    return tell == SIGNALS.QUOTES_LOADED
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
                 {_.map(this.state.quotes, (quote) => <Quote key={quote.id} quote={quote}/>)}
            </div>
        )
    }
}
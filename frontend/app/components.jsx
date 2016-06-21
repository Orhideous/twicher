import _ from 'lodash';
import React from "react";


class Quote extends React.Component {
    render() {
        return (
            <div className="list-group-item">
					<span className="badge">
						{/*<input type="checkbox" checked={false}>*/}
					</span>
                <p className="list-group-item-text">{this.props.quote.text}</p>
            </div>
        )
    }
}

export class List extends React.Component {
    render() {
        return (
            <div className="cite-list list-group">
                {_.map(this.props.quotes, (quote) => <Quote quote={quote}/>)}
            </div>
        )
    }
}
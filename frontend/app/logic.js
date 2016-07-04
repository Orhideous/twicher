import xhr from 'xhr';

export const SIGNALS = {
    QUOTES_FETCHED: "QUOTES_FETCHED",
    QUOTE_SELECTED: "QUOTE_SELECTED",
    QUOTE_LOADED: "QUOTE_LOADED",
    QUOTE_SAVE: "QUOTE_SAVE",
};

export function send(bus, tell, data) {
    bus.onNext({tell, data});
}

export function init_bus(bus) {
    xhr.get(
        '/quotes',
        (err, resp) => send(bus, SIGNALS.QUOTES_FETCHED, JSON.parse(resp.body))
    );

    bus
        .filter(
            ({tell}) => {
                return tell == SIGNALS.QUOTE_SELECTED
            }
        )
        .subscribe(
            ({data}) => {
                xhr.get(
                    '/quotes/' + data.id,
                    (err, resp) => send(bus, SIGNALS.QUOTE_LOADED, JSON.parse(resp.body))
                );
            }
        );
    bus
        .filter(
            ({tell}) => {
                return tell == SIGNALS.QUOTE_SAVE
            }
        )
        .subscribe(
            ({data:{id, text}}) => {
                xhr.post(
                    `/quotes/${id}`,
                    {json: {text}},
                    (err, resp) => send(bus, SIGNALS.QUOTE_LOADED, JSON.parse(resp.body))
                );
            }
        )
}
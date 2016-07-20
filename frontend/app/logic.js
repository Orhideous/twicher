import xhr from 'xhr';

export const SIGNALS = {
    QUOTES_FETCHED: "QUOTES_FETCHED",
    QUOTE_SELECTED: "QUOTE_SELECTED",
    QUOTE_LOADED: "QUOTE_LOADED",
    QUOTE_SAVE: "QUOTE_SAVE",
    QUOTE_ADD: "QUOTE_ADD",
};

export function send(bus, tell, data) {
    bus.onNext({tell, data});
}

export function fetchQuotes(bus) {
    xhr.get(
        '/quotes',
        (err, resp) => send(bus, SIGNALS.QUOTES_FETCHED, JSON.parse(resp.body))
    );
}

export function init_bus(bus) {
    fetchQuotes(bus);

    bus
        .filter(
            ({tell}) => {
                return tell == SIGNALS.QUOTE_SELECTED
            }
        )
        .subscribe(
            ({data}) => {
                if (data.id >= 0) {
                    xhr.get(
                        '/quotes/' + data.id,
                        (err, resp) => send(bus, SIGNALS.QUOTE_LOADED, JSON.parse(resp.body))
                    );
                } else {
                    send(bus, SIGNALS.QUOTE_LOADED, {id: data.id, text: ''});
                }

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
                    function(err, resp) {
                        //console.log(resp.body);
                        send(bus, SIGNALS.QUOTE_LOADED, resp.body)

                    }
                );
            }
        );

    bus
        .filter(
            ({tell}) => {
                return tell == SIGNALS.QUOTE_ADD
            }
        )
        .subscribe(
            ({data:{id, text}}) => {
                xhr.post(
                    `/quotes`,
                    {json: {text}},
                    function(err, resp) {
                        xhr.post(
                            resp.headers.location,
                            {json: {text}},
                            function(err, resp) {
                                //console.log(resp.body);
                                send(bus, SIGNALS.QUOTE_LOADED, resp.body)

                            }
                        );

                    }
                );
            }
        );

    bus
        .filter(
            ({tell}) => {
                return tell == SIGNALS.QUOTE_TOGGLE
            }
        )
        .subscribe(
            ({data:{id, text}}) => {
                xhr.patch(
                    `/quotes/${id}`,
                    {json: {text}},
                    function(err, resp) {

                    }
                );
            }
        );
}
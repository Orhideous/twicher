import xhr from 'xhr';

export const SIGNALS = {
    QUOTES_LOADED: "QUOTES_LOADED"
};

export function send(bus, tell, data) {
    bus.onNext({tell, data});
}

export function init_bus(bus) {
    xhr.get(
        '/quotes',
        (err, resp) => send(bus, SIGNALS.QUOTES_LOADED, JSON.parse(resp.body))
    );
}
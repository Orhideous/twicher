from models import Quote, storage
from flask import make_response, url_for, abort

QUOTE_TPL = "quote:{}"


def get_quote_or_404(quote_id):
    text = storage.get(QUOTE_TPL.format(quote_id))
    return Quote(quote_id, text) if text else abort(404)


def get_all():
    ids = sorted(map(int, storage.smembers("all_quotes")))
    keys = [QUOTE_TPL.format(quote_id) for quote_id in ids]
    values = storage.mget(keys)
    return [Quote(quote_id, quote_text) for quote_id, quote_text in zip(ids, values)]

def get_active():
    ids = sorted(map(int, storage.smembers("active_quotes")))
    keys = [QUOTE_TPL.format(quote_id) for quote_id in ids]
    values = storage.mget(keys)
    return [Quote(quote_id, quote_text) for quote_id, quote_text in zip(ids, values)]


def get_random():
    return get_quote_or_404(storage.srandmember("active_quotes"))


def create(text):
    if not text:
        abort(400)
    quote_id = storage.incr("last_quote_id")
    storage.sadd("all_quotes", quote_id)
    storage.sadd("active_quotes", quote_id)
    storage.set(QUOTE_TPL.format(quote_id), text)
    resp = make_response('', 201)
    resp.headers['Location'] = url_for('quote', quote_id=quote_id)
    return resp


def read(quote_id):
    return get_quote_or_404(quote_id)


def update(quote_id, text):
    if not text:
        abort(400)
    if not storage.sismember("all_quotes", quote_id):
        abort(404)
    storage.set(QUOTE_TPL.format(quote_id), text)
    return Quote(quote_id, text)


def toggle(quote_id):
    if not storage.sismember("all_quotes", quote_id):
        abort(404)
    if storage.sismember("active_quotes", quote_id):
        storage.srem("active_quotes", quote_id)
    else:
        storage.sadd("active_quotes", quote_id)
    return make_response('', 204)

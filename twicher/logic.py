from models import db, Quote
from pony import orm
from flask import make_response, url_for, abort
from utils import make_snippet


@orm.db_session
def get_quote_or_404(quote_id):
    try:
        return Quote[quote_id]
    except orm.ObjectNotFound:
        return abort(404)


@orm.db_session
def get_all():
    return Quote.select()[:]


@orm.db_session
def get_random():
    return Quote.select().random(1)


@orm.db_session
def create(text):
    if not text:
        abort(400)
    quote = Quote(
        text=text,
        snippet=make_snippet(text)
    )
    db.commit()
    resp = make_response('', 201)
    resp.headers['Location'] = url_for('quote', quote_id=quote.id)
    return resp


@orm.db_session
def read(quote_id):
    return get_quote_or_404(quote_id)


@orm.db_session
def update(quote_id, text):
    if not text:
        abort(400)
    quote = get_quote_or_404(quote_id)
    quote.text = text
    quote.snippet = make_snippet(text)
    db.commit()
    return quote


@orm.db_session
def delete(quote_id):
    quote = get_quote_or_404(quote_id)
    quote.delete()
    db.commit()
    return make_response('', 204)

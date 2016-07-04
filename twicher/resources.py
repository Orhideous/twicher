from flask.ext.restful import Resource, marshal_with
from flask.ext.restful.reqparse import RequestParser

import logic
from utils import quote_marshaller

parser = RequestParser()
parser.add_argument('text', type=str, required=True)


# noinspection PyMethodMayBeStatic
class QuotesList(Resource):

    @marshal_with(quote_marshaller)
    def get(self):
        return logic.get_all()

    def post(self):
        text = parser.parse_args().get('text', None)
        return logic.create(text)


# noinspection PyMethodMayBeStatic
class Quote(Resource):

    @marshal_with(quote_marshaller)
    def get(self, quote_id):
        return logic.read(quote_id)

    @marshal_with(quote_marshaller)
    def post(self, quote_id):
        text = parser.parse_args().get('text', None)
        return logic.update(quote_id, text)

    def patch(self, quote_id):
        return logic.toggle(quote_id)


class Random(Resource):

    @marshal_with(quote_marshaller)
    def get(self):
        return logic.get_random()

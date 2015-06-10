from flask.ext.restful import Resource, marshal_with
from flask.ext.restful.reqparse import RequestParser

from twicher import logic
from twicher.utils import quote_marshaller

parser = RequestParser()
parser.add_argument('text', type=str, required=True)


class QuotesList(Resource):

    @marshal_with(quote_marshaller)
    def get(self):
        return logic.get_all()

    def post(self):
        text = parser.parse_args()
        return logic.create(text)


class Quote(Resource):

    @marshal_with(quote_marshaller)
    def get(self, quote_id):
        return logic.read(quote_id)

    def put(self, quote_id):
        text = parser.parse_args()
        return logic.update(quote_id, text)

    def delete(self, quote_id):
        return logic.delete(quote_id)


class Random(Resource):

    @marshal_with(quote_marshaller)
    def get(self):
        return logic.get_random()

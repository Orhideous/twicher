from flask.ext.restful import Resource


class QuotesList(Resource):

    def get(self):
        pass

    def post(self):
        pass


class Quote(Resource):

    def get(self, quote_id):
        pass

    def put(self, quote_id):
        pass

    def delete(self, quote_id):
        pass


class Random(Resource):

    def get(self):
        pass

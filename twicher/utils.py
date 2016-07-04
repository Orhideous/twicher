from flask_restful.fields import Integer, String

quote_marshaller = {'id': Integer, 'text': String, 'snippet': String}

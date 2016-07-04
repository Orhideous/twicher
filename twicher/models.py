from flask_redis import FlaskRedis

storage = FlaskRedis()


class Quote:
    def __init__(self, quote_id, text):
        self.id = int(quote_id)
        if isinstance(text, str):
            self.text = text
        elif isinstance(text, bytes):
            self.text = text.decode()

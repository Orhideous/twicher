from pony import orm


db = orm.Database()


class Quote(db.Entity):

    _table_ = 'Quote'

    text = orm.Required(str)

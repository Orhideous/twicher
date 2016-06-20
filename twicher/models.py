from pony import orm


db = orm.Database()


class Quote(db.Entity):

    _table_ = 'Quote'

    snippet = orm.Required(str)
    text = orm.Required(str)

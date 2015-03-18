#!/usr/bin/env python
from contextlib import contextmanager
from copy import deepcopy

from pony import orm
import progressbar as pb
from flask.ext.script import Manager

from models import db, Quote
from application import app


manager = Manager(app)

COLORS = {
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'ORANGE': '\033[93m',
    'RED': '\033[91m',
    'END': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}


@contextmanager
def perform(name, before, fail, after, kwargs=None):
    kwargs = deepcopy(kwargs) if kwargs else {}
    kwargs.update(
        COLORS,
        name=name,
        before=before.format(**kwargs),
        fail=fail.format(**kwargs),
        after=after.format(**kwargs),
    )
    print("{BLUE}[{name}]{END} {before}".format(**kwargs))
    try:
        yield
    except Exception as e:
        print("{RED}[{name}]{END} {fail}".format(**kwargs))
        print("{RED}[{name}]{END} Reason: {e}".format(e=e, **kwargs))
        exit(1)
    else:
        print("{GREEN}[{name}]{END} {after}".format(**kwargs))


@manager.command
def init_db():
    """Create empty database"""

    with perform(
            "DB",
            "Initialising empty database",
            "Failed to create empty database",
            "Database {DB_NAME} (type: {DB_TYPE}) successfully created",
            app.config
    ):
        db.bind(app.config['DB_TYPE'], app.config['DB_NAME'], create_db=True)
        db.generate_mapping(create_tables=True)


@manager.option(
    "-f", "--file",
    type=str,
    required=True,
    dest="file",
    help="html-file with quotes"
)
def load_quotes(file):
    with perform(
            "Import",
            "Parsing quotes from '{file}'",
            "Failed to parse quotes!",
            "Parsing quotes from '{file}' successful",
            {"file": file}
    ), open(file) as f:
        quotes = list(filter(None, map(str.strip, f.read().split('<hr>'))))

    db.bind(app.config['DB_TYPE'], app.config['DB_NAME'])
    db.generate_mapping()

    with perform(
            "Saving",
            "Saving quotes into database",
            "Failed to save quotes!",
            "Done!"
    ), orm.db_session:
        bar = pb.ProgressBar(widgets=[
            '{ORANGE}[Saving]{END} '.format(**COLORS),
            pb.Counter(), ' quotes ', pb.Bar(), ' ',
            pb.Percentage()
        ])
        for quote_text in bar(quotes):
            Quote(text=quote_text)

if __name__ == "__main__":
    manager.run()

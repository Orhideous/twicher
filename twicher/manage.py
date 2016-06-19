#!/usr/bin/env python
from pony.orm import db_session
import progressbar as pb
from flask_script import Manager

from models import db, Quote
from application import app
from utils import perform, COLORS

manager = Manager(app)


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
    """Load quotes from file"""

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
    ), db_session:
        bar = pb.ProgressBar(widgets=[
            '{ORANGE}[Saving]{END} '.format(**COLORS),
            pb.Counter(), ' quotes ', pb.Bar(), ' ',
            pb.Percentage()
        ])
        for quote_text in bar(quotes):
            Quote(text=quote_text)

if __name__ == "__main__":
    manager.run()

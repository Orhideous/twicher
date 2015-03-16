#!/usr/bin/env python
from flask.ext.script import Manager
from models import db

from application import app

manager = Manager(app)


class C:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@manager.command
def init_db():
    """Create empty database"""

    print("{}[DB]{} Initialising empty database...".format(C.BLUE, C.END))
    try:
        db.bind(app.config['DB_TYPE'], app.config['DB_NAME'], create_db=True)
        db.generate_mapping(create_tables=True)
    except Exception as e:
        print("{}[DB]{} Failed to create empty database!".format(C.FAIL, C.END))
        print("{}[DB]{} Reason:".format(C.FAIL, C.END))
        print(e)
    else:
        print(
            "{g}[DB]{e} Database {b}{db_name}{e} (type: {b}{db_type}{e})"
            " successfully created!".format(
                g=C.GREEN,
                b=C.BOLD,
                e=C.END,
                db_name=app.config['DB_NAME'],
                db_type=app.config['DB_TYPE']
            )
        )

if __name__ == "__main__":
    manager.run()

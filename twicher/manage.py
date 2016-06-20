#!/usr/bin/env python
from flask_script import Manager

from models import db
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


if __name__ == "__main__":
    manager.run()

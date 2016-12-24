# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import MigrateCommand
from flask_migrate import Migrate

from areweblic.app import app, db
from areweblic.models import License


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def init_db():
    db.create_all()

    req = License('user_id', 'SSP', b'license request content', b'', 'descr')

    db.session.add(req)
    db.session.commit()

manager.run()

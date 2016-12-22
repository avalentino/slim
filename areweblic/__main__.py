# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import MigrateCommand

from areweblic.app import app, db
from areweblic.models import LicenseRequest


manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def init_db():
    db.create_all()

    req = LicenseRequest('user_id', 'SSP', b'license request content', 'descr')

    db.session.add(req)
    db.session.commit()

manager.run()

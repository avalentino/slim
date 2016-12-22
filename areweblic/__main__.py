#!/usr/bin/env python

# env PYTHONPATH=. FLASK_APP=areweblic FLASK_DEBUG=1 python -m flask run

from .app import app
app.run()

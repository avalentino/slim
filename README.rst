SLiM - A Simple License Management system
=========================================

:author:    Antonio Valentino <antonio.valentino@tiscali.it>
:copyright: 2016, Antonio Valentino
:homepage:  https://github.com/avalentino/slim


Introduction
------------

The name SLiM is the acronym of "(S)imple (Li)cense (M)anagement system".

It is a very simple web application for SW license management written in
Flask_.

Features:

* light and web based
* authentication
* license request upload
* license file download
* administration interface

  - simple user management
  - simple product list management
  - simple purchasing management
  - configurable license generator program

.. _Flask: http://flask.pocoo.org


Requirements
------------

See `requirements.txt`


Installation
------------

::

  $ pip install slim


Development
-----------

The source code of the project can be found at:
https://github.com/avalentino/slim.

To run the development server use the following command for the project
root directory::

  $ env PYTHONPATH=. FLASK_DEBUG=TRUE python -m slim runserver

The package also provides a basic set tools for developer life easier::

  $ env PYTHONPATH=. FLASK_DEBUG=TRUE python -m slim --help

  usage: __main__.py [-?] {shell,db,init_test_db,runserver,user,init_db} ...

  positional arguments:
    {shell,db,init_test_db,runserver,user,init_db}
      shell               Runs a Python shell inside Flask application context.
      db                  Perform database migrations
      init_test_db        Basic initialization of the internal DB for testing
      runserver           Runs the Flask development server i.e. app.run()
      user                Perform user management
      init_db             Basic initialization of the internal DB


  optional arguments:
    -?, --help            show this help message and exit


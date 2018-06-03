SLiM - A Simple License Management system
=========================================

:author:    Antonio Valentino <antonio dot valentino at tiscali dot it>
:copyright: 2016-2018, Antonio Valentino
:license:   MIT
:homepage:  https://github.com/avalentino/slim


.. image:: https://travis-ci.org/avalentino/slim.svg?branch=master
    :target: https://travis-ci.org/avalentino/slim


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


.. important::

    SLiM is mainly a toy project and it **shall not be used in production**


.. _Flask: http://flask.pocoo.org


Requirements
------------

See `requirements.txt`


Installation
------------

::

  $ pip install slim


Command line interface
----------------------

The package also provides a command line tool that implements a basic set
functions that can be used both in the development and deployment phase::

  $ slimcli --help

  usage: slimcli [-?] {init_db,init_test_env,db,user,shell,runserver} ...

  positional arguments:
    {init_db,init_test_env,db,user,shell,runserver}
      init_db             Make a basic initialization of the internal DB.
      init_test_env       Make a basic initialization of the testing
                          environment.
      db                  Perform database migrations
      user                Perform user management
      shell               Runs a Python shell inside Flask application context.
      runserver           Runs the Flask development server i.e. app.run()

  optional arguments:
    -?, --help            show this help message and exit


Development
-----------

The source code of the project can be found at:
https://github.com/avalentino/slim.

A test environment can be set-up as follows (optional)::

  $ python3 -m venv slimenv
  $ source slimenv/bin/activete
  $ pip install wheel
  $ pip install -r requirements.txt

The command line interface can be run form the development folder as follows::

  $ env PYTHONPATH=. python -m slim <COMMAND>

Before running the development server the slim database shall be initialized,
and, at least, one admin user shall be enabled::

  $ env PYTHONPATH=. python -m slim init_db
  $ env PYTHONPATH=. python -m slim user change_password admin <password>
  $ env PYTHONPATH=. python -m slim user enable admin

The DB is initialized in the `instance` folder.
In the same folder it is possible to install an instance configuration file.
A template can ge found in the `examples` directory.

To run the development server use the following command for the project
root directory::

  $ env PYTHONPATH=. python -m slim runserver

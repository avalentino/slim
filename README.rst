SLiM - A Simple License Management system
=========================================

:author:    Antonio Valentino <antonio dot valentino at tiscali dot it>
:copyright: 2016-2017, Antonio Valentino
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


Development
-----------

The source code of the project can be found at:
https://github.com/avalentino/slim.

To run the development server use the following command for the project
root directory::

  $ env PYTHONPATH=. python -m slim runserver

The package also provides a basic set tools for developer life easier::

  $ env PYTHONPATH=. python -m slim --help

  usage: __main__.py [-?] {runserver,init_test_env,shell,db,user,init_db} ...

  positional arguments:
    {runserver,init_test_env,shell,db,user,init_db}
      runserver           Runs the Flask development server i.e. app.run()
      init_test_env       Basic initialization of the testing environment
      shell               Runs a Python shell inside Flask application context.
      db                  Perform database migrations
      user                Perform user management
      init_db             Basic initialization of the internal DB

  optional arguments:
    -?, --help            show this help message and exit


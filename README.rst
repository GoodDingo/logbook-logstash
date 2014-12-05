logbook-logstash
================

JSON logs with logstash format for logbook

This library is provided to allow
`logbook <http://pythonhosted.org/Logbook/>`__ logging to output log
data as json objects ready to be shipped out to logstash.

This project is a fork of
`exoscale/python-logstash-formatter <https://github.com/exoscale/python-logstash-formatter>`__

Installing
----------

Pip:

::

    $ pip install logbook-logstash

Pypi:

https://pypi.python.org/pypi/logbook-logstash

Manual:

::

    $ python setup.py install

Usage
-----

Json outputs are provided by the LogstashFormatter logging formatter,
for instance:

.. code:: python


        import sys

        import logbook_logstash
        from logbook import Logger, StreamHandler


        log = Logger('testlog')

        handler = StreamHandler(sys.stdout)
        handler.formatter = logbook_logstash.LogstashFormatter()
        handler.push_application()

        log.info('My test')

You can provide extra variables, and show the exception traceback.

.. code:: python


        log.info({"account": 123, "ip": "172.20.19.18"})
        log.info("classic message for account: %s", account, extra={"account": account})

        try:
            h = {}
            h['key']
        except:
            log.info("something unexpected happened", exc_info=True)

Sample output
-------------

The following keys will be found in the output JSON:

-  ``@source_host``: source hostname for the log
-  ``@timestamp``: ISO 8601 timestamp
-  ``@message``: short message for this log
-  ``@fields``: all extra fields

.. code:: python


      {
        "@fields": {
            "account": "pyr",
            "args": [],
            "created": 1367480388.013037,
            "exception": [
                "Traceback (most recent call last):\n",
                "  File \"toto.py\", line 16, in <module>\n    k['unknown']\n",
                "KeyError: 'unknown'\n"
            ],
            "filename": "toto.py",
            "funcName": "<module>",
            "levelname": "WARNING",
            "levelno": 30,
            "lineno": 18,
            "module": "toto",
            "msecs": 13.036966323852539,
            "name": "root",
            "pathname": "toto.py",
            "process": 1819,
            "processName": "MainProcess",
            "relativeCreated": 18.002986907958984,
            "thread": 140060726359808,
            "threadName": "MainThread"
        },
        "@message": "TOTO",
        "@source_host": "phoenix.spootnik.org",
        "@timestamp": "2013-05-02T09:39:48.013158"
      }

Tests
-----

This project has basic tests, and uses the ``pytest`` library. Just
execute the following commands in the project root.

::

    $ pip install -r dev-requirements.txt
    $ py.test


# -*- coding: utf-8 -*-

import json
import datetime

from logbook import LogRecord, FileHandler

from logbook_logstash import LogstashFormatter


FROZEN_DATETIME = datetime.datetime(2014, 12, 5, 17, 16, 15, 919636)


class MockedDate(datetime.datetime):
    @classmethod
    def utcnow(cls):
        return FROZEN_DATETIME


def test_formatter_with_file_handler(monkeypatch):
    r_fixture = {
        'channel': 'formatter.test',
        'level': 2,
        'msg': 'My test log message',
        'args': None,
        'kwargs': None,
        'exc_info': None,
        'extra': None,
        'frame': None,
        'dispatcher': None
    }
    fh_fixture = {
        'filename': '/tmp/bogus.log',
        'mode': 'a',
        'encoding': 'utf-8',
        'level': 0,
        'format_string': None,
        'delay': False,
        'filter': None,
        'bubble': False
    }
    # This date fixture translates to '2014-12-05T14:12:49.303830Z'
    timestamp_fixture = FROZEN_DATETIME.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    monkeypatch.setattr(datetime, 'datetime', MockedDate)

    lf = LogstashFormatter()
    json_msg = lf(
        record=LogRecord(**r_fixture),
        handler=FileHandler(**fh_fixture)
    )

    expected_json = {
        '@fields': {
            'extra': {}, 'level': r_fixture['level'], 'process': None,
            'frame': None, 'args': [], 'kwargs': {},
            '_dispatcher': r_fixture['dispatcher'],
            'channel': r_fixture['channel']
        },
        '@handler': {
            'level': fh_fixture['level'],
            '_filename': fh_fixture['filename'], '_mode': fh_fixture['mode'],
            'filter': fh_fixture['filter'], 'bubble': fh_fixture['bubble'],
            'encoding': fh_fixture['encoding']
        },
        '@timestamp': timestamp_fixture,
        '@source_host': 'localhost',
        '@message': r_fixture['msg']
    }
    assert json.loads(json_msg) == expected_json

import collections

import pytest

from syslog_rfc5424_parser import SyslogMessage
from syslog_rfc5424_parser.constants import SyslogFacility, SyslogSeverity


Expected = collections.namedtuple('Expected', ['severity', 'facility', 'version', 'timestamp', 'hostname',
                                               'appname', 'procid', 'msgid', 'msg', 'sd'])


VECTORS = (
    (
        '<1>1 - - - - - -',
        Expected(SyslogSeverity.alert, SyslogFacility.kern, 1, '-', '-', '-', '-', '-', None, {})
    ),
    (
        '<78>1 2016-01-15T00:04:01+00:00 host1 CROND 10391 - [meta sequenceId="29"] some_message',  # noqa
        Expected(SyslogSeverity.info, SyslogFacility.cron, 1, '2016-01-15T00:04:01+00:00', 'host1', 'CROND', 10391,
                 '-', 'some_message', {'meta': {'sequenceId': '29'}})
    ),
    (
        '<29>1 2016-01-15T01:00:43Z some-host-name SEKRETPROGRAM prg - [origin x-service="svcname"][meta sequenceId="1"] 127.0.0.1 - - 1452819643 "GET /health HTTP/1.1" 200 175 "-" "hacheck 0.9.0" 20812 127.0.0.1:40150 1199',  # noqa
        Expected(SyslogSeverity.notice, SyslogFacility.daemon, 1, '2016-01-15T01:00:43Z', 'some-host-name',
                 'SEKRETPROGRAM', 'prg', '-', '127.0.0.1 - - 1452819643 "GET /health HTTP/1.1" 200 175 "-" "hacheck 0.9.0" 20812 127.0.0.1:40150 1199',  # noqa
                 {'meta': {'sequenceId': '1'}, 'origin': {'x-service': 'svcname'}})
    ),
    (
        '<198>1 2016-01-15T01:00:59+00:00 some-other-host 2016-01-15 - - [origin x-service="program"][meta sequenceId="4"] 01:00:59,989 PRG[14767:INFO] Starting up',  # noqa
        Expected(SyslogSeverity.info, SyslogFacility.unknown, 1, '2016-01-15T01:00:59+00:00', 'some-other-host',
                 '2016-01-15', '-', '-', msg='01:00:59,989 PRG[14767:INFO] Starting up',
                 sd={'meta': {'sequenceId': '4'}, 'origin': {'x-service': 'program'}})
    )
)


@pytest.mark.parametrize('input_line, expected', VECTORS)
def test_vector(input_line, expected):
    parsed = SyslogMessage.parse(input_line)
    assert parsed.severity == expected.severity
    assert parsed.facility == expected.facility
    assert parsed.version == expected.version
    assert parsed.timestamp == expected.timestamp
    assert parsed.hostname == expected.hostname
    assert parsed.appname == expected.appname
    assert parsed.procid == expected.procid
    assert parsed.msgid == expected.msgid
    assert parsed.msg == expected.msg
    assert parsed.sd == expected.sd

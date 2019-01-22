import collections

import pytest

from syslog_rfc5424_parser import SyslogMessage, ParseError
from syslog_rfc5424_parser.constants import SyslogFacility, SyslogSeverity


Expected = collections.namedtuple('Expected', ['severity', 'facility', 'version', 'timestamp', 'hostname',
                                               'appname', 'procid', 'msgid', 'msg', 'sd'])


PARSE_VECTORS = (
    (
        '<1>1 - - - - - -',
        Expected(SyslogSeverity.alert, SyslogFacility.kern, 1, '-', '-', '-', None, None, None, {})
    ),
    (
        '<78>1 2016-01-15T00:04:01+00:00 host1 CROND 10391 - [meta sequenceId="29"] some_message',  # noqa
        Expected(SyslogSeverity.info, SyslogFacility.cron, 1, '2016-01-15T00:04:01+00:00', 'host1', 'CROND', 10391,
                 None, 'some_message', {'meta': {'sequenceId': '29'}})
    ),
    (
        '<29>1 2016-01-15T01:00:43Z some-host-name SEKRETPROGRAM prg - [origin x-service="svcname"][meta sequenceId="1"] 127.0.0.1 - - 1452819643 "GET /health HTTP/1.1" 200 175 "-" "hacheck 0.9.0" 20812 127.0.0.1:40150 1199',  # noqa
        Expected(SyslogSeverity.notice, SyslogFacility.daemon, 1, '2016-01-15T01:00:43Z', 'some-host-name',
                 'SEKRETPROGRAM', 'prg', None, '127.0.0.1 - - 1452819643 "GET /health HTTP/1.1" 200 175 "-" "hacheck 0.9.0" 20812 127.0.0.1:40150 1199',  # noqa
                 {'meta': {'sequenceId': '1'}, 'origin': {'x-service': 'svcname'}})
    ),
    (
        '<190>1 2016-01-15T01:00:59+00:00 some-other-host 2016-01-15 - - [origin x-service="program"][meta sequenceId="4"] 01:00:59,989 PRG[14767:INFO] Starting up',  # noqa
        Expected(SyslogSeverity.info, SyslogFacility.local7, 1, '2016-01-15T01:00:59+00:00', 'some-other-host',
                 '2016-01-15', None, None, msg='01:00:59,989 PRG[14767:INFO] Starting up',
                 sd={'meta': {'sequenceId': '4'}, 'origin': {'x-service': 'program'}})
    ),
    # this one has a malformed PRI
    (
        '<409>1 2016-01-15T00:00:00Z host2 prg - - - message',
        Expected(SyslogSeverity.alert, SyslogFacility.unknown, 1, '2016-01-15T00:00:00Z', 'host2',
                 'prg', None, None, 'message', {})
    ),
    # this one has an SD-ID, but no SD-PARAMS
    (
        '<78>1 2016-01-15T00:04:01+00:00 host1 CROND 10391 - [sdid] some_message',  # noqa
        Expected(SyslogSeverity.info, SyslogFacility.cron, 1, '2016-01-15T00:04:01+00:00', 'host1', 'CROND', 10391,
                 None, 'some_message', {'sdid': {}})
    ),
    (
        '<85>1 2017-03-02T13:21:15.733598-08:00 vrs-1 polkitd 20481 - -  msg',
        Expected(SyslogSeverity.notice, SyslogFacility.authpriv, 1, '2017-03-02T13:21:15.733598-08:00', 'vrs-1',
                 'polkitd', 20481, None, ' msg', {})
    ),
    # reported in pr 2; empty sd-param body
    (
        '<29>1 2018-05-14T08:23:01.520Z leyal_test4 mgd 13894 UI_CHILD_EXITED [junos@2636.1.1.1.2.57 pid="14374" return-value="5" core-dump-status="" command="/usr/sbin/mustd"]',  # noqa
        Expected(SyslogSeverity.notice, SyslogFacility.daemon, 1, '2018-05-14T08:23:01.520Z',
                 'leyal_test4', 'mgd', 13894, 'UI_CHILD_EXITED', None, {
                     'junos@2636.1.1.1.2.57': {
                         'command': '/usr/sbin/mustd',
                         'core-dump-status': '',
                         'pid': '14374',
                         'return-value': '5',
                     }
                 })
    ),
    # reported in issue #7; multi-line body
    (
        '<78>1 2019-01-17T17:39:00Z localhost CROND 9999 - - some message\nwith embedded newlines',
        Expected(SyslogSeverity.info, SyslogFacility.cron, 1, '2019-01-17T17:39:00Z',
                 'localhost', 'CROND', 9999, None, 'some message\nwith embedded newlines', {})
    ),
    # requested in #10
    (
        '''<134>1 2019-01-20T23:43:41.087236Z 172.16.3.1 NAT 15634 SADD [nsess SSUBIX="0" SVLAN="0" IATYP="IPv4" ISADDR="172.16.1.2" ISPORT="6303" XATYP="IPv4" XSADDR="10.0.0.3" XSPORT="16253" PROTO="6" XDADDR="172.16.2.2" XDPORT="80"] <type 'str'>''',  # noqa
        Expected(SyslogSeverity.info, SyslogFacility.local0, 1, '2019-01-20T23:43:41.087236Z',
            '172.16.3.1', 'NAT', 15634,
            'SADD', '''<type 'str'>''',
            {
                'nsess': {
                    'SSUBIX': '0',
                    'SVLAN': '0',
                    'IATYP': 'IPv4',
                    'ISADDR': '172.16.1.2',
                    'ISPORT': '6303',
                    'PROTO': '6',
                    'XATYP': 'IPv4',
                    'XSADDR': '10.0.0.3',
                    'XSPORT': '16253',
                    'XDADDR': '172.16.2.2',
                    'XDPORT': '80',
                }
            }
        )
    )

)


# these only have one SD because ordering of SDs isn't consistent between runs
ROUND_TRIP_VECTORS = (
    '<1>1 - - - - - -',
    '<78>1 2016-01-15T00:04:01+00:00 host1 CROND 10391 - [meta sequenceId="29"] some_message',
)


@pytest.mark.parametrize('input_line, expected', PARSE_VECTORS)
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


def test_emitter():
    m = SyslogMessage(facility=SyslogFacility.cron, severity=SyslogSeverity.info)
    assert '<78>1 - - - - - -' == str(m)


def test_emitter_with_unix_timestamp():
    m = SyslogMessage(facility=SyslogFacility.kern, severity=SyslogSeverity.emerg, timestamp=0)
    assert '<0>1 1970-01-01T00:00:00Z - - - - -' == str(m)


@pytest.mark.parametrize('input_line', ROUND_TRIP_VECTORS)
def test_emitter_round_trip(input_line):
    m = SyslogMessage.parse(input_line)
    assert str(m) == input_line


@pytest.mark.parametrize('input_line, expected', PARSE_VECTORS)
def test_as_dict(input_line, expected):
    m = SyslogMessage.parse(input_line)
    dictified = m.as_dict()
    expected_dict = expected._asdict()
    expected_dict['severity'] = expected_dict['severity'].name
    expected_dict['facility'] = expected_dict['facility'].name
    assert dictified == expected_dict


def test_dumping_with_bad_pri_fails():
    m = SyslogMessage(facility=SyslogFacility.unknown, severity=SyslogSeverity.emerg)
    with pytest.raises(ValueError):
        str(m)


def test_unparseable():
    with pytest.raises(ParseError):
        SyslogMessage.parse('garbage')


def test_repr_does_not_raise():
    m = SyslogMessage(facility=SyslogFacility.cron, severity=SyslogSeverity.info)
    repr(m)

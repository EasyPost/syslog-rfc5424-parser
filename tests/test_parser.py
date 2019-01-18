from syslog_rfc5424_parser import parser


def test_minimal():
    message = '<1>1 - - - - - -'
    parsed = parser.syslog_message.parseString(message)
    assert 'header' in parsed
    assert parsed['header']['pri'] == 1
    assert parsed['header']['version'] == 1
    assert parsed['header']['timestamp'] == '-'
    assert parsed['header']['hostname'] == '-'
    assert parsed['header']['appname'] == '-'
    assert parsed['header']['procname'] == '-'
    assert parsed['header']['msgid'] == '-'
    assert parsed['sd'][0] == '-'

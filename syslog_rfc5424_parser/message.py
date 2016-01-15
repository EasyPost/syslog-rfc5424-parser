import json

import pyparsing

from . import parser
from .constants import SyslogSeverity, SyslogFacility


class ParseError(Exception):
    def __init__(self, description, message):
        self.description = description
        self.message = message

    def __repr__(self):
        return '{0}({1!r}, {2!r})'.format(self.__class__.__name__, self.description, self.message)

    def __str__(self):
        return '{0}: {1!r}'.format(self.description, self.message)


class SyslogMessage(object):
    __slots__ = ['severity', 'facility', 'version', 'timestamp', 'hostname', 'appname', 'procid', 'msgid', 'sd', 'msg']

    @classmethod
    def parse(cls, message):
        try:
            groups = parser.syslog_message.parseString(message)
        except pyparsing.ParseException:
            raise ParseError('Unable to parse message', message)
        obj = cls()
        header = groups['header']
        structured_data = groups['sd']
        if 'msg' in groups:
            msg = groups['msg']
        else:
            msg = None
        pri = int(header['pri'])
        fac = pri >> 3
        sev = pri & 7
        try:
            obj.severity = SyslogSeverity(sev)
        except Exception:
            obj.severity = SyslogSeverity.unknown
        try:
            obj.facility = SyslogFacility(fac)
        except Exception:
            obj.facility = SyslogFacility.unknown
        obj.version = header['version']
        obj.hostname = header['hostname']
        obj.timestamp = header['timestamp']
        obj.appname = header['appname']
        obj.procid = header['procname']
        obj.msgid = header['msgid']
        obj.msg = msg
        obj.sd = {}
        if structured_data != '-':
            for item in structured_data:
                obj.sd.setdefault(item['sd_id'], {})
                for param_pair in item['sd_params']:
                    obj.sd[item['sd_id']][param_pair['param_name']] = param_pair['param_value']
        return obj

    @property
    def topic_name(self):
        if 'origin' in self.sd and 'x-service' in self.sd['origin']:
            return '{0}.syslog'.format(self.sd['origin']['x-service'])
        else:
            return 'syslog'

    def __repr__(self):
        return '{0}({1})'.format(
            self.__class__.__name__,
            ','.join('{0}={1!r}'.format(k, getattr(self, k)) for k in self.__slots__)
        )

    def as_json(self):
        return json.dumps(dict(
            (k, getattr(self, k).name if k in ('severity', 'facility') else getattr(self, k))
            for k in self.__slots__
        ))

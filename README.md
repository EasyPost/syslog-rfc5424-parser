This module implements an [RFC 5424](https://tools.ietf.org/html/rfc5424) IETF Syslog Protocol parser in Python, using the [lark](https://github.com/lark-parser/lark) parser-generator. It should work on Python 2.7 or Python 3.3+.

[![Build Status](https://travis-ci.org/EasyPost/syslog-rfc5424-parser.svg?branch=master)](https://travis-ci.org/EasyPost/syslog-rfc5424-parser)
[![PyPI version](https://badge.fury.io/py/syslog-rfc5424-parser.svg)](https://badge.fury.io/py/syslog-rfc5424-parser)
[![Documentation Status](https://readthedocs.org/projects/syslog-rfc5424-parser/badge/?version=latest)](https://syslog-rfc5424-parser.readthedocs.io/en/latest/?badge=latest)

The file [example_syslog_server.py](example_syslog_server.py) contains a fully-functional Syslog server which will receive messages on a UNIX domain socket and print them to stdout as JSON blobs.

### A word on performance
On a fairly modern system (Xeon E3-1270v3), it takes about 230µs to parse a single syslog message and construct a SyslogMessage object (which is to say, you should be able to parse about 4300 per second with a single-threaded process). Are you really in that much of a rush, anyway?

If you're interested in a faster, non-Python alternative, you may also enjoy
[rust-syslog-rfc5424](https://github.com/Roguelazer/rust-syslog-rfc5424).

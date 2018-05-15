This module implements an [RFC 5424](https://tools.ietf.org/html/rfc5424) IETF Syslog Protocol parser in Python, using the [pyparsing](http://pyparsing.wikispaces.com/) parser-generator. It should work on Python 2.7 or Python 3.3+.

[![Build Status](https://travis-ci.org/EasyPost/syslog-rfc5424-parser.svg?branch=master)](https://travis-ci.org/EasyPost/syslog-rfc5424-parser)

The file [example_syslog_server.py](example_syslog_server.py) contains a fully-functional Syslog server which will receivemessages on a UNIX domain socket and print them to stdout as JSON blobs.

### A word on performance
On a fairly modern system (Xeon E3-1270v3), it takes about 700µs to parse a single syslog message and construct a SyslogMessage object (which is to say, you should be able to parse about 1400 per second with a single-threaded process). Effectively all of the time is spent in pyparsing, and packrat only makes it worse. Are you really in that much of a rush, anyway?

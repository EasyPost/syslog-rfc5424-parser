#!/usr/bin/env python

from __future__ import print_function

import argparse
import socket
import os
import sys
import json

from syslog_rfc5424_parser import SyslogMessage, ParseError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-B', '--bind-path', required=True,
                        help='Path at which to bind a Datagram-mode UNIX domain socket')
    args = parser.parse_args()

    s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    temp_name = args.bind_path + '.' + str(os.getpid())
    s.bind(temp_name)
    os.rename(temp_name, args.bind_path)

    while True:
        message = s.recv(4096)
        # Technically, messages are only UTF-8 if they have a BOM; otherwise they're binary. However, I'm not
        # aware of any Syslog servers that handle that. *shrug*
        message = message.decode('utf-8')
        try:
            message = SyslogMessage.parse(message)
            print(json.dumps(message.as_dict()))
        except ParseError as e:
            print(e, file=sys.stderr)


if __name__ == '__main__':
    sys.exit(main())

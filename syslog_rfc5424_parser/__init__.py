from .message import SyslogMessage, ParseError

version_info = (0, 3, 2)
__version__ = '.'.join(map(str, version_info))
__author__ = 'James Brown <jbrown@easypost.com>'

__all__ = ['SyslogMessage', 'ParseError', 'version_info', '__version__', '__author__']

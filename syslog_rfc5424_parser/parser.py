import collections

from lark import Lark, Transformer


GRAMMAR = '''
    ?start           : header _SP structured_data [ msg ]
    ?header          : pri version _SP timestamp _SP hostname _SP appname _SP procid _SP msgid
    pri              : "<" /[0-9]{1,3}/ ">"
    version          : /[1-9][0-9]{0,2}/
    timestamp        : NILVALUE
                     | /[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}/ time_secfrac? time_offset
    time_secfrac     : /\.[0-9]{1,6}/
    time_offset      : ZULU
                     | _ntime_offset
    _ntime_offset    : /[+-][0-9]{2}:[0-9]{2}/
    structured_data  : NILVALUE
                     | sd_element+
    sd_element       : "[" sd_id (" " sd_param)* "]"
    ?sd_id           : sd_name
    sd_param         : param_name "=" ESCAPED_STRING
    ?param_name      : sd_name
    ?sd_name         : /[^= \]\"]{1,32}/
    appname          : NILVALUE
                     | /[!-~]{1,48}/
    procid           : NILVALUE
                     | /[!-~]{1,128}/
    msgid            : NILVALUE
                     | /[!-~]{1,32}/
    hostname         : NILVALUE
                     | /[!-~]{1,255}/
    msg              : / .*/ms

    %import common.ESCAPED_STRING   -> ESCAPED_STRING

    _SP: " "
    NILVALUE: "-"
    ZULU: "Z"
'''


Header = collections.namedtuple('Header', ['pri', 'version', 'timestamp', 'hostname', 'appname', 'procid', 'msgid'])

SDElement = collections.namedtuple('SDElement', ['sd_id', 'sd_params'])

ParsedMessage = collections.namedtuple('ParsedMessage', ['header', 'structured_data', 'message'])


class TreeTransformer(Transformer):
    def NILVALUE(self, inp):
        return '-'

    def pri(self, inp):
        return int(inp[0])

    def version(self, inp):
        return int(inp[0])

    def timestamp(self, inp):
        if len(inp) == 1:
            return inp[0]
        else:
            datetime = str(inp[0])
            rest = [str(i.children[0]) for i in inp[1:]]
            return datetime + ''.join(rest)

    def hostname(self, inp):
        return str(inp[0])

    def appname(self, inp):
        return str(inp[0])

    def procid(self, inp):
        inp = str(inp[0])
        if inp.isdigit():
            return int(inp)
        return inp

    def msgid(self, inp):
        return str(inp[0])

    def structured_data(self, inp):
        if len(inp) == 1 and inp[0] == "-":
            return []
        output = []
        for sd_element in inp:
            sd_id = str(sd_element.children[0])
            sd_params = []
            for sd_param in sd_element.children[1:]:
                param_name = str(sd_param.children[0])
                param_value = str(sd_param.children[1])[1:-1]
                sd_params.append((param_name, param_value))
            output.append(SDElement(sd_id=sd_id, sd_params=sd_params))
        return output

    def msg(self, inp):
        return str(inp[0])[1:]

    def header(self, inp):
        return Header(
            pri=inp[0],
            version=inp[1],
            timestamp=inp[2],
            hostname=inp[3],
            appname=inp[4],
            procid=inp[5],
            msgid=inp[6]
        )

    def start(self, inp):
        if len(inp) > 2:
            message = inp[2]
        else:
            message = None
        return ParsedMessage(
            header=inp[0],
            structured_data=inp[1],
            message=message
        )


_parser = Lark(GRAMMAR, parser='lalr', transformer=TreeTransformer())


def parse(s):
    tree = _parser.parse(s)
    return tree


if __name__ == '__main__':
    import sys
    print(parse(sys.argv[1]))

import re
from pprint import pprint

def strip(self):
    return  self.lstrip(' ').lstrip('/n').lstrip('/t')

def string_parser(string):

    parsed_string = ''
    unparsed_string = ''

    if(string[0] != '"'):
        return (None, string.strip())

    x = 1
    while (string[x] != '"'):
        if(string[x] == '\\'):  # encounter of escape sequence
            x += 1
        parsed_string = parsed_string + string[x]
        x += 1
    unparsed_string = string[x+1:]
    return (parsed_string, unparsed_string.strip())


def null_parser(string):
    if (re.match('null', string) != None):
        return (None, string[4:].strip())


def boolean_parser(string):
    parsed_value = None

    if (re.match('true', string) != None):
        parsed_value = True
        string = string[4:].strip()

    elif (re.match('false', string) != None):
        parsed_value = False
        string = string[5:].strip()

    return (parsed_value, string)


def number_parser(string):

    to_parse_number_str = ''.join(re.findall(r'^((?:-?\d+)(?:\.?\d+)?(?:[Ee][+-]\d+)?)', string))
    if (len(to_parse_number_str) == 0):
        return (None, string)
    try:
        parsed_number = int(to_parse_number_str)
    except ValueError:
        parsed_number = float(to_parse_number_str)

    return (parsed_number, string[len(to_parse_number_str):].strip())


def array_parser(string):
    if (string[0] != '['):
        return (None, string.strip())
    parsed_list = []
    string = string[1:]

    while (string[0] != ']'):
        value, string = value_parser(string)   # checking if the value is string

        parsed_list.append(value)
        string = comma_parser(string)

    return (parsed_list, string[1:].strip())


def value_parser(string):
    parser_tuple = (string_parser, array_parser, object_parser,
                    number_parser, boolean_parser,)

    for parser_func in parser_tuple:

        value, string = parser_func(string.strip())

        if(value != None):
            return (value, string.strip())

        if (null_parser(string) != None):     # special check for null_parser
            return null_parser(string)


def comma_parser(string):
    if(string[0] != ','):
        return string.strip()
    else:
        return string[1:].strip()


def colon_parser(string):
    if(string[0] != ':'):
        return None
    else:
        return string[1:].strip()


def object_parser(string):
    if(string[0] != '{'):
        return (None, string.strip())

    parsed_dict = {}
    string = string[1:]

    string = string.strip()

    while(string[0] != '}'):

        key, string = string_parser(string)

        string = colon_parser(string) # expected : after key
        if (string is None):
            raise SyntaxError(": not found")
                                      # start of value
        value, string = value_parser(string)

        parsed_dict[key] = value   # key: value pair generated

        string = comma_parser(string)

        continue

    return (parsed_dict, string[1:])

if __name__ == "__main__":
    with open('first.json') as f:
        content = f.read()

    content = ''.join(x for x in content)
    pprint (object_parser(content))
#    print (content)
#    content = re.search(r'(".*?")', content)
#    print (content)

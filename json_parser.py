import pdb
import re

def string_parser(string):

    parsed_string = ''
    unparsed_string = ''

    if(string[0] != '"'):
        return (None,string.strip())

    if(string[0] == '"'):

        x = 1
        while (string[x] != '"'):
            if(string[x] == '\\'):  # encounter of escape sequence
                x += 1
            parsed_string = parsed_string + string[x]
            x += 1
        unparsed_string = string[x+1:]
    return (parsed_string, unparsed_string.strip())


def value_parser(string):
    original_string = string
    parsed_value = None

    if (re.match('true',string) != None):
        parsed_value = True
        string = string[4:].strip()

    elif (re.match('false',string) != None):
        parsed_value = False
        string = string[5:].strip()

    elif (re.match('null',string) != None):
        parsed_value = None
        string =  string[4:].strip()

    if(original_string != string):
        return (parsed_value, string )
    else:
        return None


def number_parser(string):

    to_parse_number_str = ''.join(re.findall(r'^((?:-?\d+)(?:\.?\d+)?(?:[Ee][+-]\d+)?)',string))
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
    if(string[0] == '['):
        parsed_list = []
        string = string[1:]

        while (string[0] != ']'):

            value,string = string_parser(string)   # checking if the value is string

            if(value != None):
                parsed_list.append(value)

            value,string = object_parser(string) #sending to Object parser

            if(value != None):
                parsed_list.append(value)

            value,string = number_parser(string) # sending to number_parser

            if (value != None):
                parsed_list.append(value)

            if(value_parser(string) != None): # if return None means the value is not null
                value, string = value_parser(string)  # value parsing
                parsed_list.append(value)

            string = comma_parser(string)

        return (parsed_list, string[1:].strip())


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
        return (None,string.strip())

    if(string[0] == '{'):
        parsed_dict = {}
        string = string[1:]

        string = string.strip()

        while(string[0] != '}'):

            key, string = string_parser(string)   # return of string_parser of form ("","") tuple

            string = colon_parser(string) # expected : after key
            if (string is None):
                raise SyntaxError(": not found")

                                          # start of value
            value, string = string_parser(string)   # checking for string value

            if (value is None): # if value is a JS object
                value, string = object_parser(string)

            if (value is None):
                value, string = array_parser(string)
                                    # number parser
            if (value is None):
                value, string = number_parser(string)

            if (value is None):    # always put value_parser at last
                value, string = value_parser(string)

            string = string.strip()
            parsed_dict[key] = value   # key: value pair generated

            string = comma_parser(string)

            continue

        return (parsed_dict, string[1:])

if __name__ == "__main__":
    with open('first.json') as f:
        content = f.read()

    content = ''.join(x.strip('\n').strip('\t') for x in content)
    print (content)
    content = re.search(r'(".*?")', content)
    print (content)

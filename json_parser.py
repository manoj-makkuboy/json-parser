import re


def string_parser(string):

    parsed_string = ''
    unparsed_string = ''

    if(string[0] == '"'):

        x = 1
        while (string[x] != '"'):
            parsed_string = parsed_string + string[x]
            x += 1
        unparsed_string = string[x+1:]

    return (parsed_string, unparsed_string)


def array_parser(string):
    pass


def object_parser(string):
    if(string[0] == '{'):

        parsed_dict = {}
        string = string[1:]

        while(string[0] != '}'):

            if (string[0] == '"'):   # assuming key will be a string
                key_string_tuple = string_parser(string[:])
                key, string = key_string_tuple   # return of string_parser of form ("","") tuple

            if (string[0] != ':'):
                raise SyntaxError(" : not found after key")
            elif(string[0] == ':'):
                string = string[1:]

            if (string[0] == '"'):
                value_string_tuple = string_parser(string[:])
                value, string = value_string_tuple

            if (string[0] == '{'):
                value_dict_tuple = object_parser(string)   #recursive call when value is a dict
                value, string = value_dict_tuple

            parsed_dict[key] = value   # key: value pair generated

            if (string[0] == ','):
                string = string[1:]
                if(string[0] == '}'):
                    raise SyntaxError(" no key:value pair found after , ")
            continue

#        string = string[1:]             # case to find the end of dict in string
#        if(string == ''):
#            return (parsed_dict, string)    # base case return

        return (parsed_dict, string[1:])

if __name__ == "__main__":
    with open('first.json') as f:
        content = f.read()

    content = ''.join(x.strip(' ').strip('\n').strip('\t') for x in content)
    print (content)
    content = re.search(r'(".*?")', content)
    print (content)

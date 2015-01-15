# -*- coding: utf-8 -*-
from constants import html_colors, plain_to_tex_dict
from helpers import find_first


def int_to_fixed_hex(val, length=2):
    result = hex(val)[2:]
    result = (length - len(result)) * u"0" + result
    return result


def need_definition_color(color):
    color = color.upper()
    return color.startswith(u"RGB(") or color.startswith(u"#") or color in html_colors


#Получаем имя цвета, которое должно быть определено в начале файла и может быть использовано в дальнейшем
def get_color_name(color):
    color = color.upper()
    if color in html_colors:
        result = color
    elif color.startswith(u"#"):
        result = u"MSHPCOLOR" + color[1:]
    elif color.startswith(u"RGB("):
        rgb_list = color[4:-1].split(',')
        html_style_color = u"".join([int_to_fixed_hex(int(single_color.strip(u" "))) for single_color in rgb_list])
        result = u"MSHPCOLOR" + html_style_color
    else:
        result = u"black"
    return result


#Получаем код, который позволяет определить нужный нам цвет
def get_single_color_definition(color):
    color = color.upper()
    if not color:
        result = u"{black}"
    elif color in html_colors:
        result = html_colors[color]
    elif color.startswith(u"#"):
        color = color[1:]
        if len(color) == 3:
            color = u"0".join(color) + u"0"
        result = u"{HTML}{%s}" % color
    elif color.startswith(u"RGB("):
        rgb_list = color[4:-1].split(',')
        html_style_color = u"".join([int_to_fixed_hex(int(single_color.strip(u" "))) for single_color in rgb_list])
        result = u"{HTML}{%s}" % html_style_color.upper()
    else:
        result = u"{%s}" % color
    return result


#Возможно вынести в helpers всего проекта, так как довольно полезно
def dict_to_string(dictionary, key_value_separator=u"=", separator=u','):
    return separator.join([key_value_separator.join([key, value]) for key, value in dictionary.items()])


#escape максимально длинных подстрок.
def plain_to_tex(string):

    if not string.strip(u" "):
        string = u""

    def get_tokens():
        index = 0
        while index < len(string):
            lengths = xrange(max_escaped_len, 0, -1)
            length = find_first(lengths, lambda length: string[index:index + length] in plain_to_tex_dict)
            token = plain_to_tex_dict[string[index:index + length]] if length else string[index]
            index += length or 1
            yield token
    return u"".join(get_tokens())

max_escaped_len = 8


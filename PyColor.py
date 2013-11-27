import re

def get_colors_old():
    '''
        Function loads 6 digit hex colors and formats them to a list.

        TODO: make function more general

        Returns: List
    '''
    colors_list = []

    with open('config/unformated_colors', encoding='utf-8') as file:
        for line in file:
            colors_list.extend(line.rsplit(' '))
    colors_list = ['#' + color.strip() for color in colors_list]

    return colors_list


def get_colors():
    '''
        Function loads 6 digit hex colors and formats them to a list

        Returns: List
    '''
    colors_list = []

    # pattern matching any 6 digit hex color, either with # or without
    pattern = '#?[0-9a-fA-F]{6}'

    # we find all strings matching our pattern in a file
    with open('config/unformated_colors', encoding='utf-8') as file:
        colors_list = re.findall( pattern, file.read() )

    # if color already have a # sign just remove all ws char. else add #
    colors_list = ['#' + color.strip() if (color[0] != '#')
                    else color.strip() for color in colors_list]

    return  colors_list

def toggle_blue(colors):
    '''
        Function takes list of 6 digit hex colors and depending on the value of blue it toggles it to be either 255 or 0. Then it returns newly created list of colors.

        Returns: List
    '''
    border_colors = []

    # If the blue value is smaller then 127 (7f) then change it to 'ff' else
    # to '00'
    for color in colors:
        if int(color[1:5], 16) < 127:
            border_colors.append(color[:5] + 'ff')
        else:
            border_colors.append(color[:5] + '00')

    return border_colors


def invert_colors(colors):
    '''
        Function takes list of colors and inverse each of them. Then, it returns list with inverted colors.

        Returns: List
    '''

    ids_colors = []

    # create translation table
    prev = tuple(ord(c) for c in '#0123456789abcdef')
    new = tuple(ord(c) for c in '#fedcba9876543210')
    inv_table = dict(zip(prev, new))

    # inverse each color in the list using inv_table
    for color in colors:
        inv_color = color.lower().translate(inv_table)
        ids_colors.append(inv_color)

    return ids_colors

import PyColor
import pickle
import random

def main():
    '''
        When script is launched from terminal it creates list of triples of colors to use in plot and saves it to pickle file

    '''

    # load colors
    squares_colors = PyColor.get_colors()

    # create labels colors by inverting colors of squares
    ids_colors = PyColor.invert_colors(squares_colors)

    # make list of triples of colors for every task on the list and shuffle it
    palette = list(zip(squares_colors, ids_colors))

    random.shuffle(palette)

    config_path = '../config/palette_data.pickle'

    # save list of triples to config file using pickle
    with open(config_path, 'wb') as fl:
        pickle.dump(palette, fl)


if __name__ == '__main__':
    main()

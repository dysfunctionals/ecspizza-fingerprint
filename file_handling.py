import pickle

import os


def load_pkl(name):
    if os.path.isfile(name):
        with open(name, 'rb') as f:
            return pickle.load(f)
    else:
        return {}


def write_pkl(name, data):
    with open(name, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def get_pizza_centre(file_name, pklfile):
    data = load_pkl(pklfile)
    return data[file_name]


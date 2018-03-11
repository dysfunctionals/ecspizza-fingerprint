import functools
import pickle

import cv2 as cv


@functools.lru_cache()
def load_pkl():
    with open('centres.pkl', 'rb') as file:
        return pickle.load(file)


def get_pizza_centre(file_name):
    data = load_pkl()
    return data[file_name]


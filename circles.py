import functools

import pickle
from PIL import Image
import cv2 as cv
import numpy as np
import sys
import argparse

from slicing import lines

def detect_pizzas(src):
    # Get the shortest edge of the image
    smallest_image_dimension = min(src.shape[0:2])
    # Smallest allowable pizza radius takes up this amount of the image
    smallest_radius = int((smallest_image_dimension/2) * 0.55)

    # Greyscale & blur the image
    img = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    img = cv.medianBlur(img, 5)

    circles = cv.HoughCircles(
        img,
        method=cv.HOUGH_GRADIENT,
        dp=0.3,
        minDist=int(smallest_image_dimension * 2),
        # The higher threshold of the two passed to Canny
        param1=130,
        # The accumulator threshold for the circle centers at the detection stage. The smaller it is, the more false circles may be detected
        param2=30, # 40
        minRadius=smallest_radius,
        maxRadius=0,
    )
    return circles


@functools.lru_cache()
def load_pkl():
    with open('centres.pkl', 'rb') as file:
        return pickle.load(file)


def get_pizza_centre(file_name):
    data = load_pkl()
    return data[file_name]


def display_circles(circles, image):
    if circles is not None: # Check if circles have been found and only then iterate over these and add them to the image
        a, b, c = circles.shape
        for i in range(b):
            cv.circle(image, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv.LINE_AA)
            cv.circle(image, (circles[0][i][0], circles[0][i][1]), 2, (0, 255, 0), 3, cv.LINE_AA)  # draw center of circle

    cv.imshow("detected circles", image)
    cv.waitKey(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    file_names = args.files
    for file_name in file_names:
        print(file_name)
        src = cv.imread(file_name, 1)
        centre = get_pizza_centre(file_name)
        radius = max(src.shape)/3
        circle = centre[0], centre[1], radius
        # circles = detect_pizzas(src)
        # circle = circles[0][0] if circle else None
        if circle is not None:
            lines(src, circle)
        else:
            print(f"No circles in {file_name}")
    # display_circles(circles, src.copy())

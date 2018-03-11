import argparse
import cv2 as cv

from circle_detection import detect_pizzas
from circle_manual import get_pizza_centre
from fingerprinting import calc_fingerprint

CENTRES_FILE = 'centres.pkl'
PRINTS_FILE = 'prints.pkl'


def display_circles(circles, image):
    if len(circles): # Check if circles have been found and only then iterate over these and add them to the image
        for circle in circles:
            circle = tuple(int(x) for x in circle)
            cv.circle(image, (circle[0], circle[1]), circle[2], (0, 0, 255), 3, cv.LINE_AA)
            cv.circle(image, (circle[0], circle[1]), 2, (0, 255, 0), 3, cv.LINE_AA)  # draw center of circle

    cv.imshow("detected circles", image)
    cv.waitKey(0)


def collect_data(file_names,
                 detect_circles=False,
                 show_edges=False,
                 show_fingers=False,
                 show_circles=False):
    for file_name in file_names:
        print(file_name)
        img = cv.imread(file_name, 1)

        if detect_circles:
            circles = detect_pizzas(img)
        else:
            centre = get_pizza_centre(file_name)
            radius = max(img.shape)/3
            circles = [(centre[0], centre[1], radius)]

        if show_circles:
            display_circles(circles, img.copy())

        if len(circles):
            fingerprint = calc_fingerprint(img,
                                           circles[0],
                                           show_edges=show_edges,
                                           show_fingers=show_fingers,
                                           )

        else:
            print(f"No circles in {file_name}")
    # display_circles(circles, img.copy())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    parser.add_argument('--detect_circles', action='store_true', default=False)
    parser.add_argument('--show_circles', action='store_true', default=False)
    parser.add_argument('--show_edges', action='store_true', default=False)
    parser.add_argument('--show_fingers', action='store_true', default=False)
    parser.add_argument('--centres', default=CENTRES_FILE)
    parser.add_argument('--prints', default=PRINTS_FILE)
    args = parser.parse_args()
    file_names = args.files
    collect_data(
        file_names,
        detect_circles=args.detect_circles,
        show_edges=args.show_edges,
        show_fingers=args.show_fingers,
        show_circles=args.show_circles,
    )


if __name__ == '__main__':
    main()


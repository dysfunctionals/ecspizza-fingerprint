import argparse
import cv2 as cv

from circle_detection import detect_pizzas
from file_handling import get_pizza_centre, load_pkl, write_pkl
from fingerprinting import calc_fingerprint, similarity

CENTRES_FILE = 'centres.pkl'
PRINTS_FILE = 'prints.pkl'


def display_circles(circles, image):
    if len(
            circles):  # Check if circles have been found and only then iterate over these and add them to the image
        for circle in circles:
            circle = tuple(int(x) for x in circle)
            cv.circle(image, (circle[0], circle[1]), circle[2], (0, 0, 255), 3,
                      cv.LINE_AA)
            cv.circle(image, (circle[0], circle[1]), 2, (0, 255, 0), 3,
                      cv.LINE_AA)  # draw center of circle

    cv.imshow("detected circles", image)
    cv.waitKey(0)


def guess_pizza_circle(img, file_name, centres_file):
    centre = get_pizza_centre(file_name, centres_file)
    radius = max(img.shape) / 3
    return \
        centre[0], centre[1], radius


def collect_data(
         file_names,
         detect_circles=False,
         show_edges=False,
         show_fingers=False,
         show_circles=False,
         centres_file=CENTRES_FILE,
         prints_file=PRINTS_FILE,
    ):

    saved_prints = load_pkl(prints_file)
    # if we're displaying, go through all of them
    if any([show_edges, show_fingers, show_circles]):
        to_process = file_names
    else:
        # otherwise only process the ones we need to process
        to_process = set(file_names) - set(saved_prints.keys())
        if not to_process:
            print("Nothing to process!")
    for file_name in to_process:
        print('Calculating', file_name)
        img = cv.imread(file_name, 1)

        if detect_circles:
            circles = detect_pizzas(img)
        else:
            circles = [guess_pizza_circle(img, file_name, centres_file)]

        if show_circles:
            display_circles(circles, img.copy())

        if len(circles):
            fingerprint = calc_fingerprint(
                img,
                circles[0],
                show_edges=show_edges,
                show_fingers=show_fingers,
            )
            if not detect_circles:  # (only save if we've manually done the circles)
                saved_prints[file_name] = fingerprint
        else:
            print(f"No circles in {file_name}")

    write_pkl(prints_file, saved_prints)

    # display_circles(circles, img.copy())


def find_nearest(file_names, prints_file=PRINTS_FILE, centres_file=CENTRES_FILE):
    print("finding nearest...")
    saved_prints = load_pkl(prints_file)
    # print("prints", saved_prints)
    for file_name in file_names:
        samenesses = []
        candidate = saved_prints[file_name]
        for compare_file_name, comparison in saved_prints.items():
            if file_name == compare_file_name:
                continue
            sameness = similarity(candidate, comparison)
            samenesses.append((sameness, compare_file_name))
        samenesses.sort()

        print(file_name)
        print(samenesses[:6])
        samest, samest_file_name = samenesses[0]
        img = cv.imread(file_name)
        calc_fingerprint(
            img,
            guess_pizza_circle(img, file_name, centres_file),
            show_fingers='Candidate'
        )
        img = cv.imread(samest_file_name)
        calc_fingerprint(
            img,
            guess_pizza_circle(img, samest_file_name, centres_file),
            show_fingers='Closest'
        )
        cv.waitKey(0)


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
        centres_file=args.centres,
        prints_file=args.prints,
    )

    find_nearest(
        file_names,
        prints_file=args.prints,
        centres_file=args.centres,
    )


if __name__ == '__main__':
    main()

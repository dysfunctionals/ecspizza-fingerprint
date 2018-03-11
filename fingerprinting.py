import functools
from collections import deque

import cv2 as cv
import numpy as np

angles_to_try = 300
offsets_per_angle = 10
SAMPLES_PER_LINE = 100


def rotate(pos, theta):
    rot_mat = np.array([[np.cos(theta), -np.sin(theta)],
                        [np.sin(theta), np.cos(theta)]])
    return np.dot(rot_mat, pos)


def get_intensity(edges, angle, circle):
    x, y, radius = tuple(circle)
    unit_vector = rotate((radius, 0), angle)
    # no need to oversample
    samples = min(SAMPLES_PER_LINE * 1.4, radius)
    vals = []
    for sample in np.linspace(0, 1, samples):
        dx = unit_vector[0] * sample
        dy = unit_vector[1] * sample
        nx = int(x + dx)
        ny = int(y + dy)
        if ny < edges.shape[0] and nx < edges.shape[1]:
            vals.append(edges[ny][nx])
    return np.mean(vals)


def draw_radius(img, circle, angle, color=(0, 255, 0)):
    x, y, radius = circle
    unit = rotate((radius, 0), angle)
    cv.line(
        img,
        (int(x + unit[0]), int(y + unit[1])),
        (int(x), int(y)),
        color
    )


def normalise(finger):
    mean = np.mean(finger)
    normalised = np.array([x - mean for x in finger])
    return normalised


@functools.lrucache(maxsize=1000)
def similarity(candidate, template):
    # Matches the two fingerprints like how inspectors match bullets.
    # (rotate one array to find the closest match).
    candidate_deque = deque(candidate)
    assert len(candidate) == len(template), "candidate should match template"
    smallest_difference = 9e999
    for offset in range(len(candidate)):
        difference = 0
        for c, t in zip(candidate_deque, template):
            difference += int(abs(c - t))
        smallest_difference = min(smallest_difference, difference)
        candidate_deque.rotate(1)
    return smallest_difference


def running_average(values, running_avg=50):
    for i, val in enumerate(values):
        avg = np.mean([values[(i+c) % len(values)] for c in range(running_avg)])
        yield val-avg


def calc_fingerprint(img, circle, show_edges=False, show_fingers=False):
    x, y, rad = circle
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.blur(gray, ksize=(10, 10))
    gray = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                          cv.THRESH_BINARY, 111, 2)

    if show_edges:
        edges = cv.Canny(gray, 60, 120, apertureSize=3)
        cv.imshow(f"lines {show_edges}", edges)
        # cv.waitKey(0)

    angles = []
    for angle in np.linspace(0, 2 * np.pi, 1000):
        prob = get_intensity(gray, angle, circle)
        angles.append((angle, prob))

    angles = [(ang, n_val) for ((ang, val), n_val) in
              zip(angles, running_average([v for _, v in angles]))]

    if show_fingers:
        overlay = img.copy()
        for ang, val in angles:
            scaled = (val / 155) + 0.2
            draw_radius(overlay, (x, y, rad * scaled), ang)

        img = cv.addWeighted(overlay, 0.5, img, 0.5, 0)

        cv.imshow(f"fingers {show_fingers}", img)

    return [v for _, v in angles]


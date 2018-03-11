import cv2 as cv

from fingerprinting import calc_fingerprint, similarity


def get_image_fingerprint(img_name):
    """
    Get the fingerprint data for a given image.

    Image Requirements:
    - Each image *must* be taken from directly above the pizza
    - Each image must have its centre at the middle (the sliced centre) of the pizza

    :param img_name: image file name to get the data for
    :return: fingerprint data in the form of a list of floats
    """
    img = cv.imread(img_name, 1)
    estimated_pizza_radius = max(img.shape) / 3
    circle = (
        int(img.shape[1]/2),
        int(img.shape[0]/2),
        estimated_pizza_radius
    )
    return calc_fingerprint(
        img,
        circle,
    )


def get_pizza_similarity(fingerprint_1, fingerprint_2):
    """
    Get the similarity of two pizza fingerprints.
    Anything higher than 0.5 can be considered a match.

    :param fingerprint_1: fingerprint 1 to compare against
    :param fingerprint_2: fingerprint 2 to compare against
    :return: similarity of a pizza (>0.5 is a match)
    """
    sameness = similarity(fingerprint_1, fingerprint_2)
    certainty = 1-((sameness/18000)*0.5)
    return certainty

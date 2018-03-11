import cv2 as cv


def detect_pizzas(img):
    # Get the shortest edge of the image
    smallest_image_dimension = min(img.shape[0:2])
    # Smallest allowable pizza radius takes up this amount of the image
    smallest_radius = int((smallest_image_dimension/2) * 0.55)

    # Greyscale & blur the image
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
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
    if len(circles):
        return circles[0]
    else:
        return []




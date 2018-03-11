from PIL import Image
import argparse

from file_handling import load_pkl

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
centres = load_pkl('centres.pkl')
args = parser.parse_args()
for file_name in args.files:
    img = Image.open(file_name)
    centre = centres[file_name]
    image_centre = int(img.size[0]/2), int(img.size[1]/2)
    dx = centre[0]-image_centre[0]
    dy = centre[1]-image_centre[1]

    img2 = Image.new('RGB',
                     (img.size[0]+(dx*2 if dx > 0 else 0), img.size[1]+(dy*2 if dy > 0 else 0)),
                     (255, 255, 255))
    img2.paste(
        img,
        (-dx if dx < 0 else 0, -dy if dy < 0 else 0)
    )
    img2.save(f"{file_name}_centred.jpg")
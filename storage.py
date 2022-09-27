import json
import os
import sys
from os.path import exists
from pathlib import Path

from PIL import ImageDraw, Image

from modules import pre_trained_classifier

SETTINGS_FILENAME = "settings.json"


def check_folder_struct(data):
    Path(data['data_root']).mkdir(parents=True, exist_ok=True)
    Path(data['tmp_root']).mkdir(parents=True, exist_ok=True)
    Path(data['ext_root']).mkdir(parents=True, exist_ok=True)
    Path(data['prt_root']).mkdir(parents=True, exist_ok=True)
    Path(data['prt_img_root']).mkdir(parents=True, exist_ok=True)


def create_settings_file():
    data = {
        'data_root': '/home/regen/psrc/data',
        'tmp_root': '/home/regen/psrc/tmp',
        'ext_root': '/home/regen/psrc/data/external',
        'prt_root': '/home/regen/psrc/data/private',
        'prt_img_root': '/home/regen/psrc/data/private/image',
    }
    json_string = json.dumps(data)
    with open(SETTINGS_FILENAME, 'w') as f:
        f.write(json_string)
        print("Created the json settings file")

    return data


def init():
    if exists(SETTINGS_FILENAME):
        f = open(SETTINGS_FILENAME)
        settings = json.load(f)
    else:
        settings = create_settings_file()

    check_folder_struct(settings)

    return settings


def show_image(image):
    with Image.open(image) as im:
        draw = ImageDraw.Draw(im)
        draw.line((0, 0) + im.size, fill=128)
        draw.line((0, im.size[1], im.size[0], 0), fill=128)

        # write to stdout
        im.save(sys.stdout, "PNG")


def analysis(file):
    image = Image.open(file)

    metadata = os.stat(file)
    stats = {k: getattr(metadata, k) for k in dir(metadata) if k.startswith('st_')}

    # Get image tags
    objects = pre_trained_classifier.get_classes(file)
    # Faces
    # etc

    # extract other basic metadata
    info_dict = {
        "Original Filename": os.path.basename(image.filename),
        "Objects": objects,
        "Stats": stats,
        "Image Size": image.size,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    return info_dict


def print_info(metadata_path):
    if exists(metadata_path):
        f = open(metadata_path)
        meta_data = json.load(f)
        for label, value in meta_data.items():
            print(f"{label:25}: {value}")
        print('')

import argparse
import io
import json
import os
import shutil
from os.path import exists

from PIL import Image

import storage


def all_in_folder(folder, settings):
    if not exists(folder):
        print(f'{folder} not found!')
        return

    for file in os.listdir(folder):
        single_file(folder + file, settings, True)


def single_file(file, settings, verbose=False):
    if not exists(file):
        print(f'{file} not found!')
        return

    info = storage.analysis(file)
    # TODO: identical ctime fix by checking original filename, adding _x.json
    time = str(info['Stats']['st_mtime_ns'])
    new_image_filename = time + '.png'
    new_json_filename = time + '.json'

    new_path = settings['data_root'] + '/private/image/'
    if new_image_filename not in os.listdir(new_path):
        image = Image.open(file)
        image.save(new_path + new_image_filename)

    with open(new_path + new_json_filename, 'w') as f:
        json_string = json.dumps(info)
        f.write(json_string)

    if verbose:
        print(f'Entity {time} information:')
        storage.print_info(new_path + new_json_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--folder', type=str, required=False)
    group.add_argument('--file', type=str, required=False)
    args = parser.parse_args()

    s = storage.init()
    if args.folder:
        all_in_folder(args.folder, s)
    elif args.file:
        single_file(args.file, s)
    else:
        single_file('tmp/315_en_ful_snygg_blomma_brevid_mig_desutom_jaa_.jpg', s)


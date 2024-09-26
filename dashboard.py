from collections import defaultdict
import base64
import json
import os


def export_images(ipynb_fname, export_dir):
    with open(ipynb_fname) as fp:
        nb = json.load(fp)

    image_b64 = defaultdict(list)
    for cell in nb['cells']:
        for d in cell['outputs']:
            for k, v in d['data'].items():
                if 'image' in k:
                    img_type = k.replace('image/', '')
                    img_text = base64.b64decode(v)
                    image_b64[img_type].append(img_text)

    for img_type, images in image_b64.items():
        for i, img_b64 in enumerate(images):
            img_fname = f'plot_{i}.{img_type}'
            img_export = os.path.join(export_dir, img_fname)
            with open(img_export, 'wb') as fp:
                fp.write(img_b64)


if __name__ == "__main__":
    nb_fname = './sample.ipynb'
    export_dir = './images/'

    export_images(nb_fname, export_dir)
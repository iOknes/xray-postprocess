import os

import numpy as np
from cv2 import imread, imwrite


def load_folder(folder_path: str):
    images = []
    folder = os.listdir(folder_path)
    folder.sort()
    for filename in folder:
        if filename.endswith(".tif"):
            image = imread(os.path.join(folder_path, filename))
            images.append(image)
    return images


def image_diff(ref_image: np.ndarray, image: np.ndarray):
    ref_image = ref_image.astype(np.int16)
    image = image.astype(np.int16)
    diff = np.abs(ref_image - image)
    diff[diff > 8] = 255
    diff *= int(255 / diff.max())
    return diff.astype(np.uint8)


def postprocess(ref_image_path: str, image_path: str, output_path: str):
    ref_image = np.array(imread(ref_image_path))
    image = np.array(imread(image_path))

    if not output_path.endswith(".tif"):
        output_path += ".tif"

    diff = image_diff(ref_image, image)
    imwrite(output_path, diff)


def postprocess_folder(
    ref_image_path: str, image_folder_path: str, output_folder_path: str
):
    ref_image = np.array(imread(ref_image_path))
    images = load_folder(image_folder_path)

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    diffs = [image_diff(ref_image, i) for i in images]

    for i, diff in enumerate(diffs):
        imwrite(os.path.join(output_folder_path, f"diff_{i}.png"), diff)

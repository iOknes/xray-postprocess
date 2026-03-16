import os
import numpy as np
from cv2 import imread, imwrite

def load_images(regex: str):
    pass

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


def postprocess(ref_image: str, image: str, output: str):
    ref_image = imread(ref_image)
    image = imread(image)

    if not output.endswith(".tif"):
        output += ".tif"

    diff = image_diff(ref_image, image)
    imwrite(output, diff)


def postprocess_folder(ref_image: str, image: str, output: str):
    ref_image = imread(ref_image)
    images = load_folder(image)

    if not os.path.exists(output):
        os.makedirs(output)

    diffs = [image_diff(ref_image, i) for i in images]

    for i, diff in enumerate(diffs):
        imwrite(os.path.join(output, f"diff_{i}.png"), diff)

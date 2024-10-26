# -*- coding: utf-8 -*-
#
# Copyright (c) 2024~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from PIL import Image


def trim_white_border(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")

    width, height = image.size
    left, right, top, bottom = width, 0, height, 0

    def is_near_white(pixel, tolerance):
        return all(channel >= 255 - tolerance for channel in pixel[:3])

    # walk through each pixel and see if it's white
    pixel_data = image.load()
    for y in range(height):
        for x in range(width):
            if not is_near_white(pixel_data[x, y], 20):
                if x < left:
                    left = x
                if x > right:
                    right = x
                if y < top:
                    top = y
                if y > bottom:
                    bottom = y

    if (left, top, right + 1, bottom + 1) == (0, 0, width, height):
        # nothing to trim
        return image

    cropped_image = image.crop((left, top, right + 1, bottom + 1))
    return cropped_image


def split_image_by_color_difference(image: Image.Image, count: int, threshold=20, min_width=4) -> list[Image.Image]:
    pixels = image.load()

    def compute_boundary_rank(x):
        prev_col = [pixels[x-1, y] for y in range(height)]
        curr_col = [pixels[x, y] for y in range(height)]
        differences = [
            sum(abs(a - b) for a, b in zip(pixel1, pixel2))
            for pixel1, pixel2 in zip(prev_col, curr_col)
        ]
        if valid_diff := [x for x in differences if x > threshold]:
            return sum(valid_diff) + (len(valid_diff) * height)
        else:
            return 0

    width, height = image.size
    boundaries = [0]
    boundaries.append(width)
    for x in reversed(sorted(range(1, width), key=compute_boundary_rank)):
        if any(abs(x - b) < min_width for b in boundaries):
            continue
        boundaries.append(x)
        if len(boundaries) > count:
            break
    boundaries.sort()

    sub_images = []
    for i in range(len(boundaries) - 1):
        left = boundaries[i]
        right = boundaries[i + 1]
        sub_image = image.crop((left, 0, right, height))
        sub_images.append(sub_image)

    return sub_images

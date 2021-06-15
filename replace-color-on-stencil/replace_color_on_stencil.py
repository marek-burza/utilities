#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script replaces colors on a stenciled image
"""

import json
import sys

from PIL import Image, ImageDraw


def composite_stencil_and_base(config, best_base, best_alpha):
    """
    Creates composite image from the stencils and base color
    """
    for palette_entry in config['palette']:
        base_color = best_base[palette_entry]
        base_absent = base_color[:]
        base_absent.append(0)
        base_absent = tuple(base_absent)
        base_present = base_color[:]
        base_present.append(255 - best_alpha)
        base_present = tuple(base_present)
        for stencil_entry, stencil in config['stencils'].items():
            base = Image.new('RGBA', stencil.size)
            for at_x in range(stencil.size[0]):
                for at_y in range(stencil.size[1]):
                    if stencil.getpixel((at_x, at_y))[3] == 255:
                        base.putpixel((at_x, at_y), base_absent)
                    else:
                        base.putpixel((at_x, at_y), base_present)
            composite = Image.alpha_composite(base, stencil).convert('RGB')
            composite.save(f'composite.{stencil_entry}.{palette_entry}.jpg')


def prepare_stencils(config, image, best_alpha):
    """
    Prepares translucent stencils
    """
    stencil_color = config['stencil_color']
    stencil_color.append(255)
    stencil_color = tuple(stencil_color)
    for entry in config['stencils']:
        stencil_path = config['stencils'][entry]
        stencil = Image.open(stencil_path).convert('RGBA')
        for at_x in range(stencil.size[0]):
            for at_y in range(stencil.size[1]):
                color = list(image.getpixel((at_x, at_y)))
                if stencil.getpixel((at_x, at_y)) == stencil_color:
                    color.append(best_alpha)
                else:
                    color.append(255)
                stencil.putpixel((at_x, at_y), tuple(color))
        config['stencils'][entry] = stencil


def calculate_error(source, target, base, alpha):
    """
    Calculates error for a given source/target/base colors and alpha
    """
    alpha /= 255.0
    alpha_inverse = 1.0 - alpha
    return abs(target - alpha * source - alpha_inverse * base)


def channel_value_with_minimal_error(source, target, alpha):
    """
    Finds the base color channel with the smallest error for a given alpha
    """
    found_value = found_error = None
    for channel_value in range(10, 256 - 10):
        channel_error = calculate_error(source, target, channel_value, alpha)
        if found_error is None or channel_error < found_error:
            found_error = channel_error
            found_value = channel_value
    return found_value, found_error


def color_with_minimal_error(source, target, alpha):
    """
    Finds the base color with the smallest error for a given alpha
    """
    found_color = [None, None, None]
    found_error = 0.0
    for channel in [0, 1, 2]:
        found_value, minimal_error = channel_value_with_minimal_error(
            source[channel], target[channel], alpha)
        found_color[channel] = found_value
        found_error += minimal_error
    return found_color, found_error


def best_base_and_alpha(config):
    """
    Finds the base color and alpha with the smallest error
    """
    palette = config['palette']
    best_error = best_alpha = best_base = None
    for alpha in range(16, 256 - 16):
        error = 0
        base = {}
        for entry in palette:
            source = palette[entry]['source_color']
            target = palette[entry]['target_color']
            base_color, base_error = color_with_minimal_error(
                source, target, alpha)
            base[entry] = base_color
            error += base_error
        if best_error is None or error < best_error:
            best_error = error
            best_alpha = alpha
            best_base = base
    return best_base, best_alpha


def sample_average_color(image, box):
    """
    Samples average color inside a box
    """
    sum_r = sum_g = sum_b = 0
    all_xs = range(box[0][0], box[1][0] + 1)
    all_ys = range(box[0][1], box[1][1] + 1)
    for at_x in all_xs:
        for at_y in all_ys:
            color = image.getpixel((at_x, at_y))
            sum_r += color[0]
            sum_g += color[1]
            sum_b += color[2]
    count = len(all_xs) * len(all_ys)
    return (sum_r // count, sum_g // count, sum_b // count)


def sample_color(config, image, entry, box_key, color_key):
    """
    Samples the source and target color for replacement
    """
    gfx = ImageDraw.Draw(image)
    palette = config['palette']
    box = palette[entry][box_key]
    color = sample_average_color(image, box)
    palette[entry][color_key] = color
    gfx.rectangle(tuple([tuple(entry) for entry in box]), tuple(color))


def sample_colors(config, image):
    """
    Samples the source and target colors for replacement
    """
    for entry in config['palette']:
        sample_color(config, image, entry, 'source_color_box', 'source_color')
        sample_color(config, image, entry, 'target_color_box', 'target_color')


def load_image(config):
    """
    Loads the original image
    """
    return Image.open(config['original_image'])


def load_config(path):
    """
    Loades the configuration file
    """
    with open(path, 'rb') as handle:
        return json.loads(handle.read().decode('utf-8'))


def main():
    """
    Main function of the application
    """
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} CONFIG_FILE_PATH')
        sys.exit(1)
    config = load_config(sys.argv[1])
    image = load_image(config)
    sample_colors(config, image)
    best_base, best_alpha = best_base_and_alpha(config)
    prepare_stencils(config, image, best_alpha)
    composite_stencil_and_base(config, best_base, best_alpha)


if __name__ == '__main__':
    main()

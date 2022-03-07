#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script creates a heatmap plot.
"""

import json
import sys

import matplotlib.cm
import matplotlib.colors
import matplotlib.pyplot
import pandas


def heatmap(arguments):
    """
    Creates a heatmap
    """
    data = pandas.read_csv(arguments['input_file'])
    figure, axes = matplotlib.pyplot.subplots()
    figure.set_figwidth(arguments['width'])
    figure.set_figheight(arguments['height'])
    figure.set_dpi(arguments['dpi'])
    cmap = matplotlib.cm.get_cmap(arguments['cmap_name'], arguments['cmap_n'])
    norm = matplotlib.colors.Normalize(
        vmin=arguments['norm_vmin'], vmax=arguments['norm_vmax'],
        clip=arguments['norm_clip'])
    extent = arguments['extent']
    extent = None if extent is None else tuple(extent)
    plot = axes.imshow(
        data,
        cmap=cmap,
        norm=norm,
        aspect=arguments['aspect'],
        interpolation=arguments['interpolation'],
        alpha=arguments['alpha'],
        vmin=arguments['vmin'],
        vmax=arguments['vmax'],
        origin=arguments['origin'],
        extent=extent,
        filternorm=arguments['filternorm'],
        filterrad=arguments['filterrad'],
        resample=arguments['resample']
        )
    figure.colorbar(
        plot,
        extend=arguments['colorbar_extend'],
        extendfrac=arguments['colorbar_extendfrac'],
        extendrect=arguments['colorbar_extendrect'],
        spacing=arguments['colorbar_spacing'],
        ticks=arguments['colorbar_ticks'],
        format=arguments['colorbar_format'],
        drawedges=arguments['colorbar_drawedges'])
    axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
    matplotlib.pyplot.suptitle('')
    matplotlib.pyplot.title(arguments['title'])
    matplotlib.pyplot.tight_layout()
    figure.savefig(arguments['output_file'])
    matplotlib.pyplot.close()


def main():
    """
    Main entry point into the script.
    """
    if len(sys.argv) < 2:
        print('USAGE: plot_heatmap.py JSON_ARGUMENTS')
    else:
        arguments = {
            'title': '',
            'width': 12.80,
            'height': 7.20,
            'dpi': 100,
            'cmap_n': 256,
            'norm_vmin': None,
            'norm_vmax': None,
            'norm_clip': False,
            'aspect': None,
            'interpolation': None,
            'alpha': None,
            'vmin': None,
            'vmax': None,
            'origin': None,
            'extent': None,
            'filternorm': 1,
            'filterrad': 4.0,
            'resample': None,
            'colorbar_extend': 'neither',
            'colorbar_extendfrac': None,
            'colorbar_extendrect': False,
            'colorbar_spacing': 'uniform',
            'colorbar_ticks': None,
            'colorbar_format': None,
            'colorbar_drawedges': None
            }
        arguments.update(json.loads(sys.argv[1]))
        heatmap(arguments)


if __name__ == '__main__':
    main()

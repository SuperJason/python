# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Make GIF Animations of the Domino Shuffling Algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script requires ImageMagick be installed on your computer.
Windows users also need to set the variable `CONVERTER` below
to be the path to your `convert.exe`.

:copyright (c) 2015 by Zhao Liang.
"""
import os
import glob
import subprocess
import argparse
from tqdm import trange
import aztec
from random_tiling import render_with_cairo as render


CONVERTER = 'convert'


def make_animation(order, size, filename):
    """
    Begin with the Aztec diamond of order zero, repeat the operations
    `delete`, `slide` and `create` until its order reaches `order`.
    Render one frame for each operation and then use ImageMagick to
    convert the images to a gif file.

    Parameters
    ----------

    order: total steps to run the algorithm.

    size: size of the gif image.

    filename: the output .gif filename.
    """
    az = aztec.AztecDiamond(0)
    for i in trange(order):
        az.delete()
        render(az, size, order + 1, '_tmp{:03d}.png'.format(3 * i))

        az = az.slide()
        render(az, size, order + 1, '_tmp{:03d}.png'.format(3 * i + 1))

        az.create()
        render(az, size, order + 1, '_tmp{:03d}.png'.format(3 * i + 2))

    command = [CONVERTER,
               '-layers', 'Optimize',
               '-delay', '15', '_tmp%03d.png[0-{}]'.format(3 * order - 2),
               '-delay', '500', '_tmp{:03d}.png'.format(3 * order - 1),
               filename]
    subprocess.check_call(command)

    # do the clean up
    for f in glob.glob('_tmp*.png'):
        os.remove(f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-order', metavar='o', type=int,
                        default=30, help='order of aztec diamond')
    parser.add_argument('-size', metavar='s', type=int,
                        default=1024, help='image size')
    parser.add_argument('-filename', metavar='f',
                        default='domino_shuffling.gif', help='output filename')
    args = parser.parse_args()
    make_animation(args.order, args.size, args.filename)

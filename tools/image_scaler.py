#!/usr/bin/env python
# -*- coding: utf-8 -*-

# title              :image_scaler.py
# description        :asks the user for a horizontal and vertical value and scales all\
#                     the images found in the path with the provided factor.
# author             :divby0
# date               :20140802
# version            :0.2

import os
import argparse
import pygame as pg

SCALE_FACTOR_BOTTOM_LIMIT = 2
SCALE_FACTOR_UPPER_LIMIT = 10
PNG = '.png'


def check_params():
    parser = argparse.ArgumentParser(description='Image scaler.')
    parser.add_argument('path', action="store", help='path to the images (PNG)')
    parser.add_argument('--vertical', action="store", dest='vertical', type=int, default=2,
                        help='vertical scale factor')
    parser.add_argument('--horizontal', action="store", dest='horizontal', type=int, default=2,
                        help='horizontal scale factor')
    results = parser.parse_args()
    return results


def main():
    results = check_params()

    # Pygame initialization
    pg.init()
    display = pg.display.set_mode((320, 200))
    pg.display.set_caption('Image scaler')
    text = pg.Surface((320, 20))
    font = pg.font.SysFont(pg.font.get_default_font(), 20)

    # Notify to the user
    srfc = font.render('Scaler is working...', 1, (128, 128, 128))
    display.blit(srfc, (0, 0))
    pg.display.flip()

    # Calculate number of files
    number_of_files = 0

    for root, dirs, files in os.walk(results.path):

        for file in files:

            if file.lower().endswith(PNG):
                number_of_files += 1

    # Notify to the user
    srfc = font.render('Found ' + str(number_of_files) + ' files', 1, (128, 128, 128))
    display.blit(srfc, (0, 20))
    pg.display.flip()

    # Load files into the image dictionary
    image_map = {}

    for root, dirs, files in os.walk(results.path):

        for file in files:

            if file.lower().endswith(PNG):
                surface = pg.image.load(os.path.join(root, file))

                if surface is None:
                    print("Can't load file %s" % file)
                else:
                    image_map[file] = surface

    # Notify to the user
    srfc = font.render('Loaded ' + str(len(image_map)) + ' files', 1, (128, 128, 128))
    display.blit(srfc, (0, 40))
    pg.display.flip()

    # Iterate through the dictionary resizing the image
    for k in image_map.items():
        src_srfc = k[1]
        dst_srfc = pg.Surface((
            src_srfc.get_size()[0] * results.horizontal,
            src_srfc.get_size()[1] * results.vertical
        ), pg.SRCALPHA)
        dst_srfc.fill((0, 0, 0, 0))
        dst_srfc = pg.transform.scale(src_srfc, (
            src_srfc.get_size()[0] * results.horizontal,
            src_srfc.get_size()[1] * results.vertical
        ))

        # Inform to the user
        srfc = font.render('Saving scaled_' + k[0] + '...', 1, (128, 128, 128))
        text.fill((0, 0, 0))
        text.blit(srfc, (0, 0))
        display.blit(text, (0, 60))
        pg.display.flip()

        # Save the new image
        pg.image.save(dst_srfc, 'scaled_' + k[0])

    pg.quit()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#title              :animate.py
#description        :Animates some bitmaps. Useful when making some animations for a videogame and want to test them.
#author             :divby0
#date               :20140802
#version            :0.1
#usage              :
# M                 :Swap between movement mode and no movement.
# +/-               :Change background color.
# Left/Right Arrow  :Change x move speed (movement mode only)
# Down/UP Arrows    :Change y move speed (movement mode only)
# ESC               :Quit.

import pygame as pg
from pygame import image as img
import argparse
import sys


def check_params():
    parametros = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Small utility to animate some bitmaps.')
    parser.add_argument('input_file', action="store", help='image filename (PNG)')
    parser.add_argument('-z', action="store", dest='zoom', type=int, default=1, help='scale factor for image playing')
    parser.add_argument('--width', action="store", dest='width', type=int, default=640, help='screen width')
    parser.add_argument('--height', action="store", dest='height', type=int, default=480, help='screen height')
    parser.add_argument('-d', action="store", dest='delay', type=int, default=50, help='delay between frames')
    parser.add_argument('-f', action="store_true", dest='fullscreen', default=False, help='fullscreen')
    results = parser.parse_args()
    return results


def load_image(filename):
    image = None

    if filename is None or '' == filename.strip():
        image = pg.Surface((128, 32), pg.SWSURFACE | pg.SRCALPHA)
        image.fill((0, 0, 0, 0))
    else:
        image = img.load(filename)

    return image


def make_image_list(results, image):
    images = []
    img_size = image.get_rect()
    w = img_size[2]
    h = img_size[3]

    if w % h != 0:
        print('WARNING: Image width is not an exact multiple of image height')

    img_number = w / h

    for i in xrange(img_number):
        srfc = pg.Surface((h, h), pg.SWSURFACE | pg.SRCALPHA)
        srfc.fill((0, 0, 0, 0))
        srfc.blit(image, (0, 0), (i * h, 0, h, h))

        if results.zoom > 1:
            scaled_size = h * results.zoom
            scaled_srfc = pg.transform.scale(srfc, (scaled_size, scaled_size))
            images.append(scaled_srfc)
        else:
            images.append(srfc)

    return images


def main():
    move = False
    displ_flags = 0
    results = check_params()
    pg.init()

    if results.fullscreen:
        displ_flags = pg.FULLSCREEN

    display = pg.display.set_mode((results.width, results.height), displ_flags)
    pg.display.set_caption('Animating ' + results.input_file)
    image = load_image(results.input_file)
    images = make_image_list(results, image)
    counter = 0
    selected_color = 3
    colors = [
        (255, 255, 255, 255),
        (224, 224, 224, 244),
        (196, 196, 196, 196),
        (128, 128, 128, 255),
        (64, 64, 64, 255),
        (32, 32, 32, 255),
        (0, 0, 0, 255)
    ]

    x = 0
    y = 0
    x_direction = 1
    y_direction = 1
    x_speed = results.zoom
    y_speed = results.zoom

    while (True):
        display.fill(colors[selected_color])
        img_size = images[counter].get_size()

        if move is True:
            x = x + x_direction * x_speed
            y = y + y_direction * y_speed

            if x + img_size[0] + x_speed > results.width:
                x_direction = -1

            if x < 0:
                x_direction = +1

            if y + img_size[1] + y_speed > results.height:
                y_direction = -1

            if y < 0:
                y_direction = +1

        else:
            x = (results.width / 2) - (img_size[0] / 2)
            y = (results.height / 2) - (img_size[1] / 2)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit(0)

                if event.key == pg.K_PLUS:
                    if selected_color > 0:
                        selected_color = selected_color - 1

                if event.key == pg.K_MINUS:
                    if selected_color < len(colors) - 1:
                        selected_color = selected_color + 1

                if event.key == pg.K_RIGHT:
                    if x_speed < 30:
                        x_speed = x_speed + 1

                if event.key == pg.K_LEFT:
                    if x_speed > 0:
                        x_speed = x_speed - 1

                if event.key == pg.K_UP:
                    if y_speed < 30:
                        y_speed = y_speed + 1

                if event.key == pg.K_DOWN:
                    if y_speed > 0:
                        y_speed = y_speed - 1

                if event.key == pg.K_m:
                    move = move ^ True

        display.blit(images[counter], (x, y))
        pg.display.flip()
        pg.time.delay(results.delay)
        counter = counter + 1

        if counter >= len(images):
            counter = 0


if __name__ == '__main__':
    main()

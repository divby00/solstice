#!/usr/bin/env python
#-*- coding: utf-8 -*-
import pygame as pg
from display import display


def main():
    pg.init()
    disp = display.Display()
    disp.set_mode()
    pg.quit()


if __name__ == '__main__':
    main()

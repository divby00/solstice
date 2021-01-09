# Solstice


## IMPORTANT: This project is not longer under development, anyway, it doesn't mean that the remake has died, I've changed the technology and you can find the final remake in the repository 'solstice-godot', or in the url http://love4retro.itch.io/solstice. I keep this for historic purposes.

This project is a remake of Mikro-Gen's Equinox, a great game that I enjoyed a lot when I was a child.

In this remake you control a drone with the mission of stabilize a nuclear plant that can blow in any moment. 
The drone has the ability to fly and shoot to destroy the baddies made by the radiation, at the cost of energy.

The drone is limited to carry one object at a time, some objects are needed to open closed areas, others fill
the drone's energy, etc.

There are 8 levels to complete and each level has a time limit.

Good luck.

# Installation

Depending your OS, there are several ways to install the game:

## Windows

Windows users who don't want to install Python, the best option is to download the provided binaries at 
https://github.com/divby00/solstice/releases/download/0.0-alpha/solstice-0.0.zip
Please note that this package is not updated.

## Other OS

At the moment there isn't binary distribution of this game for Linux or Mac, to run this game follow this instructions:

* Install Python 2.7
* Install Pygame 1.9.14 `pip install pygame`
* Install git
* Clone the project: `git clone https://github.com/divby00/solstice.git`
* Enter the solstice folder and run `./solstice.sh`

## Setuptools

There is some support for setuptools, clone the project after installing python and git as explained above, enter in 
the solstice folder and run `python setup.py develop`
Now you could run the game with `python -m solstice.main`, note that the first time you run this command it won't work,
but it'll generate a file called `solstice.cfg`, adjust in that file the path to the game assets (`data.zip`) and the
next times it will work.

# Controls

You can control the game with a keyboard or a gamepad. Please note that the gamepad support is on alpha stage at the
moment, it will work *only* during the game, not in menus or any other interactive scene.

The keyboard default mapping is:

* W: Up
* A: Left
* D: Right
* S: Get / Change item
* U: Laser
* I: Use item

# Screenshots

* Screenshots of development version (Using 16 colors palette from Niklas Jansson, http://androidarts.com/).

    ![Title screen](https://cloud.githubusercontent.com/assets/7277786/10656742/5f0cba20-7882-11e5-8066-563e1f6086aa.png)
    ![Ingame screen](https://cloud.githubusercontent.com/assets/7277786/10656746/6e7ca330-7882-11e5-869a-cfb297a6a361.png)

* Screenshots of old version (2015-01-02). (EGA palette).

    ![Title screen](https://cloud.githubusercontent.com/assets/7277786/5601945/12a838c8-932a-11e4-9ca8-6f978f4e1b46.png)
    ![Ingame screen](https://cloud.githubusercontent.com/assets/7277786/5601946/12aca7d2-932a-11e4-83c3-e05f7cf5877c.png)

# Development notes

## Overview

This remake is made with Python 2.7 and Pygame 1.9. The game is based in the Spectrum version of Equinox. 
You can get the original game here: http://www.worldofspectrum.org/infoseekid.cgi?id=0001637

## How to prepare a development environment

* Clone the source code:
        
        git clone http://github.com/divby00/solstice
        
* Cd into the folder `solstice`:
    
        cd solstice
        
* Create a Python 2.7 virtual environment with `VirtualEnv` (install this tool if you don't have it installed):

        virtualenv venv
        
* Activate the virtual environment:

        source venv/bin/activate
        
* Install the project dependecies with `pip`:

        pip install -r dependencies.txt

## Tools

I have used both VIM and PyCharm to edit the source code, GIMP for graphics (using 16 colors palette from Niklas Jansson, http://androidarts.com/)
and Tiled (http://www.mapeditor.org) for the making and design of the levels. 

## Additional notes

The levels information are exported with this tool as `TMX`, there is a small implementation for loading the TMX format in `tiled_tools.py`.

All the data the game uses is saved in the zipped file data.zip, as all the data is read from it, you have to recreate
this zip file each time that you change some resource. The script `zipdata.sh` is useful for this.

The game has a resource manager that it is responsible of assets loading and also is used to access these resources.
Basically, it is a dictionary with the name of the asset that you want to obtain and the data itself. The definition of
all the resources is in file `resources.xml`, for each resource is a field called name, this is the key that you have to
use with resource manager (`resource_manager.py`).

## What is left

There're many things missing yet. The most important ones to consider the game finished are:

* A game over scene.
* An ending scene.
* Create levels 7 & 8.
* Add support for the bomb item.
* Add time limit.
* Fix the issue with music while playing.
* Fix the joystick and keyboard controls redefinition.
* Add joystick support to the UI.
* Find some way to serialize the level data to support coming back to the previous levels or remove this once for all. (ElevatorScene).
* More animations.
* More sounds.

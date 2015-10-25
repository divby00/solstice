Solstice
========
This project is a remake of Mikrogen's Equinox, a great game that I enjoyed a lot when I was a child.

In this game you control a drone with the mission of stabilize a nuclear plant that can blow in any moment. 
The drone has the ability to fly and shoot to destroy the baddies made by the radiation, at the cost of energy.

The drone is limited to carry one object at a time, some objects are needed to open closed areas, others fill
the drone's energy, etc.

There are 8 levels to complete and each level has a time limit.

Good luck.

Installation
============
At the moment there is no binary distribution of this project, to run this game install Python 2.7 and Pygame 1.9,
clone the project with git or download the source code from the button at the right and run python src/solstice.py.

Screenshots
===========
Screenshots of development version (Using 16 colors palette from Niklas Jansson, http://androidarts.com/).
![Title screen](https://cloud.githubusercontent.com/assets/7277786/10656742/5f0cba20-7882-11e5-8066-563e1f6086aa.png)
![Ingame screen](https://cloud.githubusercontent.com/assets/7277786/10656746/6e7ca330-7882-11e5-869a-cfb297a6a361.png)

Screenshots of old version (2015-01-02). (EGA palette).
![Title screen](https://cloud.githubusercontent.com/assets/7277786/5601945/12a838c8-932a-11e4-9ca8-6f978f4e1b46.png)
![Ingame screen](https://cloud.githubusercontent.com/assets/7277786/5601946/12aca7d2-932a-11e4-83c3-e05f7cf5877c.png)

Development notes
=================
Overview and tools
------------------
This remake is programmed with Python 2.7 and Pygame 1.9. The game is based in the Spectrum version of Equinox. 
You can get the original game here: http://www.worldofspectrum.org/infoseekid.cgi?id=0001637

I have used both VIM and PyCharm to edit the source code, GIMP for graphics (using 16 colors palette from Niklas Jansson, http://androidarts.com/)
and Tiled (http://www.mapeditor.org) for the making and design of the levels. 

The levels information are exported with this tool as TMX, there is a small implementation for loading the TMX format in tiled_tools.py.

All the data the game uses is saved in the zipped file data.zip, as all the data is read from it, you have to recreate
this zip file each time that you change some resource. The script zipdata.sh is useful for this.

The game has a resource manager that it is responsible of assets loading and also is used to access this resources.
Basically, it is a dictionary with the name of the asset that you want to obtain and the data itself. The definition of
all the resources is in file resources.xml, for each resource is a field called name, this is the key that you have to
use with resource manager (resource_manager.py).






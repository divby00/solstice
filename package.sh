#!/usr/bin/env bash
cd solstice
rm -rf ./dist
pyinstaller --onefile --windowed --icon=../solstice.ico solstice.py
rm -rf ./build
cp ../solstice.png ./dist/
cp ../solstice.cfg ./dist/
cp ../data.zip ./dist/
cd ..
echo "Done!"


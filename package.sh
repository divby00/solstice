#!/usr/bin/env bash
cd solstice
rm -rf ./dist
pyinstaller --onefile --windowed --icon=../solstice.ico main.py
rm -rf ./build
cp ../solstice.png ./dist/
cp ../solstice.cfg ./dist/
cp ../README.md ./dist/
cp ../data.zip ./dist/
cd ..
echo "Done!"


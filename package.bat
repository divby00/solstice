cd solstice
rmdir /s /q "dist"
pyinstaller --onefile --windowed --icon=../solstice.ico solstice.py
rmdir /s /q "build"
copy ..\solstice.png dist\
copy ..\solstice.cfg dist\
copy ..\data.zip dist\
cd ..
echo "Done!"

cd solstice
rmdir /s /q "dist"
pyinstaller --onefile --windowed --icon=../solstice.ico main.py
rmdir /s /q "build"
copy ..\solstice.png dist\
copy ..\solstice.cfg dist\
copy ..\README.md dist\
copy ..\data.zip dist\
cd ..
echo "Done!"

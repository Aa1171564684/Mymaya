pyinstaller -F "%cd%\use_thread.py" -i "D:\speed.ico"

xcopy "%cd%\dist" %cd%
echo Y|rmdir /s %cd%\build
echo Y|rmdir /s %cd%\dist

del %cd%\*.spec


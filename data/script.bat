SETLOCAL
CD /D %0\..

@ECHO off

ECHO %cd%

ECHO Copy addins to Python
xcopy /E /Y addins\* C:\Users\Jason\Anaconda3\envs\py3636\
ECHO -------------

ECHO Install PyX (This may take a while)
python -m pip install pyx

ECHO Install Kivy (This may take a while)
python -m pip install --upgrade pip wheel setuptools
python -m pip install pypiwin32
python -m pip install kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy.deps.gstreamer --extra-index-url https://kivy.org/downloads/packages/simple/
python -m pip install kivy


ECHO Installation Complete

PAUSE
ENDLOCAL
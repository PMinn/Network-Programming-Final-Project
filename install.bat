@ECHO OFF
setlocal enabledelayedexpansion

SET [ipList='']

@REM pip install eel
@REM pip install pyautogui

cd ./module
@REM  tokens=5
for /f "skip=7 delims=" %%i in ('dir') do (
	
    for %%a in (%%i) do set ipList=!ipList!%%a$
    set ipList=!ipList!#
    @REM pip install ./
)

echo %ipList%
  
pause
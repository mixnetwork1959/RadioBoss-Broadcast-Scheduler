@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "BUILD_NAME=BroadcastScheduler-4.5.0-test"
set "BUILD_DEST=%CD%\dist\%BUILD_NAME%.exe"

if not exist "scheduler.py" goto missing_input
if not exist "BroadcastScheduler.ico" goto missing_input
if not exist "tk_runtime_hook.py" goto missing_input
if not exist "templates\" goto missing_input

if exist "%BUILD_DEST%" (
    echo BUILD_ALREADY_EXISTS: "%BUILD_DEST%"
    echo Rename the existing test build before trying again. Nothing was overwritten.
    goto fail
)

py -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller is missing. Install it with:
    echo py -m pip install pyinstaller
    goto fail
)

echo Building %BUILD_NAME% with the original radio icon...
py -m PyInstaller --onefile --windowed --name "%BUILD_NAME%" --distpath "%CD%\dist" --workpath "%CD%\build\portable-test" --specpath "%CD%\build\specs" --runtime-hook "%CD%\tk_runtime_hook.py" --icon "%CD%\BroadcastScheduler.ico" --add-data "%CD%\BroadcastScheduler.ico;." --add-data "%CD%\templates;templates" "%CD%\scheduler.py"
if errorlevel 1 goto fail

if not exist "%BUILD_DEST%" (
    echo BUILD_OUTPUT_MISSING
    goto fail
)

echo.
echo BUILD_OK: "%BUILD_DEST%"
echo Test the EXE without settings.json; select the customer's SDL file.
echo The EXE is self-contained. Do NOT copy _internal.
pause
exit /b 0

:missing_input
echo BUILD_INPUT_MISSING: scheduler.py, templates, or BroadcastScheduler.ico
:fail
echo.
echo BUILD_FAILED. See the messages above.
pause
exit /b 1

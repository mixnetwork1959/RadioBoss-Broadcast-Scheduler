# BroadcastScheduler portable Windows build

## First-run behavior

- `settings.json` is created **beside the EXE**, not in the current working directory.
- `public_calendar.json` is also stored beside the EXE instead of the temporary extraction directory.
- If the configured SDL is missing or invalid, a file-picker asks for the real RadioBOSS `.sdl` file.
- `File > Open SDL...` changes the source without editing JSON or renaming the SDL.
- A cancelled picker leaves the original configuration intact.

## Build on Windows

In a clean virtual environment with Python and PyInstaller installed, open
the extracted source folder and double-click **`build_windows.cmd`**.
Unlike the optional PowerShell script, this does not require changing
PowerShell execution policies.

If PyInstaller is not installed, open a terminal there and run:

```powershell
py -m pip install pyinstaller
```

Then double-click `build_windows.cmd`. A different option is to run the command
below directly from the source folder:

```powershell
py -m pip install pyinstaller
py -m PyInstaller --noconfirm --clean --windowed --onefile --name BroadcastScheduler --runtime-hook "tk_runtime_hook.py" --icon "BroadcastScheduler.ico" --add-data "BroadcastScheduler.ico;." --add-data "templates;templates" scheduler.py
```

`BroadcastScheduler.ico` was recovered from the previously shipped Windows EXE
and contains seven sizes, from 16×16 through 256×256. Use that original radio
icon for both the executable and its application window.

Copy the single EXE from `dist`. Do not copy an old
`settings.json`, `Admin.sdl`, personal `public_calendar.json`, or previously
generated website output into a public distribution.

## Acceptance test before release

1. Start the single EXE **without** settings.json.
2. Select a copy of the supplied customer SDL; Events and Calendar must populate.
3. Test Public Calendar and Publish Website using a disposable export directory.
4. Use `File > Open SDL...` to switch to the separate Radio Albena sample;
   confirm Events and Calendar update.
5. Cancel a subsequent SDL selection and confirm the current schedule remains.
6. Restart the program from a different working directory; the saved SDL path
   must still be found.

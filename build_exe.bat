@echo off
echo Building EVE Combat Monitor...
pip install pyinstaller --quiet
pyinstaller --onefile --windowed ^
  --name "EVECombatMonitor" ^
  --add-data "ui;ui" ^
  --hidden-import "webview" ^
  --hidden-import "watchdog" ^
  --hidden-import "watchdog.observers" ^
  --hidden-import "watchdog.observers.winapi" ^
  --hidden-import "watchdog.events" ^
  main.py
echo.
echo Done! Executable is in the dist\ folder.
pause

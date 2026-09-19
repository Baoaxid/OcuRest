@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo               Building OcuRest Standalone
echo ========================================================

:: Step 1: Activate Virtual Environment
echo [1/4] Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [Error] Virtual environment not found at venv\Scripts\activate.bat
    pause
    exit /b 1
)

:: Step 2: Compile Localization
echo [2/4] Compiling localization assets...
python scripts\compile_i18n.py
if %ERRORLEVEL% NEQ 0 (
    echo [Error] Localization compilation failed.
    pause
    exit /b %ERRORLEVEL%
)

:: Step 3: Clean Previous Artifacts
echo [3/4] Cleaning previous build artifacts...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

:: Step 4: Package via PyInstaller
echo [4/4] Packaging executable with PyInstaller...
pyinstaller --noconsole --onefile ^
    --name "OcuRest" ^
    --icon "assets\icon.ico" ^
    --add-data "locales;locales" ^
    --add-data "assets;assets" ^
    --collect-all mediapipe ^
    --exclude-module scipy ^
    --exclude-module pandas ^
    main.py

if %ERRORLEVEL% NEQ 0 (
    echo [Error] PyInstaller packaging failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ========================================================
echo Build Successful! Binary located at: dist\OcuRest.exe
echo ========================================================
pause
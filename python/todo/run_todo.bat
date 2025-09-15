@echo off
echo Enhanced Todo App with Telegram Bot
echo ====================================
echo.
echo Choose an option:
echo 1. Run Desktop App (GUI)
echo 2. Run Telegram Bot Only
echo 3. Setup/Install Dependencies
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Starting Desktop App...
    python todo.py --mode gui
) else if "%choice%"=="2" (
    echo Starting Telegram Bot...
    python todo.py --mode bot
) else if "%choice%"=="3" (
    echo Running Setup...
    python setup.py
) else if "%choice%"=="4" (
    echo Goodbye!
    exit
) else (
    echo Invalid choice. Please run the script again.
)

pause

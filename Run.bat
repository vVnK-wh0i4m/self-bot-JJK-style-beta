@echo off
chcp 65001 >nul 2>&1
title HostBot v6.4
color 0D
cls

echo.
echo   =========================================
echo    HostBot v6.4 - Discord Self-Bot
echo    by QU4N.TH3.D3V
echo   =========================================
echo.

:: Kiem tra Python
where python >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found!
    echo  Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%A in ('python --version 2^>^&1') do echo  [OK] %%A
echo.

:: Tao config.json neu chua co
if not exist "config.json" (
    echo  [!] Chua co config.json
    set /p "TK=  Nhap Discord Token: "
    echo {"token":"%TK%","prefix":"."} > config.json
    echo  [OK] Da tao config.json
    echo.
)

:: Install tat ca thu vien tu requirements.txt
if exist "requirements.txt" (
    echo  [!] Dang kiem tra va cai dat thu vien...
    python -m pip install --upgrade pip --quiet 2>nul
    python -m pip install -r requirements.txt --quiet 2>nul
    if errorlevel 1 (
        echo  [WARNING] Mot so thu vien khong cai duoc, bot co the chay binh thuong.
    ) else (
        echo  [OK] Da cai dat du thu vien.
    )
    echo.
)

:: Tao thu muc music neu chua co
if not exist "music" mkdir music

:: Tao thu muc music_cache neu chua co
if not exist "music_cache" mkdir music_cache

echo  ========================================
echo   Dang khoi dong bot...
echo   (Nhan Ctrl+C de dung)
echo  ========================================
echo.

:restart
python main.py
echo.
echo  [!] Bot da dung. Dang restart sau 3 giay...
timeout /t 3 /nobreak >nul
goto restart

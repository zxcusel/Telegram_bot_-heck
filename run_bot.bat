@echo off
title Telegram Bot Runner (Auto-Restart)
chcp 65001 > nul

:loop
echo [%date% %time%] Starting Telegram Bot...
python main.py
echo [%date% %time%] Bot exited or crashed. Restarting in 5 seconds...
timeout /t 5
goto loop

@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\.gemini\skills\browser-login\scripts\run.ps1" %*
exit /b %ERRORLEVEL%

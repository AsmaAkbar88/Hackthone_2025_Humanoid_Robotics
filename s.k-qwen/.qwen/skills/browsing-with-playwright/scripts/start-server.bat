@echo off
REM Start Playwright MCP server for browser-use skill
REM Usage: start-server.bat [port]

set PORT=%1
if "%PORT%"=="" set PORT=8808
set PID_FILE=%TEMP%\playwright-mcp-%PORT%.pid

echo Starting Playwright MCP server on port %PORT%...

REM Start server in background
start /B npx @playwright/mcp@latest --port %PORT% --shared-browser-context

REM Save PID
for /f "tokens=2" %%i in ('tasklist /FI "WINDOWTITLE eq npx*" /NH') do (
    echo %%i > "%PID_FILE%"
)

timeout /t 2 /nobreak >nul

echo Playwright MCP started on port %PORT%
echo To stop: stop-server.bat
echo To verify: python verify.py

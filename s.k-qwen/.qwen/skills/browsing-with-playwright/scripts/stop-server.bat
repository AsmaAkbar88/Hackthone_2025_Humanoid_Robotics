@echo off
REM Stop Playwright MCP server gracefully
REM Usage: stop-server.bat [port]

set PORT=%1
if "%PORT%"=="" set PORT=8808
set PID_FILE=%TEMP%\playwright-mcp-%PORT%.pid

echo Stopping Playwright MCP server on port %PORT%...

REM First, close the browser gracefully via MCP
python mcp-client.py call -u http://localhost:%PORT% -t browser_close -p "{}" 2>nul

REM Wait a moment
timeout /t 1 /nobreak >nul

REM Kill any remaining Playwright MCP processes
taskkill /F /FI "WINDOWTITLE eq npx*" 2>nul
taskkill /F /IM node.exe 2>nul | findstr /i "playwright" 2>nul

REM Clean up PID file
if exist "%PID_FILE%" del "%PID_FILE%"

echo Playwright MCP server stopped

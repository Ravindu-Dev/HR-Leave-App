@echo off
setlocal
echo ==========================================
echo   Smart Leave System - Database Setup
echo ==========================================
echo.
echo This script attempts to create the database 'smart_leave_db' automatically.
echo It assumes the user is 'postgres' and password is 'password'.
echo.

REM HARDCODED: PostgreSQL password for database creation
REM WARNING: This is the default development password. Change in production!
set PGPASSWORD=password

REM HARDCODED: Common PostgreSQL installation paths for versions 13-17
REM Searches these directories to find the createdb.exe utility
set "PG_PATHS=C:\Program Files\PostgreSQL\17\bin;C:\Program Files\PostgreSQL\16\bin;C:\Program Files\PostgreSQL\15\bin;C:\Program Files\PostgreSQL\14\bin;C:\Program Files\PostgreSQL\13\bin"

:: Try to find createdb in the paths
for %%P in ("%PG_PATHS:;=" "%") do (
    if exist "%%~P\createdb.exe" (
        echo Found PostgreSQL at: %%~P
        REM HARDCODED: Creating database 'smart_leave_db' with user 'postgres'
        "%%~P\createdb.exe" -U postgres smart_leave_db
        if errorlevel 0 (
            echo.
            echo [SUCCESS] Database 'smart_leave_db' created!
            goto end
        ) else (
            echo [ERROR] Found tool but failed to create database. 
            echo Check if database already exists or password is correct.
        )
        goto end
    )
)

echo.
echo [FAILED] Could not find PostgreSQL installation or 'createdb.exe'.
echo Please create the database manually using pgAdmin.
echo.

:end
echo.
pause

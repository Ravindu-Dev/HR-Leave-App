@echo off
setlocal
echo ==========================================
echo   Smart Leave System - Database Setup
echo ==========================================
echo.
echo This script attempts to create the database 'smart_leave_db' automatically.
echo It assumes the user is 'postgres' and password is 'password'.
echo.

:: Set the password environment variable for the session
set PGPASSWORD=password

:: List of common PostgreSQL bin paths
set "PG_PATHS=C:\Program Files\PostgreSQL\17\bin;C:\Program Files\PostgreSQL\16\bin;C:\Program Files\PostgreSQL\15\bin;C:\Program Files\PostgreSQL\14\bin;C:\Program Files\PostgreSQL\13\bin"

:: Try to find createdb in the paths
for %%P in ("%PG_PATHS:;=" "%") do (
    if exist "%%~P\createdb.exe" (
        echo Found PostgreSQL at: %%~P
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

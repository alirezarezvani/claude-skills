@echo off
REM
REM Codex Installation Script for Claude Skills Library (Windows)
REM
REM Installs skills from this repository to your local Codex skills directory.
REM Uses direct copy (no symlinks) for Windows compatibility.
REM
REM Usage:
REM   scripts\codex-install.bat [--all | --skill <name>]
REM
REM Options:
REM   --all             Install all skills (default)
REM   --skill <name>    Install a single skill by name
REM   --list            List available skills
REM   --help            Show this help message
REM

setlocal enabledelayedexpansion

REM Configuration
set "CODEX_SKILLS_DIR=%USERPROFILE%\.codex\skills"
set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%.."
set "CODEX_SKILLS_SRC=%REPO_ROOT%\.codex\skills"
set "CODEX_INDEX=%REPO_ROOT%\.codex\skills-index.json"

REM Check for help
if "%1"=="--help" goto :show_help
if "%1"=="-h" goto :show_help

REM Check prerequisites
if not exist "%CODEX_SKILLS_SRC%" (
    echo [ERROR] Codex skills directory not found: %CODEX_SKILLS_SRC%
    echo [INFO] Run 'python scripts\sync-codex-skills.py' first to generate structure.
    exit /b 1
)

REM Parse arguments
set "MODE=all"
set "TARGET="

:parse_args
if "%1"=="" goto :run_mode
if "%1"=="--all" (
    set "MODE=all"
    shift
    goto :parse_args
)
if "%1"=="--skill" (
    set "MODE=skill"
    set "TARGET=%2"
    shift
    shift
    goto :parse_args
)
if "%1"=="--list" (
    set "MODE=list"
    shift
    goto :parse_args
)
echo [ERROR] Unknown option: %1
goto :show_help

:run_mode
echo.
echo ========================================
echo   Claude Skills - Codex Installer
echo   (Windows Version)
echo ========================================
echo.

if "%MODE%"=="list" goto :list_skills
if "%MODE%"=="skill" goto :install_skill
if "%MODE%"=="all" goto :install_all
goto :end

:list_skills
echo Available skills:
echo.
for /d %%i in ("%CODEX_SKILLS_SRC%\*") do (
    if exist "%%i\SKILL.md" (
        echo   - %%~ni
    )
)
goto :end

:install_skill
if "%TARGET%"=="" (
    echo [ERROR] Skill name required
    exit /b 1
)

set "SKILL_SRC=%CODEX_SKILLS_SRC%\%TARGET%"
set "SKILL_DEST=%CODEX_SKILLS_DIR%\%TARGET%"

if not exist "%SKILL_SRC%" (
    echo [ERROR] Skill not found: %TARGET%
    exit /b 1
)

if not exist "%SKILL_SRC%\SKILL.md" (
    echo [ERROR] Invalid skill (no SKILL.md): %TARGET%
    exit /b 1
)

echo [INFO] Installing skill: %TARGET%

REM Create destination directory
if not exist "%CODEX_SKILLS_DIR%" mkdir "%CODEX_SKILLS_DIR%"

REM Remove existing
if exist "%SKILL_DEST%" rmdir /s /q "%SKILL_DEST%"

REM Copy skill
xcopy /e /i /q "%SKILL_SRC%" "%SKILL_DEST%"

echo [SUCCESS] Installed: %TARGET%
goto :end

:install_all
echo [INFO] Installing all skills to: %CODEX_SKILLS_DIR%
echo.

set "INSTALLED=0"
set "FAILED=0"

if not exist "%CODEX_SKILLS_DIR%" mkdir "%CODEX_SKILLS_DIR%"

for /d %%i in ("%CODEX_SKILLS_SRC%\*") do (
    if exist "%%i\SKILL.md" (
        set "SKILL_NAME=%%~ni"
        set "SKILL_DEST=%CODEX_SKILLS_DIR%\%%~ni"

        echo [INFO] Installing: %%~ni

        if exist "!SKILL_DEST!" rmdir /s /q "!SKILL_DEST!"

        xcopy /e /i /q "%%i" "!SKILL_DEST!" >nul

        if errorlevel 1 (
            echo [ERROR] Failed to install: %%~ni
            set /a FAILED+=1
        ) else (
            set /a INSTALLED+=1
        )
    )
)

echo.
echo [INFO] Installation complete: !INSTALLED! installed, !FAILED! failed
echo.
echo [SUCCESS] Skills installed to: %CODEX_SKILLS_DIR%
goto :end

:show_help
echo.
echo Codex Installation Script for Claude Skills Library (Windows)
echo.
echo Usage:
echo   scripts\codex-install.bat [--all ^| --skill ^<name^>]
echo.
echo Options:
echo   --all             Install all skills (default)
echo   --skill ^<name^>    Install a single skill by name
echo   --list            List available skills
echo   --help            Show this help message
echo.
echo Examples:
echo   scripts\codex-install.bat
echo   scripts\codex-install.bat --skill content-creator
echo   scripts\codex-install.bat --list
goto :end

:end
endlocal

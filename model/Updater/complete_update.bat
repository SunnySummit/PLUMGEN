@echo off
setlocal enabledelayedexpansion

REM pause for 1 second ---------------------------------------------
timeout /t 3 >nul

REM Set the script's directory explicitly --------------------------
set "script_dir=%~dp0"
cd /d "%script_dir%"

REM find and move to target directory ------------------------------
set "target_dir=%script_dir%\_PLUMGEN"
set "plumgen_dir=%script_dir%\..\..\"
set "model_dir=%script_dir%\..\"

if exist "%target_dir%" (
    cd /d "%target_dir%"

    REM check and move files ---------------------------------------
    if exist "%target_dir%\*.xml" (
        robocopy "%target_dir%" "%model_dir%" *.xml /MOV
        echo Moved XML files from "%target_dir%" to "%model_dir%"
    ) else (
        echo NOTE: No XML files found in "%target_dir%". Probably no issue.
    )

    if exist "%target_dir%\*.py" (
        robocopy "%target_dir%" "%plumgen_dir%" *.py /MOV
        echo Moved py files from "%target_dir%" to "%plumgen_dir%"
    ) else (
        echo NOTE: No PY files found in "%target_dir%"
    )

    if exist "%target_dir%\*.conf" (
        robocopy "%target_dir%" "%plumgen_dir%" *.conf /MOV
        echo Moved conf files from "%target_dir%" to "%plumgen_dir%"
    ) else (
        echo NOTE: No CONF files found in "%target_dir%"
    )

    if exist "%target_dir%\*.dll" (
        robocopy "%target_dir%" "%plumgen_dir%" *.dll /MOV
        echo Moved dll files from "%target_dir%" to "%plumgen_dir%"
    ) else (
        echo NOTE: No DLL files found in "%target_dir%"
    )

    if exist "%target_dir%\*.txt" (
        robocopy "%target_dir%" "%plumgen_dir%" *.txt /MOV
        echo Moved txt files from "%target_dir%" to "%plumgen_dir%"
    ) else (
        echo NOTE: No TXT files found in "%target_dir%"
    )

    if exist "%target_dir%\_PLUMGEN.exe" (
        robocopy "%target_dir%" "%plumgen_dir%" _PLUMGEN.exe /MOV
        echo Moved _PLUMGEN.exe from "%target_dir%" to "%plumgen_dir%"
    ) else (
        echo NOTE: _PLUMGEN.exe not found in "%target_dir%"
    )

    REM check and move directories ---------------------------------
    if exist "%target_dir%\Lua Parts" (
        robocopy "%target_dir%\Lua Parts" "%plumgen_dir%\Lua Parts" *.* /E /MOV
        echo Moved Lua Parts contents from "%target_dir%" to "%plumgen_dir%"
    ) else (
        echo NOTE: Lua Parts not found in "%target_dir%"
    )

    if exist "%target_dir%\Defaults Json" (
        robocopy "%target_dir%\Defaults Json" "%plumgen_dir%\Defaults Json" *.* /E /MOV
        echo Moved Defaults Json contents from "%target_dir%" to "%plumgen_dir%"
    ) else (
        echo NOTE: Defaults Json not found in "%target_dir%"
    )

    if exist "%target_dir%\Share" (
        robocopy "%target_dir%\Share" "%plumgen_dir%\Share" *.* /E /MOV
        echo Moved Share contents from "%target_dir%" to "%plumgen_dir%"
    ) else (
        echo NOTE: Share not found in "%target_dir%"
    )

    if exist "%target_dir%\lib" (
        robocopy "%target_dir%\lib" "%plumgen_dir%\lib" *.* /E /MOV
        echo Moved lib contents from "%target_dir%" to "%plumgen_dir%"
    ) else (
        echo NOTE: lib not found in "%target_dir%"
    )

    REM wait 1 second then run _PLUMGEN.exe if it exists -----------
    timeout /t 1 /nobreak >nul
    if exist "%plumgen_dir%\_PLUMGEN.exe" (
        cd /d "%plumgen_dir%"
        "_PLUMGEN.exe"
        echo Running _PLUMGEN.exe
    ) else (
        echo _PLUMGEN.exe not found in "%plumgen_dir%"
    )

) else (
    echo Either: Do not run this alone. OR: PLUMGEN folder not found in Model\Updater.
)

pause
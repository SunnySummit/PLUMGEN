@echo off
setlocal


REM pause for 2 seconds-----------------------------------------
timeout /t 2 >nul


REM define source and destination directories-------------------
set "source_dir=%cd%"
set "plumgen_dir=%cd%\..\.."
set "model_dir=%cd%\.."


REM check if files exist before moving -------------------------
if exist "%source_dir%\*.xml" (
    move "%source_dir%\*.xml" "%model_dir%"
    echo Moved XML files from "%source_dir%" to "%model_dir%"
) else ( echo Note: No XML files found in "%source_dir%". Probably not an issue. )

if exist "%source_dir%\*.py" (
    move "%source_dir%\*.py" "%plumgen_dir%"
    echo Moved py files from "%source_dir%" to "%plumgen_dir%"
) else ( echo Note: No PY files found in "%source_dir%" )

if exist "%source_dir%\*.conf" (
    move "%source_dir%\*.conf" "%plumgen_dir%"
    echo Moved conf files from "%source_dir%" to "%plumgen_dir%"
) else ( echo Note: No CONF files found in "%source_dir%" )

if exist "%source_dir%\*.dll" (
    move "%source_dir%\*.dll" "%plumgen_dir%"
    echo Moved dll files from "%source_dir%" to "%plumgen_dir%"
) else ( echo Note: No DLL files found in "%source_dir%" )

if exist "%source_dir%\*.txt" (
    move "%source_dir%\*.txt" "%plumgen_dir%"
    echo Moved txt files from "%source_dir%" to "%plumgen_dir%"
) else ( echo Note: No TXT files found in "%source_dir%" )


REM check if folders exist before moving -----------------------
if exist "%source_dir%\Lua Parts" (
    move "%source_dir%\Lua Parts" "%plumgen_dir%"
    echo Moved Lua Parts from "%source_dir%" to "%plumgen_dir%"
) else ( echo Note: Lua Parts not found in "%source_dir%" )

if exist "%source_dir%\Defaults Json" (
    move "%source_dir%\Defaults Json" "%plumgen_dir%"
    echo Moved Defaults Json from "%source_dir%" to "%plumgen_dir%"
) else ( echo Note: Defaults Json not found in "%source_dir%" )

if exist "%source_dir%\Share" (
    move "%source_dir%\Share" "%plumgen_dir%"
    echo Moved Share from "%source_dir%" to "%plumgen_dir%"
) else ( echo Note: Share not found in "%source_dir%" )

if exist "%source_dir%\lib" (
    move "%source_dir%\lib" "%plumgen_dir%"
    echo Moved lib from "%source_dir%" to "%plumgen_dir%"
) else ( echo Note: lib not found in "%source_dir%" )


:end
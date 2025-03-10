from cx_Freeze import setup, Executable
import sys
import os

# create empty directories, move these to child folder
empty_dirs = [
    "build/_BIOMES Xmls Folder Goes Here",
    "build/__Exported Mod Files"
]

for dir_name in empty_dirs:
    os.makedirs(dir_name, exist_ok=True)


build_options = {
    "include_files": [
        #("controller", "controller"), # not needed
        #("view", "view"),
        #("Resources", "Resources"),
        ("EMPTY_latest_versions.json", "Resources/latest_versions.json"), # replaces with blank one
        #("EMPTY_plum_extract_biomes.xml", "Resources/plum_extract_biomes.xml"), # replaces with blank one
        ("Resources/filename_hashes.json", "Resources/filename_hashes.json"),
        #("Resources/psarc.exe", "Resources/psarc.exe"),
        ("Resources/Updater/complete_update.bat", "Resources/Updater/complete_update.bat"),
        ("logging.conf", "logging.conf"),
        ("logger_config.py", "logger_config.py"),
        ("README.md", "README.md"),
        ("LICENSE", "LICENSE"),
        ("_Extracted Vanilla Game Files/DO_NOT_CHANGE_ANY_FILES_HERE.txt", "_Extracted Vanilla Game Files/DO_NOT_CHANGE_ANY_FILES_HERE.txt"),
        
        ("images", "Images"),
        ("_Biome Templates", "_Biome Templates"),
        ("_Presets", "_Presets"),
        ("Defaults Json", "Defaults Json"),
        ("Lua Parts", "Lua Parts"),
    ],
    
    "excludes": ['__pycache__', 'turtle.jpg'],
    "packages": ["tkinter", "lxml", "requests"],
}
 
base = 'Win32GUI' if sys.platform=='win32' else None #Win32GUI #Console <- to debug stuff

icon_file = "images/plum_icon_cc0_og.ico"

executables = [
    Executable("PLUMGEN_main.py", base=base, target_name="_PLUMGEN.exe", icon=icon_file)
]

setup(
    name="_PLUMGEN",
    version="1.3",
    description="PLUMGEN",
    options={'build_exe': build_options},
    executables=executables
)

#install cx_freeze, then run: python setup.py build
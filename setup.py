from cx_Freeze import setup, Executable
import sys
import os

# create empty directories, move these to child folder
empty_dirs = [
    "build/_BIOMES Exmls Folder Goes Here",
    "build/__Exported Mod Files"
]

for dir_name in empty_dirs:
    os.makedirs(dir_name, exist_ok=True)


build_options = {
    "include_files": [
        #("controller", "controller"), # not needed
        #("view", "view"),
        #("model", "model"),
        ("EMPTY_latest_mbc_version.json", "Model/latest_mbc_version.json"), # replaces with blank one
        ("EMPTY_plum_extract_biomes.xml", "Model/plum_extract_biomes.xml"), # replaces with blank one
        ("model/psarc.exe", "Model/psarc.exe"),
        ("logging.conf", "logging.conf"),
        ("logger_config.py", "logger_config.py"),
        ("_README.txt", "_README.txt"),
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
    version="1.0",
    description="PLUMGEN",
    options={'build_exe': build_options},
    executables=executables
)

#install cx_freeze, then run: python setup.py build
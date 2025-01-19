# Plumgen (v1.2)

[![License](https://img.shields.io/github/license/SunnySummit/PLUMGEN)](https://github.com/SunnySummit/PLUMGEN/blob/main/LICENSE)
[![Downloads](https://img.shields.io/github/downloads/SunnySummit/PLUMGEN/total.svg)](https://github.com/SunnySummit/PLUMGEN/releases)
[![Stars](https://img.shields.io/github/stars/SunnySummit/PLUMGEN)](https://github.com/SunnySummit/PLUMGEN/stargazers)
[![Issues](https://img.shields.io/github/issues/SunnySummit/PLUMGEN)](https://github.com/SunnySummit/PLUMGEN/issues)
[![Version](https://img.shields.io/github/v/release/SunnySummit/PLUMGEN)](https://github.com/SunnySummit/PLUMGEN/releases)

### App Features

+ Make a detailed & aesthetically pleasing biome mod in as little as 30 seconds.
+ IMPORT and merge multiple biome mods.
+ Bulk replace OR multiply flora traits (scale, density, etc).
+ Auto-rename and auto-add biomes to sub-biomes (for spawning).
+ EXPORT directly to PAK, EXML, MBIN, and LUA (AMUMSS optional).
+ "LUA-ize" or remix almost any biome mod.
+ Save and share individual biomes (JSON files).
+ Validates all input and data = stable mods.
+ Exhaustive error handling and logging (all done locally).
+ Responsive and intuitive interface.
+ And more!

### Changelog

<details>

#### Update v1.2:

+ Reworked the 'Add Biome' button to create more aesthetically pleasing and detailed biomes.
    + Instead of adding 4 completely random props to a biome, now, 9-14 props can be added, all based on a similar biome category.
    + Before, what a biome used to look like:
		+ Huge crystal, cactus, toxic plant, lush grass
    + After v1.2:
		+ Large fan shroom, huge bounder, large blue shroom, medium boulder02, medium blue shroom,
			medium bounder01, small boulder, lush grass, small shroom cluster, decorative gravel
    + This basically categorizes each new biome into 1 (or more) of 25 categories (lush, frozen, etc), and only grabs new props from a similar pool.
    + More details:
		+ 25% chance of adding 1 distant prop - biggest props & can be a huge eyesore if added to every planet.
		+ 2-3 landmark props
		+ 3-4 objects
		+ 4-6 detail objects
+ Changed 'Auto-add Biome Objects to Tiles' menu item to sort more biomes, like biomes with Nevada and Alpine props.
+ Removed many huge props with short LODs from several CSVs (Vanilla+Pre NMS & FoundPathAtlas).

#### Update v1.12:

+ New dropdown menu item (File > Bulk Import & Update) for bulk updating many BIOMES folders separately in '_BIOMES Exmls Folder Goes Here' directory.
    + Video demo: https://www.youtube.com/watch?v=LbyHlvXGZXM
+ New export draw distance option for better performance: 'Near'. Can be used for biomes with demanding/high res custom models.
+ Added support for new prop attribute: 'Type'. Two values for this attribute: 'Instanced' or 'Single'.
    + Type is an obfuscated attribute which controls e.g. whether props despawn on slopes or if a floating prop has collisions.

Update v1.11.1b: Fix for importing outdated after-NEXT biomes.

#### Update v1.11.1a:

+ Fixed bulk editing certain prop attributes, like "Coverage."
+ Support for auto-renaming and auto-adding new 'Worlds Part 1' biomes.
+ Fixed issue with making a biome template (.csv) with outdated after-NEXT biomes.
+ Misc. bug fixes.

#### Update v1.11:

+ Updated to "Worlds Part 1"
    + Added support for 4 new prop attributes: MaxYRotation, MaxRaise, MaxLower & IsFloatingIsland.
    + Updated each biome .csv ("v2" in filename), added 'Worlds Part 1.csv' biome template - includes newest props.
    + Automatically updates old biome objects files, biome files, and presets.

#### Update v1.1:

+ New Update menu item - Fetches and downloads latest PLUMGEN update. You no longer have to manually download updates.
+ Added support for 10 languages - Reworked all text elements, translated each via. DeepL (take these with a grain of salt). ;)
    + These include: Chinese-Simplified, English, Finnish, French, German, Italian, Japanese, Korean, Portuguese, Russian, Spanish
+ Fixed issue - Bug preventing bulk editing model paths.
+ Readme clarifications.
+ Security improvements.
+ New prompt asking to download latest MBINCompiler update - You can export offline or continue modding with outdated NMS/MBINCompiler versions.

#### Full Release v1.0:

+ Overhauled exporting. AMUMSS no longer required. You can now export directly to .PAK using PLUMGEN's new efficient export system.
    + 10x faster export time vs. LUA - Exporting 20,000+ biomes now takes ~3 minutes, compared to 30+ minutes via. LUA/AMUMSS. [1]
    + Improved stability - PLUMGEN's new export to PAK system is highly resilient against game updates. [2]
    + Export all files - EXMLs, MBINs, LUAs, and PAKs. Immediately locate and import exported modded biomes/EXMLs.
    + Automatic updates - Exporting fetches latest MBINCompiler and extracts vanilla game files = easily mod vanilla biomes too.
    + Enhanced custom sub-biome support - Replicate modded or even *outdated* sub-biomes with a new export menu (should the issue arise).
    + LUA now optional - Exporting still generates 2 LUA files, but making use of them (via. AMUMSS) is now optional.
    + Please see updated 'Requirements' and 'Exporting Info' sections below for more info.

	*[1] lxml wraps around C libraries = highly optimized EXML parsing/processing. Plus, I just understand Python better than I do LUA.

	*[2] lxml follows XML standards for syntax, structure, & validation. This improves long-term EXML compatibility with NMS updates.

</details>

### Requirements

+ **[Required]** Download .NET 6 - Select appropriate download under "Run desktop apps"
	https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime

+ [*Optional*] PLUMGEN generates .LUA scripts too. AMUMSS is needed to make use of these .LUA scripts. AMUMSS Guide:
	https://www.nexusmods.com/nomanssky/mods/2626

### Exporting Details

After exporting, you'll find a folder inside '__Exported Mod Files' containing:

+ PAKs - Your mods. How to install mods: https://nomanssky.fandom.com/wiki/Mods#Summary
+ EXMLs - Look for any 'BIOMES' (or 'CUSTOMBIOMES') folder -> copy it to PLUMGEN's '_BIOMES Exmls Folder Goes Here' -> import. [1]
+ MBINs - Compiled EXMLs.
+ LUAs - To be used with AMUMSS (optional). [2]

	*[1] If you have multiple BIOMES or CUSTOMBIOMES:  Rename the others, e.g. BIOMES2, BIOMES3, etc. PLUMGEN can auto-merge multiple mods via. this method: https://youtu.be/zzaeyRAobOQ?t=867

	*[2] Spawner LUA may throw errors if you use any custom 'sub-biomes' (PLUMGEN's PAKs are designed to avoid this issue). Watch video^ for more info.


### Known Issues

+ Using 'Reset Auto-Rename' on a filepath with multiple underscores can erase almost all of the path's name.
+ If a link opens a *new* browser, then you quit PLUMGEN, the app will stay active until you quit the browser.
    + This does not happen when your browser is *already* open. This issue seems to occur when creating the EXE via. cx_Freeze.



### Q&A/Troubleshooting

<details>

+ When running the app, I encounter a window that says, "Windows protected your PC"

Click "More info" -> "Run anyway." This is a false flag from your antivirus. PLUMGEN is safe to use. You can view the source code on github.

+ Is this difficult to learn?

In my (100% unbiased) opinion, no. You do not need any programming or scripting knowledge to use PLUMGEN. Nearly everything is done via. a graphical interface.

+ Is this a paid app?

No, although donations are accepted.

+ Will my exported biome mod break after game updates?

If it breaks, import your mod and export it again. Note: wait for MBINCompiler update after game updates ([check here for updates](https://github.com/monkeyman192/MBINCompiler/releases)). 

Although rare, if a new game update fundamentally changes game structure/biome files, wait for a PLUMGEN update. Check for updates via the top "Update" menu item.

+ The PLUMGEN window looks blurry and parts are cut-off by the edge of the window, like the tooltip.

This shouldn't happen after v1.0. If it does, please let me know.
	
+ I changed the language, and now text elements appear cut off, like the tooltip/info box.

Simply expand the window. This should let you see the rest of the text. Some translations require more space than the English version.
	
+ Some translations are not accurate.

Yeah, I used DeepL and a few other machine learning sources to translate. Consider opening an issue on github with any suggested improvements. :)

</details>

### Need Help?

- Video Tutorial - FYI this predates v1.0 which added the ability to export directly to PAK:
	https://www.youtube.com/watch?v=zzaeyRAobOQ

- If you encounter issues, please report them on nexus mods or github with full details and the plumgen.log file. Images or videos are always appreciated: https://github.com/SunnySummit/



### Credits & Acknowledgements

+ PSARC Archive Tool - Decompiles PAK files to MBIN
+ [MBINCompiler](https://github.com/monkeyman192/MBINCompiler/) - Decompiles MBIN files to EXML
+ [lxml](https://lxml.de/index.html) - Parses EXML files
+ [cx_Freeze](https://pypi.org/project/cx-Freeze/) - Creates executables, high performance, cross-platform



### Disclaimer/Notes

+ PLUMGEN lets you import and mod almost any biomes. Always seek permission before distributing others' work.
+ Note: If a mod author grants you permission to share their work, they cannot later retract it, per Nexus Mods rules.
+ Do not restrict permissions on any present or past *vanilla* game biomes using PLUMGEN (not including changes to prop attributes).



### Other

Give a tip 🍻 - Easy and secure transactions using *Buy Me A Coffee* & *Stripe*. No pressure whatsoever :) https://buymeacoffee.com/sunnysummit

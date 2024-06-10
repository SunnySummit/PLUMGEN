PLUMGEN (v1.1)

-- APP FEATURES: --------------------------------------------------------------------------------------------------

	-Make a biome mod in as little as 30 seconds.
	-IMPORT and merge multiple biome mods.
	-Bulk replace OR multiply flora traits (scale, density, etc).
	-Auto-rename and auto-add biomes to sub-biomes (for spawning).
	-EXPORT directly to PAK, EXML, MBIN, and LUA (AMUMSS optional).
	-"LUA-ize" or remix almost any biome mod.
	-Save and share individual biomes (JSON files).
	-Validates all input and data = very stable mods.
	-Exhaustive error handling and logging (all done locally), helps fix app issues quickly.
	-Responsive and intuitive interface, anyone can learn how to make badass biome mods!
	-And more!



-- CHANGELOG: -----------------------------------------------------------------------------------------------------

v1.1 Update:

	-Added support for 10 languages - reworked all text elements, translated them via. DeepL (take these with a grain of salt) ;)
		(Chinese-Simplified, English, Finnish, French, German, Italian, Japanese, Korean, Portuguese, Russian, & Spanish)
	-Fixed issue - Bug preventing bulk editing model SCENE paths.
	-Readme clarifications - e.g. how to update biome mods in Q&A section.


v1.0 Full Release:

	-Overhauled exporting. AMUMSS no longer required. You can now export directly to .PAK using PLUMGEN's new, very efficient export system.

		-10x faster export time vs. LUA - Exporting 20,000+ biomes now takes ~3 minutes, compared to 30+ minutes via. LUA/AMUMSS. [1]
		-Improved stability - PLUMGEN's new export to PAK system is highly resilient against game updates. [2]
		-Export all files - EXMLs, MBINs, LUAs, and PAKs. Immediately locate and import exported modded biomes/EXMLs.
		-Automatic updates - Exporting fetches latest MBINCompiler and extracts vanilla game files = easily mod vanilla biomes too.
		-Enhanced custom sub-biome support - Replicate modded or even *outdated* sub-biomes with a new export menu (should the issue arise).
		-LUA now optional - Exporting still generates 2 LUA files, but making use of them (via. AMUMSS) is now optional.
		-Please see updated 'Requirements' and 'Exporting Info' sections below for more info.

		*[1] lxml wraps around C libraries = extremely well-optimized EXML parsing/processing. Plus, I just know Python better than LUA.
		*[2] lxml follows XML standards for syntax, structure, & validation. This improves long-term EXML compatibility with NMS updates.



-- *NEW* v1.0 REQUIREMENTS: --------------------------------------------------------------------------------------

	-[Required] Download .NET 6 - Select appropriate download under "Run desktop apps"
	https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime

	-[Optional] PLUMGEN generates .LUA scripts too. AMUMSS is needed to make use of these .LUA scripts. AMUMSS Guide:
	https://www.nexusmods.com/nomanssky/mods/2626



-- *NEW* v1.0 EXPORTING INFO: ------------------------------------------------------------------------------------

	After exporting, you'll find a folder inside '__Exported Mod Files' containing:

	-PAKs - Your mods. How to install mods: https://nomanssky.fandom.com/wiki/Mods#Summary
	-EXMLs - Look for any 'BIOMES' (or 'CUSTOMBIOMES') folder -> copy it to PLUMGEN's '_BIOMES Exmls Folder Goes Here' -> import. [1]
	-MBINs - Compiled EXMLs.
	-LUAs - To be used with AMUMSS (optional). [2]

	*[1] - If you have multiple BIOMES or CUSTOMBIOMES: 
		Rename the others, e.g. BIOMES2, BIOMES3, etc. PLUMGEN can auto-merge multiple mods via. this method: https://youtu.be/zzaeyRAobOQ?t=867
	*[2] - Spawner LUA may throw errors if you use any custom 'sub-biomes' (PLUMGEN's PAKs are designed to avoid this issue). Watch video^ for more info.



-- KNOWN ISSUES: -------------------------------------------------------------------------------------------------

	-Using 'Reset Auto-Rename' on a filepath with multiple underscores can erase almost all of the path's name.
	-If a link opens a *new* browser, then you quit PLUMGEN, the app will stay active until you quit the browser.
		-This does not happen when your browser is *already* open. This issue seems to occur when creating the EXE via. cx_Freeze.



-- Q&A/TROUBLESHOOTING -------------------------------------------------------------------------------------------

	-When running the app, I encounter a window that says, "Windows protected your PC"
	Click "More info" -> "Run anyway." This is a false flag from your antivirus. PLUMGEN is safe to use. You can view the source code on github.

	-Is this difficult to learn?
	In my (100% unbiased) opinion, no. You do not need any programming or scripting knowledge to use PLUMGEN. Nearly everything is done via. a graphical interface.

	-Is this a paid app?
	No, although donations are accepted.

	-Will my exported biome mod break after game updates?
	If it breaks, import your mod and export it again. Note: wait for MBINCompiler to update after game updates (see: https://github.com/monkeyman192/MBINCompiler/releases). 
	Although rare, if a new game update fundamentally changes game structure or biome files, wait for a PLUMGEN update, then download the app again.

	-The PLUMGEN window looks blurry and parts are cut-off by the edge of the window, like the tooltip.
	This shouldn't happen after v1.0. If it does, please let me know.

	Others: TBD.



-- NEED HELP? ----------------------------------------------------------------------------------------------------

	Video Tutorial - This predates v1.0 which added the ability to export directly to PAK:
	https://www.youtube.com/watch?v=zzaeyRAobOQ

	If you encounter issues, please report them on github with full details and the plumgen.log file. Niceties are appreciated:
	https://github.com/SunnySummit/



-- CREDITS & ACKNOWLEDGEMENTS: -----------------------------------------------------------------------------------

	-PSARC Archive Tool - Decompiles PAK files to MBIN
	-MBINCompiler - Decompiles MBIN files to EXML - https://github.com/monkeyman192/MBINCompiler/
	-lxml - Parses EXML files - https://lxml.de/index.html
	-cx_Freeze - Creates executables, high performance, cross-platform - https://pypi.org/project/cx-Freeze/



-- DISCLAIMER/NOTES: ---------------------------------------------------------------------------------------------

	-PLUMGEN lets you import and mod almost any biomes. Always seek permission before distributing others' work.
	-Note: If a mod author grants you permission to share their work, they cannot later retract it, per Nexus Mods rules.
	-Do not restrict permissions on any present or past *vanilla* game biomes using PLUMGEN (not including changes to prop attributes).



-- OTHER: --------------------------------------------------------------------------------------------------------

	Support me via. Buy Me A Coffee - Uses Stripe for easy and secure transaction. Anonymous donations accepted (email address visible to me).
	https://buymeacoffee.com/sunnysummit
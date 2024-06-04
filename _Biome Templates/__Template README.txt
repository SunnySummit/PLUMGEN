WHAT THIS IS:

	Info on creating and organizing custom .CSV 'Biome Templates' to use in PLUMGEN + disclaimers

HOW TO USE:

		1. Decompile .MBIN files to .EXML files within one or more BIOMES folder(s)
			A. Place .PAK into AMUMSS 'ModScript' folder and run BUILDMOD.bat, then navigate to:
			\TOOLS\UNPACKED_DECOMPILED_PAKs\ and find something like \EXMLFILES_PAK\METADATA\SIMULATION\SOLARSYSTEM\BIOMES
			B. using psarc and MBINCompiler to extract vanilla files:
			-Post-NEXT = NMSARC.Precache.pak
			-Pre-NEXT = NMSARC.515F1D3.pak
			C. Or use Modding Station (or another tool) to unpack all of your game files
		2. Place BIOMES directory (filled with EXML files) in 'BIOMES_EXMLs_Folder_Goes_Here' folder
		3. Run PLUMGEN, then click 'File' > 'Make Biome Template'
		4. Done! Select the new template from the dropdown menu!
			-When opening the resulting .CSV, if Excel prompts you to convert to scientific notation, select 'Don't Convert'
			-To sort the data: Go to 'Data' tab > 'Sort' > sort by: 'Filename' > OK.
			-Don't worry about replacing '\' or '/' characters, PLUMGEN handles this.

	-**IMPORTANT: After sorting the data, verify there are no empty cells.
		-If you find rows with any empty cells: Select the entire row(s) > Right click > 'Clear contents'
		-(empty cells could cause issues)
	
LINKS:
	
	MBINCompiler - https://github.com/monkeyman192/MBINCompiler/releases
	Modding Station - https://www.nexusmods.com/nomanssky/mods/320
	Psarc comes with PLUMGEN via. 'model' folder

DISCLAIMERS:

	-PLUMGEN creates templates from biome object MBINs (with "GcObjectSpawnData.xml")
	-It does not convert non-biome object MBINs, it does not updated outdated models to current NMS.
	-Old mods typically reference outdated or broken 3rd-party models,
		PLUMGEN uses default model paths (via. PLUMGEN_model_gen.py) to automatically use updated models by default.
		(Debugging crashes due to broken models in NMS is very not fun)
	-Also, making a BT from pre-NEXT biomes might have missing values in DestroyedByPlayerShip column, double check these.
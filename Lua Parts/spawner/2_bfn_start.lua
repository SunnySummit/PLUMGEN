

NMS_MOD_DEFINITION_CONTAINER =  --## 2_bfn_start
{
["AMUMSS_SUPPRESS_MSG"] = "UNUSED_VARIABLE", --remove notices that a variable was not used
["MOD_FILENAME"] 			= "@mod_title@.pak",
["MOD_AUTHOR"]				= "@mod_author@",
["NMS_VERSION"]				= "",
["MODIFICATIONS"] 			= 
	{
		{
			["MBIN_CHANGE_TABLE"] 	= 
			{ 
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"METADATA\SIMULATION\SOLARSYSTEM\BIOMES\BIOMEFILENAMES.MBIN"
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						--### BiomeFilles + Weights ### ----------------------------------
						{
							["PRECEDING_KEY_WORDS"] = { "BiomeFiles", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = addHeader,
						},
						{
							["PRECEDING_KEY_WORDS"] = {"BiomeFiles",},
							["REMOVE"] = "SECTION",
						},
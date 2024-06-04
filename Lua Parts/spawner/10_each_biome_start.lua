
					} --## 10_each_biome_start
				},
				
				{
					["MBIN_FILE_SOURCE"] 	= "@each_biome_mbin@",
					["EXML_CHANGE_TABLE"] 	= 
					{
						
						{
							["PRECEDING_KEY_WORDS"] = { "ExternalObjectLists", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = addEachBiomeHeader,
						},
						{
							["PRECEDING_KEY_WORDS"] = {"ExternalObjectLists",},
							["REMOVE"] = "SECTION",
						},
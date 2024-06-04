
			} --## 4a_global_distance
		},
------------------------------------------------------------------------------------------------------------------------
--Section below originally written by InsaneRuffles, modified by FjordFish ---------------------------------------------
------------------------------------------------------------------------------------------------------------------------
		{
			["PAK_FILE_SOURCE"] 	= "NMSARC.59B126E2.pak",
			["MBIN_CHANGE_TABLE"] 	= 
			{ 
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"GCGRAPHICSGLOBALS.GLOBAL.MBIN"
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = "",
							["REPLACE_TYPE"] 		= "ALL",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"ForceUncachedTerrain",	ForceUncachedTerrain},
							}
						},
						{
							["PRECEDING_KEY_WORDS"] = "",   
							["MATH_OPERATION"] 		= "*",    
							["REPLACE_TYPE"] 		= "ALL",    
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"ShadowLength",			ShadowLengthMultiplier},
								--{"ShadowLengthShip",		ShadowLengthMultiplier},
								{"ShadowLengthSpace",		ShadowLengthMultiplier},
								{"ShadowLengthStation",		ShadowLengthMultiplier},
								{"ShadowLengthCameraView",	ShadowLengthMultiplier},
							}
						},
					} 
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"GCENVIRONMENTGLOBALS.GLOBAL.MBIN"		
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = "",   
							["MATH_OPERATION"] 		= "*",    
							["REPLACE_TYPE"] 		= "ALL",    
							["LINE_OFFSET"] 		= "+1",    
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"LODAdjust",	LODAdjustMultiplier} 
							}
						},
						{
							["PRECEDING_KEY_WORDS"] = "",
							["MATH_OPERATION"] 		= "*",
							["REPLACE_TYPE"] 		= "ALL",
							["LINE_OFFSET"] 		= "+2",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"LODAdjust",	LODAdjustMultiplier}
							}
						},
						{
							["PRECEDING_KEY_WORDS"] = "",
							["MATH_OPERATION"] 		= "*",
							["REPLACE_TYPE"] 		= "ALL",
							["LINE_OFFSET"] 		= "+3",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"LODAdjust",	LODAdjustMultiplier}
							}
						},
						{
							["PRECEDING_KEY_WORDS"] = "",
							["MATH_OPERATION"] 		= "*",
							["REPLACE_TYPE"] 		= "ALL",
							["LINE_OFFSET"] 		= "+4",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"LODAdjust",	LODAdjustMultiplier}
							}
						},
						{
							["PRECEDING_KEY_WORDS"] = "",
							["MATH_OPERATION"] 		= "*",
							["REPLACE_TYPE"] 		= "ALL",
							["LINE_OFFSET"] 		= "+5",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"LODAdjust",	LODAdjustMultiplier}
							}
						},
						{
							["PRECEDING_KEY_WORDS"] = "",   
							["MATH_OPERATION"] 		= "+",    
							["REPLACE_TYPE"] 		= "ALL",    
							["LINE_OFFSET"] 		= "+1",    
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"RegionLODRadius",	0}	--distance radius of finest details, increase causes flickering on some planets
							}
						},
						{
							["PRECEDING_KEY_WORDS"] = "",
							["MATH_OPERATION"] 		= "+",
							["REPLACE_TYPE"] 		= "ALL",
							["LINE_OFFSET"] 		= "+2",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"RegionLODRadius",	RegionLODRadiusAdd}
							}
						},
						{
							["PRECEDING_KEY_WORDS"] = "",
							["MATH_OPERATION"] 		= "+",
							["REPLACE_TYPE"] 		= "ALL",
							["LINE_OFFSET"] 		= "+3",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"RegionLODRadius",	RegionLODRadiusAdd}
							}
						},
						{
							["PRECEDING_KEY_WORDS"] = "",
							["MATH_OPERATION"] 		= "+",
							["REPLACE_TYPE"] 		= "ALL",
							["LINE_OFFSET"] 		= "+4",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"RegionLODRadius",	RegionLODRadiusAdd}
							}
						},
						{
							["PRECEDING_KEY_WORDS"] = "",
							["MATH_OPERATION"] 		= "+",
							["REPLACE_TYPE"] 		= "ALL",
							["LINE_OFFSET"] 		= "+5",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"RegionLODRadius",	RegionLODRadiusAdd}
							}
						},						
						{
							["PRECEDING_KEY_WORDS"] = "",
							["MATH_OPERATION"] 		= "+",
							["REPLACE_TYPE"] 		= "ALL",
							["LINE_OFFSET"] 		= "+6",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"RegionLODRadius",	RegionLODRadiusAdd}
							}
						},
						{
							["PRECEDING_KEY_WORDS"] = "",   
							["MATH_OPERATION"] 		= "*",    
							["REPLACE_TYPE"] 		= "ALL",    
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"PlanetObjectSwitch",			PlanetLODMultiplier},
								{"PlanetLodSwitch0",			PlanetLODMultiplier},
								{"PlanetLodSwitch0Elevation",	PlanetLODMultiplier},
								{"PlanetLodSwitch1",			PlanetLODMultiplier},
								{"PlanetLodSwitch2",			PlanetLODMultiplier},
								{"PlanetLodSwitch3",			PlanetLODMultiplier}
								--{"PlanetFlipDistance",		PlanetLODMultiplier},
								--{"PlanetEffectEndDistance",	PlanetLODMultiplier}
							}
						},
------------------------------------------------------------------------------------------------------------------------
--Section above originally written by InsaneRuffles, modified by FjordFish ---------------------------------------------
------------------------------------------------------------------------------------------------------------------------
						{
							["PRECEDING_KEY_WORDS"] = "",
							["INTEGER_TO_FLOAT"]	= "FORCE",
							["REPLACE_TYPE"] 		= "ALL",  
							["VALUE_CHANGE_TABLE"]	=
							{
								{"TerrainFadeTime",						  "0.7"},
								{"TerrainFadeTimeInShip",				  "0.9"},
								--{"CreatureFadeTime",					  "0.9"}, --caused hitching
								--{"FloraFadeTimeMin",						  "0.5"}, --less causes hitching
								{"FloraFadeTimeMax",				      "0.9"}, --less causes hitching
							}
						},
					} 
				}
			}
		},
    }
}
--NOTE: ANYTHING NOT in table NMS_MOD_DEFINITION_CONTAINER IS IGNORED AFTER THE SCRIPT IS LOADED
--IT IS BETTER TO ADD THINGS AT THE TOP IF YOU NEED TO
--DON'T ADD ANYTHING PAST THIS POINT HERE
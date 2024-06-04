

NMS_MOD_DEFINITION_CONTAINER = --## 2_body
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
				
			--Add collisions
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\COMMON\FLAGS\MARTIANFLAG02.SCENE.MBIN",
						"MODELS\PLANETS\COMMON\FLAGS\MARTIANFLAG01.SCENE.MBIN",
						"MODELS\PLANETS\COMMON\FLAGS\MARTIANFLAG03.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\BARREN\LARGEPROPS\LARGEFLAG.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\NEVADA\LARGEPLANTS\DEADTREE01.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\NEVADA\LARGEPLANTS\DEADTREE02.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\NEVADA\LARGEPLANTS\LARGEPLANT01.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\ALIEN\LARGEPLANT\BENDYTREE01.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\ALIEN\LARGEPLANT\LARGETREE02.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\ALIEN\MEDIUMPROP\MEDIUMPROP01.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\RAINFOREST\LARGEPLANT\MEDIUMTREE1.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\RAINFOREST\LARGEPLANT\MEDIUMTREE2.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\RAINFOREST\LARGEPLANT\LARGEPLANT1.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\RAINFOREST\LARGEPLANT\MEDIUMTREE3.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\RAINFOREST\LARGEPLANT\SMALLTREE1.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\RAINFOREST\LARGEPLANT\LARGETREE1.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\RAINFOREST\LARGEPLANT\TREEVARIANTS.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\RAINFOREST\LARGEPLANT\LARGEMANGROVE.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\RAINFOREST\LARGEPLANT\SMALLTREE1BENT.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\GLOWING\LARGEPLANT\MEDGLOWINGTREE1.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\GLOWING\LARGEPLANT\SMALLGLOWINGTREE1.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\COMMON\TREES\LARGETREE1.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddBasicCollisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/SMALLSPRUCE01.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddBasicCollisions,
						},
						{
							["REPLACE_TYPE"] 		= "ALL",
							["SPECIAL_KEY_WORDS"] = {"Name","MATERIAL",},
							["VALUE_MATCH"] 		= "MODELS\PLANETS\BIOMES\ALPINE\LARGEPLANT\SMALLSPRUCE01\FIRLEAF.MATERIAL.MBIN",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"Value",	"MODELS\PLANETS\BIOMES\COMMON\TREES\MEDIUMTREE1\TRUNKABILLBOARD_NEWLEAFMAT.MATERIAL.MBIN"},
							}	
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS/PLANETS/BIOMES/NEVADA/LARGEPLANTS/LARGEBUSH1.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["REPLACE_TYPE"] 		= "ALL",
							["SPECIAL_KEY_WORDS"] = {"Name","MATERIAL",},
							["VALUE_MATCH"] 		= "MODELS\PLANETS\BIOMES\NEVADA\LARGEPLANTS\LARGEBUSH1\LARGEBUSHMAT.MATERIAL.MBIN",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"Value",	"MODELS\PLANETS\BIOMES\COMMON\TREES\MEDIUMTREE1\TRUNKABILLBOARD_NEWLEAFMAT.MATERIAL.MBIN"},
							}	
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS/PLANETS/BIOMES/NEVADA/LARGEPLANTS/LARGEPLANT03.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddBasicCollisions,
						},
						{
							["REPLACE_TYPE"] 		= "ALL",
							["SPECIAL_KEY_WORDS"] = {"Name","MATERIAL",},
							["VALUE_MATCH"] 		= "MODELS\PLANETS\BIOMES\NEVADA\LARGEPLANTS\LARGEPLANT03\BUSHLEAFMAT.MATERIAL.MBIN",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"Value",	"MODELS\PLANETS\BIOMES\COMMON\TREES\MEDIUMTREE1\TRUNKABILLBOARD_NEWLEAFMAT.MATERIAL.MBIN"},
							}	
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/SMALLCEDAR01.SCENE.MBIN", -------------
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddBasicCollisions,
						},
						{
							["REPLACE_TYPE"] 		= "ALL",
							["SPECIAL_KEY_WORDS"] = {"Name","MATERIAL",},
							["VALUE_MATCH"] 		= "MODELS\PLANETS\BIOMES\ALPINE\LARGEPLANT\SMALLCEDAR01\LEAF01.MATERIAL.MBIN",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"Value",	"MODELS\PLANETS\BIOMES\COMMON\TREES\MEDIUMTREE1\TRUNKABILLBOARD_NEWLEAFMAT.MATERIAL.MBIN"},
							}	
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/MEDIUMUMBRELLA01.SCENE.MBIN", -------------
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddBasicCollisions,
						},
						{
							["REPLACE_TYPE"] 		= "ALL",
							["SPECIAL_KEY_WORDS"] = {"Name","MATERIAL",},
							["VALUE_MATCH"] 		= "MODELS\PLANETS\BIOMES\ALPINE\LARGEPLANT\MEDIUMUMBRELLA01\LEAF01.MATERIAL.MBIN",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"Value",	"MODELS\PLANETS\BIOMES\COMMON\TREES\MEDIUMTREE1\TRUNKABILLBOARD_NEWLEAFMAT.MATERIAL.MBIN"},
							}	
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/MEDIUMSPRUCE01.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddBasicCollisions,
						},
						{
							["REPLACE_TYPE"] 		= "ALL",
							["SPECIAL_KEY_WORDS"] = {"Name","MATERIAL",},
							["VALUE_MATCH"] 		= "MODELS\PLANETS\BIOMES\ALPINE\LARGEPLANT\MEDIUMSPRUCE01\FIRLEAF.MATERIAL.MBIN",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"Value",	"MODELS\PLANETS\BIOMES\COMMON\TREES\MEDIUMTREE1\TRUNKABILLBOARD_NEWLEAFMAT.MATERIAL.MBIN"},
							}	
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/MEDIUMDEADTREE01.SCENE.MBIN", --
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddBasicCollisions,
						},
						{
							["REPLACE_TYPE"] 		= "ALL",
							["SPECIAL_KEY_WORDS"] = {"Name","MATERIAL",},
							["VALUE_MATCH"] 		= "MODELS\PLANETS\BIOMES\ALPINE\LARGEPLANT\MEDIUMDEADTREE01\DEADLEAFMAT.MATERIAL.MBIN",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"Value",	"MODELS\PLANETS\BIOMES\COMMON\TREES\MEDIUMTREE1\TRUNKABILLBOARD_NEWLEAFMAT.MATERIAL.MBIN"},
							}	
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/LARGESPRUCE01.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddBasicCollisions,
						},
						{
							["REPLACE_TYPE"] 		= "ALL",
							["SPECIAL_KEY_WORDS"] = {"Name","MATERIAL",},
							["VALUE_MATCH"] 		= "MODELS\PLANETS\BIOMES\ALPINE\LARGEPLANT\LARGESPRUCE01\MEDIUMSPRUCE01_FIRLEAF.MATERIAL.MBIN",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"Value",	"MODELS\PLANETS\BIOMES\COMMON\TREES\MEDIUMTREE1\TRUNKABILLBOARD_NEWLEAFMAT.MATERIAL.MBIN"},
							}	
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\SNOW\CONSTRUCTS\CONSTRUCT01.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddConstruct01Collisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\BIOMES\RAINFOREST\LARGECREATURE\DIPLODOCUS\DIPLODOCUS.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\RAINFOREST\LARGECREATURE\DIPLODOCUS\DIPLODOCUSALIEN.SCENE.MBIN",
						"MODELS\PLANETS\BIOMES\RAINFOREST\LARGECREATURE\DIPLODOCUS\DIPLOPOSE.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddDiploCollisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\BIOMES\NEVADA\LARGEPROP\LARGEPYRAMID.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddLargePyramidCollisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\BIOMES\ALPINE\LARGEPLANT\LARGEFIR01.SCENE.MBIN", --big
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddLargeFir01Collisions,
						},
						{
							["REPLACE_TYPE"] 		= "ALL",
							["SPECIAL_KEY_WORDS"] = {"Name","MATERIAL",},
							["VALUE_MATCH"] 		= "MODELS\PLANETS\BIOMES\ALPINE\LARGEPLANT\LARGEFIR01\FIRMAT.MATERIAL.MBIN",
							["VALUE_CHANGE_TABLE"] 	= 
							{
								{"Value",	"MODELS\PLANETS\BIOMES\COMMON\TREES\MEDIUMTREE1\TRUNKABILLBOARD_NEWLEAFMAT.MATERIAL.MBIN"},
							}	
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\SPACE\WRECKS\DEBRIS\PANEL.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddPanelCollisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\BIOMES\CRYSTAL\LARGEPROP\GIANTCUBE.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddGiantCubeCollisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\BIOMES\CRYSTAL\SMALLPROP\TINYCUBES.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddTinyCubesCollisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\BIOMES\CRYSTAL\LARGEPROP\GIANTSPIKE.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddGiantSpikeCollisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\BIOMES\CRYSTAL\LARGEPROP\PILLAR1.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddPillar1Collisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\BIOMES\CRYSTAL\LARGEPROP\SQUATPILLAR1.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddSquatPillar1Collisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\BIOMES\RAINFOREST\MEDIUMCREATURE\ANTELOPE\ANTELOPE.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddAntelopeCollisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\COMMON\CHARACTERS\ASTRONAUT\ASTRONAUT01.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddAstronaut01Collisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\COMMON\ROBOTS\WALKER.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddWalkerCollisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\BIOMES\RAINFOREST\LARGEPLANT\SMALLTREE3.SCENE.MBIN", --"M"-shaped tree
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddSmallTree3Collisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\BIOMES\COMMON\BUILDINGS\MONUMENTS\STARGATEMAIN.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddStargateMainCollisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\BIOMES\COMMON\BUILDINGS\MONUMENTS\STARGATESMALL.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddStargateSmallCollisions,
						},
					}
				},
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						"MODELS\PLANETS\BIOMES\UNDERWATER\UPDATEPROPS\SAILPLANT.SCENE.MBIN",
					},
					["EXML_CHANGE_TABLE"] 	= 
					{
						{
							["PRECEDING_KEY_WORDS"] = { "TkSceneNodeData.xml", },
							["ADD_OPTION"] 	= "ADDafterSECTION",
							["ADD"] = AddSailPlantCollisions,
						},
					}
				},
				
				--Copy vanilla files to custombiomes folder
				{
					["MBIN_FILE_SOURCE"] 	= 
					{
						{"METADATA\SIMULATION\SOLARSYSTEM\BIOMES\OBJECTS\RARE\UNDERWATERSPHERES.MBIN","@biome_name@"},
					},
				},
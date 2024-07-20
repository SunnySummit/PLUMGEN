--[[

LUA script created using PLUMGEN
Script may include unused identifiers
Import EXML back into PLUMGEN for swift and easy editing

--]]

--## 1_header
local addHeader =
[[
  <Property name="BiomeFiles">
  </Property>
]]

function addPlanetType(planetType)
return [[
    <Property name="]] .. planetType .. [[" value="GcBiomeFileListOptions.xml">
      <Property name="FileOptions">
      </Property>
    </Property>
]]
end

function addFileListOption(subType, filename, weight, prpl_weight)
return [[
        <Property value="GcBiomeFileListOption.xml">
          <Property name="SubType" value="GcBiomeSubType.xml">
            <Property name="BiomeSubType" value="]] .. subType .. [[" />
          </Property>
          <Property name="Filename" value="]] .. filename .. [[" />
          <Property name="Weight" value="]] .. weight .. [[" />
          <Property name="PurpleSystemWeight" value="]] .. prpl_weight .. [[" />
        </Property>
]]
end

--## BFN Valid Start Planets ##-----------------------------------------------
local addStartHeader =
[[
  <Property name="ValidStartPlanetBiome">
  </Property>
]]


function addStartBody(biomeType)
return [[
    <Property value="GcBiomeType.xml">
      <Property name="Biome" value="]] .. biomeType .. [[" />
    </Property>
]]
end

--## BFN Tiletypes ##---------------------------------------------------------
local addCommonExternalHeader = 
[[
  <Property name="CommonExternalObjectLists">
  </Property>
]]

function addCommonExternalBody(weight, tileType)
return [[
    <Property value="GcExternalObjectListOptions.xml">
      <Property name="Name" value="PLUMGEN_STUFF" />
      <Property name="ResourceHint" value="" />
      <Property name="ResourceHintIcon" value="" />
      <Property name="Probability" value="]] .. weight .. [[" />
      <Property name="SeasonalProbabilityOverride" value="1" />
      <Property name="TileType" value="GcTerrainTileType.xml">
        <Property name="TileType" value="]] .. tileType .. [[" />
      </Property>
      <Property name="AllowLimiting" value="False" />
      <Property name="ChooseUsingLifeLevel" value="False" />
      <Property name="Options">
      </Property>
    </Property>
]]
end

function addBiomeOptions(biomeObjectsName)
return [[
        <Property value="VariableSizeString.xml">
          <Property name="Value" value="]] .. biomeObjectsName .. [[" />
        </Property>
]]
end

--##Each biome file ##------------------------------------------------------
local addEachBiomeHeader =
[[
  <Property name="ExternalObjectLists">
  </Property>
]]

--Reuses above 2 functions

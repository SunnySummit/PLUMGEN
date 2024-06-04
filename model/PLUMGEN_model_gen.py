'''
File: PLUMGEN_model_gen.py
'''

import random
import logging
from tkinter import messagebox

# no file imports

class PlumgenModelGen():

    def __init__(self, filename, dist_def, landm_def, objs_def, detail_def):
        
        self.logger = logging.getLogger(__name__)  #set up logging

        try:
            # initialize variables with default values
            self.filename = filename # string

            self.distant_objs_defaults = dist_def
            self.landmarks_defaults = landm_def
            self.objs_defaults = objs_def
            self.detail_objs_defaults = detail_def

            # initialize variables and dictionary with default values
            self.defaults = {
                "model_path": "MODELS/PLANETS/BIOMES/COMMON/GRASS/NEWCROSSGRASS.SCENE.MBIN",
                "placement": "WORDSTONE",
                "min_height": 0,
                "max_height": 0,
                "min_angle": 0,
                "max_angle": 0,
                "min_scale": 0.0,
                "max_scale": 0.0,
                "min_scale_y": 0.0,
                "max_scale_y": 0.0,
                "patch_edge_scaling": 0.0,
                "max_xz_rotation": 0,
                "destroyable_by_ship": True,
                "destroyable_by_terrain_edit": True,
                "creature_can_eat": True,
                "coverage": 0.0,
                "flat_density": 0.0,
                "slope_density": 0.0,
                "slope_multiplier": 0.0,
                "draw_distance": "none specified",
                "similar_items": [],
            }

            # create list by iterating over the keys of the dictionary
            self.distant_obj_list = [self.defaults[key] for key in self.defaults]

            #  create copies of the lists
            self.landmarks_list = self.distant_obj_list.copy()
            self.objects_list = self.distant_obj_list.copy()
            self.detail_obj_list = self.distant_obj_list.copy()

            # set model_path for each list to a random item (excluding "--")
            # check if list is empty = won't create a blank asset
            if bool(self.distant_objs_defaults):
                self.distant_obj_list[0] = random.choice([item for item in self.distant_objs_defaults if item != "--"])
            if bool(self.landmarks_defaults):
                self.landmarks_list[0] = random.choice([item for item in self.landmarks_defaults if item != "--"])
            if bool(self.objs_defaults):
                self.objects_list[0] = random.choice([item for item in self.objs_defaults if item != "--"])
            if bool(self.detail_objs_defaults):
                self.detail_obj_list[0] = random.choice([item for item in self.detail_objs_defaults if item != "--"])

            # create lists of lists
            self.all_distant_obj_lists = [self.distant_obj_list]
            self.all_landmarks_lists = [self.landmarks_list]
            self.all_objects_lists = [self.objects_list]
            self.all_detail_obj_lists = [self.detail_obj_list]
        
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    def show_error_message(self, message, max_length=200):
        if len(message) > max_length:
            truncated_message = message[:max_length] + "..."
        else:
            truncated_message = message
        messagebox.showerror("Error", f"{truncated_message}\n\nIf you're struggling to resolve this error, please share the 'plumgen.log' file with the dev.", master=None)


    # getter methods
    def get_distant_objs_defaults(self):
        return self.distant_objs_defaults
    
    def get_landmarks_defaults(self):
        return self.landmarks_defaults
    
    def get_objs_defaults(self):
        return self.objs_defaults
    
    def get_detail_objs_defaults(self):
        return self.detail_objs_defaults

    #
    def get_distant_obj_lists(self):
        return self.all_distant_obj_lists

    def get_landmark_lists(self):
        return self.all_landmarks_lists

    def get_objects_lists(self):
        return self.all_objects_lists

    def get_detail_obj_lists(self):
        return self.all_detail_obj_lists
    
    ##
    def get_filename(self):
        return self.filename

    
    # setter copy methods
    def set_distant_obj_lists_copy(self, distant_obj_lists):
        self.all_distant_obj_lists = distant_obj_lists.copy()

    def set_landmark_lists_copy(self, landscape_lists):
        self.all_landmarks_lists = landscape_lists.copy()

    def set_objects_lists_copy(self, objects_list):
        self.all_objects_lists = objects_list.copy()

    def set_detail_obj_lists_copy(self, detail_obj_lists):
        self.all_detail_obj_lists = detail_obj_lists.copy()


    # setter methods
    def set_distant_objs_defaults(self, dist_def):
        self.distant_objs_defaults = dist_def

    def set_landmarks_defaults(self, landm_def):
        self.landmarks_defaults = landm_def

    def set_objs_defaults(self, objs_def):
        self.objs_defaults = objs_def

    def set_detail_objs_defaults(self, detail_def):
        self.detail_objs_defaults = detail_def


    def set_filename(self, filename):
        self.filename = filename

    def set_distant_obj_lists(self, distant_obj_lists):
        self.all_distant_obj_lists = distant_obj_lists

    def set_landmark_lists(self, landscape_lists):
        self.all_landmarks_lists = landscape_lists

    def set_objects_lists(self, objects_list):
        self.all_objects_lists = objects_list

    def set_detail_obj_lists(self, detail_obj_lists):
        self.all_detail_obj_lists = detail_obj_lists


    # set "similar_items" for the latest appended list
    def set_distant_model_similar_props(self, similar_props):
        self.all_distant_obj_lists[-1][20] = similar_props
    
    def set_landmark_model_similar_props(self, similar_props):
        self.all_landmarks_lists[-1][20] = similar_props
    
    def set_object_model_similar_props(self, similar_props):
        self.all_objects_lists[-1][20] = similar_props
    
    def set_detail_model_similar_props(self, similar_props):
        self.all_detail_obj_lists[-1][20] = similar_props

    # set "similar_items" for specific index - used to refresh all counts
    def set_all_distant_model_similar_props(self, index, similar_props):
        self.all_distant_obj_lists[index][20] = similar_props
    
    def set_all_landmark_model_similar_props(self, index, similar_props):
        self.all_landmarks_lists[index][20] = similar_props
    
    def set_all_object_model_similar_props(self, index, similar_props):
        self.all_objects_lists[index][20] = similar_props
    
    def set_all_detail_model_similar_props(self, index, similar_props):
        self.all_detail_obj_lists[index][20] = similar_props


    # set custom attribute for specific index - used to save attribute
    def set_custom_distant_attr(self, index, attribute, modified_value):
        self.all_distant_obj_lists[index][attribute] = modified_value
    
    def set_custom_landmark_attr(self, index, attribute, modified_value):
        self.all_landmarks_lists[index][attribute] = modified_value
    
    def set_custom_object_attr(self, index, attribute, modified_value):
        self.all_objects_lists[index][attribute] = modified_value
    
    def set_custom_detail_attr(self, index, attribute, modified_value):
        self.all_detail_obj_lists[index][attribute] = modified_value


    # set multiply custom attribute for specific index
    def set_multiply_custom_distant_attr(self, index, attribute, modified_value):
        # convert values to numeric type before multiplying
        origin_value = float(self.all_distant_obj_lists[index][attribute])
        modified_value = float(modified_value)
        result = origin_value * modified_value
        if result.is_integer():  # check if result is whole number
            result_str = str(int(result))  # if so, convert to int
        else: 
            result_str = str(result)  # otherwise, keep as float
        self.all_distant_obj_lists[index][attribute] = result_str # assign string value back to the attribute

    def set_multiply_custom_landmark_attr(self, index, attribute, modified_value):
        origin_value = float(self.all_landmarks_lists[index][attribute])
        modified_value = float(modified_value)
        result = origin_value * modified_value
        if result.is_integer():
            result_str = str(int(result))
        else: 
            result_str = str(result)
        self.all_landmarks_lists[index][attribute] = result_str
    
    def set_multiply_custom_object_attr(self, index, attribute, modified_value):
        origin_value = float(self.all_objects_lists[index][attribute])
        modified_value = float(modified_value)
        result = origin_value * modified_value
        if result.is_integer():
            result_str = str(int(result))
        else: 
            result_str = str(result)
        self.all_objects_lists[index][attribute] = result_str
    
    def set_multiply_custom_detail_attr(self, index, attribute, modified_value):
        origin_value = float(self.all_detail_obj_lists[index][attribute])
        modified_value = float(modified_value)
        result = origin_value * modified_value
        if result.is_integer():
            result_str = str(int(result))
        else: 
            result_str = str(result)
        self.all_detail_obj_lists[index][attribute] = result_str


    # add new prop to lists. first check if lists are empty = won't create blank asset
    def add_distant_obj_list(self):
        try:
            if bool(self.distant_objs_defaults):
                new_distant_obj_list = self.distant_obj_list.copy()
                new_distant_obj_list[0] = random.choice([item for item in self.distant_objs_defaults if item != "--"])
                self.all_distant_obj_lists.append(new_distant_obj_list)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))

    def add_landmark_list(self):
        try:
            if bool(self.landmarks_defaults):
                new_landmarks_list = self.landmarks_list.copy()
                new_landmarks_list[0] = random.choice([item for item in self.landmarks_defaults if item != "--"])
                self.all_landmarks_lists.append(new_landmarks_list)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))

    def add_objects_list(self):
        try:
            if bool(self.objs_defaults):
                new_objects_list = self.objects_list.copy()
                new_objects_list[0] = random.choice([item for item in self.objs_defaults if item != "--"])
                self.all_objects_lists.append(new_objects_list)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))

    def add_detail_obj_list(self):
        try:
            if bool(self.detail_objs_defaults):
                new_detail_obj_list = self.detail_obj_list.copy()
                new_detail_obj_list[0] = random.choice([item for item in self.detail_objs_defaults if item != "--"])
                self.all_detail_obj_lists.append(new_detail_obj_list)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))

    # delete selected prop in lists
    def delete_distant_obj(self, index):
        try:
            del self.all_distant_obj_lists[index]
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))

    def delete_landmark(self, index):
        try:
            del self.all_landmarks_lists[index]
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))

    def delete_object(self, index):
        try:
            del self.all_objects_lists[index]
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))

    def delete_detail_obj(self, index):
        try:
            del self.all_detail_obj_lists[index]
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))

    # duplicate selected prop in lists
    def duplicate_distant_obj(self, index):
        try:
            duplicated_list = self.all_distant_obj_lists[index].copy()
            self.all_distant_obj_lists.append(duplicated_list)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))

    def duplicate_landmark(self, index):
        try:
            duplicated_list = self.all_landmarks_lists[index].copy()
            self.all_landmarks_lists.append(duplicated_list)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))

    def duplicate_object(self, index):
        try:
            duplicated_list = self.all_objects_lists[index].copy()
            self.all_objects_lists.append(duplicated_list)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))

    def duplicate_detail_obj(self, index):
        try:
            duplicated_list = self.all_detail_obj_lists[index].copy()
            self.all_detail_obj_lists.append(duplicated_list)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



# class
class DefaultSpawnDensityList():
    def __init__(self):
        
        self.create_default_sdl()

    def create_default_sdl(self):
        sdl_blocks = """
            Name: BIGHAZCROP
            CoverageType: GridPatch
            PatchSize: 586
            RegionScale: 0.1

            Name: BIGFUELCROP
            CoverageType: GridPatch
            PatchSize: 585
            RegionScale: 0.1

            Name: RARE1
            CoverageType: GridPatch
            PatchSize: 590
            RegionScale: 0.1

            Name: RARE2
            CoverageType: GridPatch
            PatchSize: 610
            RegionScale: 0.1

            Name: RARE3
            CoverageType: GridPatch
            PatchSize: 650
            RegionScale: 0.1

            Name: VALUABLE_STUFF
            CoverageType: GridPatch
            PatchSize: 250
            RegionScale: 1

            Name: WORDSTONE
            CoverageType: GridPatch
            PatchSize: 200
            RegionScale: 1

            Name: CRATES
            CoverageType: GridPatch
            PatchSize: 110
            RegionScale: 1

            Name: DEBRIS
            CoverageType: GridPatch
            PatchSize: 125
            RegionScale: 1

            Name: FUELCRYSTAL
            CoverageType: GridPatch
            PatchSize: 140
            RegionScale: 20

            Name: UNDERGROUND
            CoverageType: GridPatch
            PatchSize: 150
            RegionScale: 1

            Name: CAVEGRASSCLUMP
            CoverageType: SmoothPatch
            PatchSize: 4
            RegionScale: 5

            Name: CAVEROCKCLUMP
            CoverageType: SmoothPatch
            PatchSize: 6
            RegionScale: 5

            Name: GRASS
            CoverageType: Total
            PatchSize: 100
            RegionScale: 5

            Name: FOREST
            CoverageType: SmoothPatch
            PatchSize: 64
            RegionScale: 6

            Name: SPARSECLUMP
            CoverageType: SmoothPatch
            PatchSize: 30
            RegionScale: 5

            Name: ROCKCLUMP
            CoverageType: SmoothPatch
            PatchSize: 25
            RegionScale: 5

            Name: GRASSCLUMP
            CoverageType: SmoothPatch
            PatchSize: 20
            RegionScale: 5

            Name: BARRENROCKCLUMP
            CoverageType: SmoothPatch
            PatchSize: 25
            RegionScale: 8

            Name: BARRENGRASSCLUM
            CoverageType: SmoothPatch
            PatchSize: 5
            RegionScale: 15

            Name: CRYSTAL
            CoverageType: GridPatch
            PatchSize: 110
            RegionScale: 0.1

            Name: CRYSTAL2
            CoverageType: GridPatch
            PatchSize: 100
            RegionScale: 0.1

            Name: CRYSTAL3
            CoverageType: GridPatch
            PatchSize: 250
            RegionScale: 0.2

            Name: RESOURCE
            CoverageType: SmoothPatch
            PatchSize: 15
            RegionScale: 1.2

            Name: SMALLCLUMP
            CoverageType: SmoothPatch
            PatchSize: 8
            RegionScale: 2

            Name: FLORACLUMP
            CoverageType: SmoothPatch
            PatchSize: 5
            RegionScale: 5

            Name: BLANKETCLUMP
            CoverageType: SmoothPatch
            PatchSize: 3
            RegionScale: 2

            Name: RESCLUMPFUEL
            CoverageType: GridPatch
            PatchSize: 101
            RegionScale: 0.2

            Name: RESCLUMPCOM
            CoverageType: GridPatch
            PatchSize: 65
            RegionScale: 0.3

            Name: RESCLUMPTECH
            CoverageType: GridPatch
            PatchSize: 100
            RegionScale: 0.3

            Name: BIOMEPLANT
            CoverageType: GridPatch
            PatchSize: 550
            RegionScale: 0.2

            Name: RARE
            CoverageType: GridPatch
            PatchSize: 100
            RegionScale: 0.75

            Name: CRYSTALCAVE
            CoverageType: GridPatch
            PatchSize: 98
            RegionScale: 0.6

            Name: RARECAVE
            CoverageType: GridPatch
            PatchSize: 70
            RegionScale: 0.6

            Name: JAMESPATCH
            CoverageType: SmoothPatch
            PatchSize: 2
            RegionScale: 40

            Name: STORMCRYST
            CoverageType: GridPatch
            PatchSize: 220
            RegionScale: 1

            Name: RARE_BONES
            CoverageType: GridPatch
            PatchSize: 365
            RegionScale: 0.072

            Name: SCRAPHEAP
            CoverageType: GridPatch
            PatchSize: 185
            RegionScale: 0.54

            Name: WILDPLANTS
            CoverageType: GridPatch
            PatchSize: 120
            RegionScale: 0.6

            Name: SENTINEL_RARE1
            CoverageType: GridPatch
            PatchSize: 220
            RegionScale: 1

            Name: SENTINEL_RARE2
            CoverageType: GridPatch
            PatchSize: 320
            RegionScale: 1

            Name: SENTINEL_RARE3
            CoverageType: GridPatch
            PatchSize: 545
            RegionScale: 1
            """

        blocks = sdl_blocks.strip().split('\n\n') # split data into individual blocks

        sdl_dict = {} # empty dictionary

        # process each block, populate the dictionary
        for block in blocks:
            lines = block.split('\n')
            name = lines[0].split(': ')[1]
            attributes = {line.split(': ')[0].strip(): line.split(': ')[1].strip() for line in lines[1:]}
            sdl_dict[name] = attributes

        return sdl_dict








# class
class DefaultModelPaths():
    def __init__(self):
        
        self.create_default_model_paths()

    def create_default_model_paths(self):
        placement_defaults = [
            "BARRENGRASSCLUM",
            "BARRENROCKCLUMP",
            "BIGFUELCROP",
            "BIGHAZCROP",
            "BIOMEPLANT",
            "BLANKETCLUMP",
            "CAVEGRASSCLUMP",
            "CAVEROCKCLUMP",
            "CRATES",
            "CRYSTAL",
            "CRYSTAL2",
            "CRYSTAL3",
            "CRYSTALCAVE",
            "DEBRIS",
            "FLORACLUMP",
            "FOREST",
            "FUELCRYSTAL",
            "GRASS",
            "GRASSCLUMP",
            "JAMESPATCH",
            "RARE",
            "RARE1",
            "RARE2",
            "RARE3",
            "RARECAVE",
            "RARE_BONES",
            "RESCLUMPCOM",
            "RESCLUMPFUEL",
            "RESCLUMPTECH",
            "RESOURCE",
            "ROCKCLUMP",
            "SCRAPHEAP",
            "SENTINEL_RARE1",
            "SENTINEL_RARE2",
            "SENTINEL_RARE3",
            "SMALLCLUMP",
            "SPARSECLUMP",
            "STORMCRYST",
            "UNDERGROUND",
            "VALUABLE_STUFF",
            "WILDPLANTS",
            "WORDSTONE"
        ]
        
        distant_objs_defaults = [
            "MODELS/PLANETS/BIOMES/FROZENPILLARS/LARGEPILLAR.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/HQTREES/PARTS/HQTREE10.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/HQTREES/PARTS/HQTREE17.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/HQTREES/PARTS/HQTREE21.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/HQTREES/PARTS/HQTREE63.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HUGEPROPS/HUGERING/HUGERINGTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HUGEPROPS/HUGERING/HUGEROCKRING.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HUGEPROPS/HUGEROCK/HUGEPLATFORMROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HUGEPROPS/HUGEROCK/HUGESPIKEROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HUGEPROPS/HUGESCORCHED/HUGESPIRE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HUGEPROPS/HUGETOXIC/HUGEFUNGUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HUGEPROPS/HUGETOXIC/HUGETENDRIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HUGEPROPS/HUGEUW/HUGESTRANDS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HUGEPROPS/HUGEUW/HUGESWIRLPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/LARGEPROPS/LARGESHARDINACTIVE02.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/LARGEPROPS/LARGEVOLCANO.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SWAMP/LARGEPLANT/DEADTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SWAMP/LARGEPLANT/MANGROVELARGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SWAMP/LARGEPLANT/MANGROVELARGEFULL.SCENE.MBIN",
            "--",
            "MODELS/COMMON/CHARACTERS/ASTRONAUT/ASTRONAUT01.SCENE.MBIN",
            "MODELS/COMMON/ROBOTS/WALKER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALIEN/LARGEPLANT/BENDYTREE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALIEN/LARGEPLANT/LARGETREE02.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALIEN/MEDIUMPROP/MEDIUMPROP01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/LARGEFIR01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/LARGESPRUCE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/MEDIUMDEADTREE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/MEDIUMSPRUCE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/MEDIUMUMBRELLA01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/SMALLCEDAR01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/SMALLSPRUCE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/CACTUS/HQFLOWERCACTUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/MEDIUMBOULDER02.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/TREES/CACTUSLRG.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/LARGEPROPS/LARGEFLAG.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/GRAVEINCAVE/GRAVEINCAVE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/MONOLITH/MONOLITH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/MONUMENTS/STARGATEMAIN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/MONUMENTS/STARGATESMALL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PLAQUE/PLAQUEWARRIOR.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PROPS/ABANDONED/LIGHT_1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PROPS/ABANDONED/LIGHT_3.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PROPS/LIGHTS/SMALLLANTERN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/RELIC/RELIC.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/CRYSTALS/LARGE/CRYSTAL_LARGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/CRYSTALS/LARGE/CRYSTAL_LARGE_MOUNTAIN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/CRYSTALS/MEDIUM/CRYSTAL_MEDIUM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/CRYSTALS/MEDIUM/CRYSTAL_MEDIUM_CAVE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/CRYSTALS/MEDIUM/CRYSTAL_MEDIUM_MOUNTAIN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/BERRYPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/COMMODITYPLANT1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/COMMODITYPLANT2.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/EXPLODEPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/FUELPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/HEALTHPLANT2.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/TENTACLEPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/FERNLARGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/LARGEPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/MONSTERPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/MYRTLEBUSH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/CRYSTALS/LIGHTNINGROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/CRYSTALS/SENTINELCRYSTAL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/CRYSTALS/SENTINELCRYSTALDRONE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/CRYSTALS/SENTINELCRYSTALDRONESMALL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/CRYSTALS/SENTINELCRYSTALSMALL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/INAIR/FLOATINGGASBAGS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/UNDERWATER/SEAURCHIN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/MEDIUM/MEDIUMROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/LARGESANDBLENDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/TREES/LARGETREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/TREES/MEDIUMTREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/TREES/SKINNEDTREES.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/CRYSTAL/LARGEPROP/GIANTCUBE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/CRYSTAL/LARGEPROP/GIANTSPIKE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/CRYSTAL/LARGEPROP/PILLAR1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/CRYSTAL/LARGEPROP/SQUATPILLAR1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/CRYSTAL/SMALLPROP/TINYCUBES.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/LARGEPROPS/LARGETREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/LARGEPROPS/LARGETREEBARE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZENPILLARS/MEDIUMPILLAR.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/GLOWING/LARGEPLANT/MEDGLOWINGTREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/GLOWING/LARGEPLANT/SMALLGLOWINGTREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/GLOWING/MEDIUMPLANT/MEDGLOWINGBUSH1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/LARGEPROPS/LARGEICEROCK_1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/HQTREES/HQTREEREF.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/LARGEPROPS/MOSSCOVEREDWEIRDPROP.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/MEDIUMPROPS/MEDIUMBOULDER02.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/LARGEPROPS/DEADTREEFLAMING.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/MEDIUMPROPS/LAVACRYSTALS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/ARRAYSHELLSAND.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/ARRAYTWIST.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/FLAMESPLINTER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/FROZENUMBRELLA.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/HOTTENDRILS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/SUMMERSPIKE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/COLOURFANSHROOM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/LARGEBLUESHROOM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/LARGEBLUESHROOMSINGLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/LARGEFANSHROOMSINGLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/NEVADA/LARGEPLANTS/DEADTREE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/NEVADA/LARGEPLANTS/LARGEBUSH1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/NEVADA/LARGEPLANTS/LARGEPLANT01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/NEVADA/LARGEPLANTS/LARGEPLANT03.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/NEVADA/LARGEPROP/LARGEPYRAMID.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/LARGE/LARGEGLOWPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/MEDIUM/MEDIUMGLOWROCKSINGLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGECREATURE/DIPLODOCUS/DIPLODOCUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGECREATURE/DIPLODOCUS/DIPLODOCUSALIEN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGECREATURE/DIPLODOCUS/DIPLOPOSE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGECREATURE/RHINO/RHINO.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/LARGEMANGROVE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/LARGEPLANT1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/LARGETREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/MEDIUMTREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/MEDIUMTREE2.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/MEDIUMTREE3.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/SMALLTREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/SMALLTREE1BENT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/SMALLTREE2.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/SMALLTREE3.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/TREEVARIANTS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/MEDIUMCREATURE/ANTELOPE/ANTELOPE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/LARGE/LARGESPIRE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SWAMP/LARGEPLANT/STRAIGHTTREELARGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SWAMP/LARGEPLANT/VINETREELARGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/HOUDINIPROPS/LARGETENTACLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/FUNGALTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/SPORETREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/MEDIUM/SPORETENDRIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPLANTS/MEDIUIMGLOWPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/ANENOMESHAPE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/CUCUMBERSHAPE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/GASBAGS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/LAMPSHAPE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/SAILPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONETREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONETREEBIGGLOW.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONETREEDAMAGED.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/CONTOUR/CONTOURPOD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/CONTOUR/CONTOURTOWER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HEXAGON/ROTATINGDETAIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HOUDINIPROPS/SPIKYPOTATO.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HOUDINIPROPS/VORONOITREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HYDROGARDEN/LARGEMUSHROOM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/SHARDS/SHARD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/SHARDS/SHARDALT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/SHARDS/TALLSHARD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WOODLAND/LARGEPLANT/MEDIUMOAK1.SCENE.MBIN",
            "MODELS/PLANETS/COMMON/FLAGS/MARTIANFLAG03.SCENE.MBIN",
            "MODELS/PLANETS/SNOW/CONSTRUCTS/CONSTRUCT01.SCENE.MBIN",
            "MODELS/PLANETS/SNOW/WRECKS/GIANTWRECKEDSHIP.SCENE.MBIN"
        ]


        landmarks_defaults = [
            "MODELS/PLANETS/BIOMES/BARREN/HQ/CACTUS/HQFLOWERCACTUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/CORAL/LARGECORALSAND.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/GROUNDREVEALROCK01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/LARGEARRANGEDROCK01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/LARGEARRANGEDROCK02.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/LARGEHIVE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/LARGEHIVESINGLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/MEDIUMHIVE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/TREES/DRACAENA.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/LARGEPROPS/LARGEFLAG.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/LARGEPROPS/SANDCOVEREDWEIRDPROP.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/PLANTS/LARGECACTUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/PLANTS/MEDIUMCACTUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/ROCKS/LARGEROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/HUTS/MOSSHUT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/GRASS/NEWCROSSGRASS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/FERNLARGEALT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/FERNLIGHT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/LARGE/LARGEROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/LARGE/PROCSHAPE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/LARGEMOSSBLENDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/LARGESANDBLENDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/LARGESNOWBLENDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/LARGEPROPS/LARGEROCKS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/LARGEPROPS/LARGETREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/LARGEPROPS/LARGETREEBARE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/LARGEPROPS/SNOWCOVEREDWEIRDPROP.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZENPILLARS/LARGEPILLAR.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZENPILLARS/MEDIUMPILLAR.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/FOLIAGE/LARGETREEBARE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/LARGEPROPS/LARGEICEROCK_1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/LARGEPROPS/LARGEROCKSTACK_1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/LARGEPROPS/LARGEROCK_1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/TREES/HEROPINE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/TREES/SKINNYPINE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/TREES/TALLPINE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/HQTREES/HQTREEREF.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/HQTREES/PARTS/HQTREE21.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/LARGEPROPS/MOSSCOVEREDWEIRDPROP.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/LARGEPROPS/DEADTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/LARGEPROPS/DEADTREEFLAMING.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/LARGEPROPS/LARGESHARDINACTIVE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/MEDIUMPROPS/COMET01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/MEDIUMPROPS/MEDIUMDEADTREE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/MEDIUMPROPS/MEDIUMVOLCANICROCKS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/MEDIUMPROPS/MEDSHARDINACTIVE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/SMALLPROPS/SMALLCOMET01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/ARRAYSHELLSAND.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/ARRAYTWIST.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/BIOTANK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/FLAMESPLINTER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/FROZENUMBRELLA.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/LARGEEGG.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/LARGEEGGHOLDER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/LARGESUMMEREGG.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/SINGLESUMMER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/SUMMERUMBRELLA.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/HOTTENDRILS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/SPINDLESUMMER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/SUMMERSPIKE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/COLOURFANSHROOM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/LARGEBLUESHROOM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/LARGEBLUESHROOMSINGLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/LARGEFANSHROOM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/LARGEFANSHROOMSINGLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/LARGE/CURVEDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/LARGE/LARGEGLOWPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/LARGE/LARGEGLOWPLANTSINGLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/LARGE/RADIOACTIVETREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/MEDIUM/MEDIUMGLOWROCKSINGLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/LARGE/LARGESHIELDTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/LARGE/LARGESHIELDTREESINGLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/LARGE/LARGESPIRE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/MEDIUM/MEDIUMSPIRE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SWAMP/LARGEPLANT/DEADTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SWAMP/LARGEPROP/GROUNDREVEALROCK01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SWAMP/LARGEPROP/LARGEMOSSROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SWAMP/MEDIUMPLANT/YUKKA.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/HOUDINIPROPS/LARGETENTACLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/FUNGALTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/LARGETOXICEGG.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/LARGETOXICEGGSINGLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/SPORETREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/SPORETREESINGLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/TENDRIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/MEDIUM/SPORETENDRIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BEAMSTONE/HUGEBEAM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONETREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONETREEBIGGLOW.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONETREEDAMAGED.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/CONTOUR/CONTOURPOD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/CONTOUR/CONTOURTOWER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/ELBUBBLE/ELBUBBLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/ELBUBBLE/SMALLBUBBLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/FRACTALCUBE/SHAPE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/FRACTALCUBE/SHAPE1FLOAT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HEXAGON/HUGEOBJECT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HOUDINIPROPS/SPIKYPOTATO.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HOUDINIPROPS/VORONOITREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HYDROGARDEN/LARGEMUSHROOM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HYDROGARDEN/LARGEMUSHROOMDEAD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/IRRISHELLS/SHELLSAIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/IRRISHELLS/SHELLSHARD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/MSTRUCTURES/MSTRUCTURE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/SHARDS/SHARD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/SHARDS/SHARDALT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/SHARDS/TALLSHARD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/WIRECELLS/WIRECELLMEGATREE.SCENE.MBIN",
            "--",
            "MODELS/COMMON/CHARACTERS/ASTRONAUT/ASTRONAUT01.SCENE.MBIN",
            "MODELS/COMMON/ROBOTS/WALKER.SCENE.MBIN",
            "MODELS/EFFECTS/HEAVYAIR/BUBBLES/BUBBLES.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALIEN/LARGEPLANT/BENDYTREE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALIEN/LARGEPLANT/LARGETREE02.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALIEN/MEDIUMPROP/MEDIUMPROP01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/LARGEFIR01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/LARGESPRUCE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/MEDIUMDEADTREE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/MEDIUMSPRUCE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/MEDIUMUMBRELLA01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/SMALLCEDAR01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/ALPINE/LARGEPLANT/SMALLSPRUCE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/MEDIUMBOULDER02.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/TREES/CACTUSLRG.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/PLANTS/SMALLCACTUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/PLANTS/THINBUSHTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/ROCKS/MEDIUMROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/GRAVEINCAVE/GRAVEINCAVE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PROPS/ABANDONED/LIGHT_1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PROPS/ABANDONED/LIGHT_3.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PROPS/LIGHTS/SMALLLANTERN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/RELIC/RELIC.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/CRYSTALS/LARGE/CRYSTAL_LARGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/CRYSTALS/LARGE/CRYSTAL_LARGE_MOUNTAIN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/CRYSTALS/MEDIUM/CRYSTAL_MEDIUM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/CRYSTALS/MEDIUM/CRYSTAL_MEDIUM_CAVE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/CRYSTALS/MEDIUM/CRYSTAL_MEDIUM_MOUNTAIN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/GRASS/TALLGRASSBILLBOARD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/BERRYPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/COMMODITYPLANT1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/COMMODITYPLANT2.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/EXPLODEPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/FUELPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/HEALTHPLANT2.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/INTERACTIVEFLORA/TENTACLEPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/FERNLARGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/LARGEPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/MEDIUMBUSH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/MONSTERPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/MYRTLEBUSH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/SMALLFLOWERS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/SMALLPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/CRYSTALS/LIGHTNINGROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/CRYSTALS/SENTINELCRYSTAL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/CRYSTALS/SENTINELCRYSTALDRONE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/CRYSTALS/SENTINELCRYSTALDRONESMALL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/CRYSTALS/SENTINELCRYSTALSMALL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/INAIR/FLOATINGGASBAGS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/RARERESOURCE/UNDERWATER/SEAURCHIN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/MEDIUM/MEDIUMROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/LARGESANDBLENDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/MEDIUMSANDBLENDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/TREES/LARGETREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/TREES/MEDIUMTREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/TREES/SKINNEDTREES.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/CRYSTAL/LARGEPROP/GIANTCUBE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/CRYSTAL/LARGEPROP/GIANTSPIKE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/CRYSTAL/LARGEPROP/PILLAR1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/CRYSTAL/LARGEPROP/SQUATPILLAR1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/CRYSTAL/SMALLPROP/TINYCUBES.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/LARGEPROPS/LARGETREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/LARGEPROPS/LARGETREEBARE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/MEDIUMPROPS/MEDIUMPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZENPILLARS/MEDIUMPILLAR.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/GLOWING/LARGEPLANT/MEDGLOWINGTREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/GLOWING/LARGEPLANT/SMALLGLOWINGTREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/GLOWING/MEDIUMPLANT/MEDGLOWINGBUSH1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/LARGEPROPS/LARGEICEROCK_1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/HQTREES/HQTREEREF.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/HQTREES/PARTS/HQTREE10.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/HQTREES/PARTS/HQTREE17.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/HQTREES/PARTS/HQTREE63.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/LARGEPROPS/MOSSCOVEREDWEIRDPROP.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/LARGEPROPS/MOUNTAINROCK_1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/MEDIUMPROPS/MEDIUMBOULDER02.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HUGEPROPS/HUGERING/HUGERINGTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HUGEPROPS/HUGETOXIC/HUGETENDRIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HUGEPROPS/HUGEUW/HUGESTRANDS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HUGEPROPS/HUGEUW/HUGESWIRLPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/MEDIUMPROPS/LAVACRYSTALS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/FROZENSPIKE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/SPINDLEEGG.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/SMALL/SMALLTENDRIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/MEDIUMBLUESHROOM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/MEDIUMSHROOM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/NEVADA/LARGEPLANTS/DEADTREE01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/NEVADA/LARGEPLANTS/LARGEBUSH1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/NEVADA/LARGEPLANTS/LARGEPLANT01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/NEVADA/LARGEPLANTS/LARGEPLANT03.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/NEVADA/LARGEPROP/LARGEPYRAMID.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/LARGE/LARGEGLOWPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/MEDIUM/CURVEDMEDIUM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/MEDIUM/MEDIUMGLOWROCKSINGLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGECREATURE/DIPLODOCUS/DIPLODOCUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGECREATURE/DIPLODOCUS/DIPLODOCUSALIEN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGECREATURE/DIPLODOCUS/DIPLOPOSE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGECREATURE/RHINO/RHINO.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/LARGEMANGROVE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/LARGEPLANT1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/LARGETREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/MEDIUMTREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/MEDIUMTREE2.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/MEDIUMTREE3.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/SMALLTREE1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/SMALLTREE1BENT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/SMALLTREE2.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/SMALLTREE3.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/LARGEPLANT/TREEVARIANTS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RAINFOREST/MEDIUMCREATURE/ANTELOPE/ANTELOPE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/LARGE/LARGESPIRE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/MEDIUM/SCORCHSEED.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SWAMP/LARGEPLANT/STRAIGHTTREELARGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SWAMP/LARGEPLANT/VINETREELARGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/HOUDINIPROPS/LARGETENTACLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/HOUDINIPROPS/MEDIUMTENTACLEBLOB.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/FUNGALTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/SPONGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/SPORETREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/MEDIUM/MEDIUMPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/MEDIUM/SPORETENDRIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPLANTS/MEDIUIMGLOWPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPLANTS/MEDIUMJELLYPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPROP/MEDIUMGROWTHS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/ANENOMESHAPE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/CUCUMBERSHAPE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/GASBAGS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/LAMPSHAPE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/SAILPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONESPORE2.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/CONTOUR/CONTOUROBJECT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/ELBUBBLE/DETAILBUBBLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HEXAGON/GEOMETRIC.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HEXAGON/MEDGEOMETRIC.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HEXAGON/ROTATINGDETAIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HOUDINIPROPS/SPIKYPOTATO.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HOUDINIPROPS/VORONOITREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/IRRISHELLS/SHELLSHELF.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/MSTRUCTURES/SINGLEJOINT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/WIRECELLS/WIRECELLBLOCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WOODLAND/LARGEPLANT/MEDIUMOAK1.SCENE.MBIN",
            "MODELS/PLANETS/COMMON/FLAGS/MARTIANFLAG03.SCENE.MBIN",
            "MODELS/SPACE/WRECKS/DEBRIS/PANEL.SCENE.MBIN"
        ]


        objs_defaults = [
            "MODELS/EFFECTS/HEAVYAIR/BUBBLES/BUBBLES.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/CACTUS/HQFLOWERCACTUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/CORAL/MEDIUMCORALSAND.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/MEDIUMBOULDER01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/MEDIUMBOULDER02.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/TREES/CACTUSMED.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/PLANTS/MEDIUMCACTUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/ROCKS/LARGEROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/ROCKS/MEDIUMROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PARTS/BUILDABLEPARTS/FOLIAGE/BEAMSTONE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PARTS/BUILDABLEPARTS/FOLIAGE/BONECOLLECT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PARTS/BUILDABLEPARTS/FOLIAGE/BUBBLECOLLECT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PARTS/BUILDABLEPARTS/FOLIAGE/CONTOURPOD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PARTS/BUILDABLEPARTS/FOLIAGE/ENGINEORB.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PARTS/BUILDABLEPARTS/FOLIAGE/HYDROPOD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PARTS/BUILDABLEPARTS/FOLIAGE/MEDGEOMETRIC.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PARTS/BUILDABLEPARTS/FOLIAGE/SHARD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PARTS/BUILDABLEPARTS/FOLIAGE/SHELLWHITE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PARTS/BUILDABLEPARTS/FOLIAGE/STARJOINT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/FLOWERS/SCABIOUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/FLOWERS/YARROW.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/GRASS/NEWCROSSGRASS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/GRASS/TALLGRASSBILLBOARD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/LARGEPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/MEDIUMBUSH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/MEDIUMPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/LARGE/LARGEROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/MEDIUM/MEDIUMROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SMALL/FRAGMENTS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/LARGEMOSSBLENDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/LARGESANDBLENDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/MEDIUMMOSSBLENDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/MEDIUMSANDBLENDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/MEDIUMSNOWBLENDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/LARGEPROPS/LARGEROCKS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/MEDIUMPROPS/MEDIUMPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/MEDIUMPROPS/MEDIUMROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZENPILLARS/SMALLPILLARSTUMP.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/MEDIUMPROPS/MEDIUMROCKS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/LARGEPROPS/MOUNTAINROCK_1.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/MEDIUMPROPS/MEDIUMBOULDER01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/MEDIUMPROPS/MEDIUMBOULDER02.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/SMALLPROPS/LAVAGEMS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/BIOTANK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/LOWUMBRELLA.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/LARGE/SINGLEUMBRELLA.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/ARRAYSHELL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/CURLYTENDRILS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/FROZENSPIKE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/HOTROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/HOTROCKLIFTED.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/HOTTENDRILS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/MEDIUMPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/SPINDLEEGG.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/SPINDLESUMMER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/SUMMERSPIKE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/SMALL/SMALLPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/SMALL/SMALLTENDRIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/MEDIUMBLUESHROOM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/MEDIUMSHROOM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/LARGE/CURVEDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/LARGE/RADIOACTIVETREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/MEDIUM/CURVEDMEDIUM.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/MEDIUM/MEDIUMGLOWPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/MEDIUM/MEDIUMGLOWROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/MEDIUM/MEDIUMSTEAMER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/LARGE/LARGEROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/MEDIUM/MEDIUMROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/MEDIUM/MEDIUMSPIRE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/MEDIUM/SCORCHSEED.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/MEDIUM/VOLCANICPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/SMALL/LEAFDROPLET.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/HOUDINIPROPS/MEDIUMTENTACLEBLOB.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/FUNGALTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/LARGEBLOB.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/SPONGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/LARGE/TENDRIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/MEDIUM/MEDIUMPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/MEDIUM/MEDIUMROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/MEDIUM/MEDIUMTOXICEGG.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/MEDIUM/SPORETUBE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/MEDIUM/TOXICEGGCLUSTER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/LARGEPLANTS/LARGESTRANDS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/LARGEPLANTS/UNDERWATERTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/LARGEPROP/LARGELUMP.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/LARGEPROP/LARGEPLATFORMROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/LARGEPROP/LARGEPROP.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/LARGEPROP/LARGESPIKEROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/LARGEPROP/LARGESWIRLPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/LARGEPROP/LARGETUBEROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPLANTS/MEDIUIMGLOWPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPLANTS/MEDIUMJELLYPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPLANTS/MEDIUMSEAPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPROP/MEDIUMGROWTHS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPROP/MEDIUMLUMPS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/SMALLPLANTS/SEABUSH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/ANENOMESHAPE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/CORALLIGHT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/CORALLIGHTINST.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/CORALTRUMPET.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/CRYSTALSSHAPE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/CRYSTALSSHAPELARGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/CURVECORAL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/GASBAGS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/HEXMONOLITH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/MONOLITH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/SMALLMONOLITH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/TALLKELP.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/UNDERWATERCONTOURPOD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/UPDATEPROPS/UNDERWATERSPORE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BEAMSTONE/BEAMSTONE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BEAMSTONE/BURST.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BEAMSTONE/BURSTB.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BEAMSTONE/BURSTC.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BEAMSTONE/HOVERING.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BEAMSTONE/HOVERINGINST.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONEBLOBS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONEFIN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONEFRUIT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONESPINE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONESPORE2.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/CONTOUR/CONTOUROBJECT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/ELBUBBLE/DETAILBUBBLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HEXAGON/GEOMETRIC.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HEXAGON/MEDGEOMETRIC.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HOUDINIPROPS/SPIKYPOTATO.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HYDROGARDEN/HYDROPOD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HYDROGARDEN/HYDROPODDEAD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HYDROGARDEN/HYDROPODFLOAT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HYDROGARDEN/HYDROPODFLOATDEAD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HYDROGARDEN/HYDROPODGROWING.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HYDROGARDEN/HYDROPODGROWINGDEAD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HYDROGARDEN/HYDROPODOFF.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HYDROGARDEN/WEIRDMEDIUMBUSH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/IRRISHELLS/SHELLHUSK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/IRRISHELLS/SHELLSHELF.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/IRRISHELLS/SHELLWHITE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/MSTRUCTURES/FLOATJOINT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/MSTRUCTURES/SINGLEJOINT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/SHARDS/FLOORPIECES.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/SHARDS/FLOORSHARD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/SHARDS/SINGLESHARD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/WIRECELLS/WIRECELLBLOCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/WIRECELLS/WIRECELLFLOATCUBE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/WIRECELLS/WIRECELLSMALLBUSH.SCENE.MBIN",
            "--",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SMALL/SMALLROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/MEDIUMPROPS/MEDIUMVOLCANICROCKS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/MEDIUM/MEDIUMGLOWROCKSINGLE.SCENE.MBIN"
        ]


        detail_objs_defaults = [
            "MODELS/EFFECTS/HEAVYAIR/STONEFRAGMENTS/STONEFRAGMENTS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/CACTUS/HQFURRYCACTUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/FOLIAGE/BARRENGRASSLARGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/FOLIAGE/BARRENGRASSSMALL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/FOLIAGE/GROUNDFLOWER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/FOLIAGE/MEDIUMPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/FOLIAGE/POOFBUSH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/FOLIAGE/YUKKA.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/FOLIAGE/YUKKA02.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/MEDIUMBOULDER01.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/SMALLBOULDER05.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/SMALLROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/HQ/TREES/CACTUSSML.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/PLANTS/FLUFFBUSH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/PLANTS/GROUNDFLOWER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/PLANTS/SCRUBBUSH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/PLANTS/SCRUBGRASS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/PLANTS/SMALLCACTUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/PLANTS/THINBUSHTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/BARREN/PLANTS/VOLUMEBUSH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/BUILDINGS/PARTS/BUILDABLEPARTS/FOLIAGE/WEIRDCUBE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/FLOWERS/BUTTERCUP.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/FLOWERS/SCABIOUS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/FLOWERS/YARROW.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/GRASS/BUBBLELUSHGRASS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/GRASS/LONGALTGRASS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/GRASS/NEWCROSSGRASS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/GRASS/NEWLUSHGRASS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/GRASS/NEWSCRUBGRASS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/GRASS/TALLGRASSBILLBOARD.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/FERN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/FERNLIGHT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/MEDIUMPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/SMALLFLOWERS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/SMALLPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/PLANTS/SPRIGBUSH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/GRAVELPATCHSHINY.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SMALL/FRAGMENTS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SMALL/SMALLROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/GRAVELPATCHMOSSBLEND.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/GRAVELPATCHSANDBLEND.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/GRAVELPATCHSNOWBLEND.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/ROCKS/SURFACEBLEND/MEDIUMSNOWBLENDROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/MEDIUMPROPS/MEDIUMPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/MEDIUMPROPS/MEDIUMROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/SMALLPROPS/SMALLPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/SMALLPROPS/SMALLROCKS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/SMALLPROPS/SMALLROCKSSHARDS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/FROZEN/SMALLPROPS/SNOWFRAGMENTS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/FOLIAGE/FROZENBUSHYGRASS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/FOLIAGE/FROZENGRASSLARGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/SMALLPROPS/ROCKSCREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/SMALLPROPS/SMALLROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/SMALLPROPS/SMALLROCKCLUMPS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/SMALLPROPS/SMALLSNOWCLUMPS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQFROZEN/SMALLPROPS/SNOWCLUMP.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/SMALLPROPS/SMALLBOULDER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSH/SMALLPROPS/SMALLROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSHULTRA/DECORATIVEFERN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSHULTRA/DECORATIVEGRAVELPATCH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/HQLUSHULTRA/DECORATIVESMALLFLOWERS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/SMALLPROPS/LAVACLUMP.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LAVA/SMALLPROPS/LAVAGEMS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/MEDIUM/HOTTENDRILS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/SMALL/GLOWGRASS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/SMALL/SMALLDETAILPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/SMALL/SMALLERODEPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LIVINGSHIP/SMALL/SMALLTENDRIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/SMALLBLUESHROOMS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/LUSHROOM/SMALLSHROOMCLUSTER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/SMALL/CURVEDSMALL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/RADIOACTIVE/SMALL/CURVEFRAGMENT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/SMALL/LEAFDROPLET.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/SMALL/SMALLROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/SCORCHED/SMALL/SMALLSPIRE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/MEDIUM/MEDIUMPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/SMALL/BLOBFRAGMENTS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/SMALL/SMALLROCK.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/SMALL/SMALLTOXICEGG.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/SMALL/SPOREBARNACLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/SMALL/SPORETUBESMALL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/TOXIC/SMALL/TOXICGRASS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/LARGEPLANTS/LARGESTRANDS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/LARGEPLANTS/UNDERWATERTREE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPLANTS/MEDIUIMGLOWPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPLANTS/MEDIUMJELLYPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPLANTS/MEDIUMSEAPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPROP/MEDIUMLUMPS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/MEDIUMPROP/SEAURCHIN.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/UNDERWATER/SMALLPLANTS/SEABUSH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BEAMSTONE/SMALLSTONE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONEBLOBS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONEFRUIT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/BONESPIRE/BONEGRASS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/CONTOUR/CONTOURDETAIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/ELBUBBLE/DEADBUBBLE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/FRACTALCUBE/CYLINDER.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/FRACTALCUBE/FLAP.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HEXAGON/DETAILSHAPE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HEXAGON/DETAILSHAPEB.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HEXAGON/HOVERINGDETAIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HEXAGON/ROTATINGDETAIL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/HOUDINIPROPS/SPIKYPOTATO.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/IRRISHELLS/SHELLCRYSTALSLICES.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/IRRISHELLS/SHELLGRASS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/MSTRUCTURES/SMALLJOINT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/WIRECELLS/WIRECELLFRAGMENTS.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/WEIRD/WIRECELLS/WIRECELLGRASS.SCENE.MBIN",
            "--",
            "MODELS/PLANETS/BIOMES/CAVE/SMALLPLANT/SMALLCAVEBUSH.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/CAVE/SMALLPROP/SMALLGLOWPLANT.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/GRASS/BARRENGRASSLARGE.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/GRASS/BARRENGRASSSMALL.SCENE.MBIN",
            "MODELS/PLANETS/BIOMES/COMMON/GRASS/CROSSGRASS.SCENE.MBIN"
        ]

        return placement_defaults, distant_objs_defaults, landmarks_defaults, objs_defaults, detail_objs_defaults
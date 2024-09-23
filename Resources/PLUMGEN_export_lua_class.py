'''
File: PLUMGEN_export_class.py
'''

import os   # os interactions
import sys
import re
import logging
from tkinter import messagebox
import tkinter as tk

# no file imports

class PlumgenExportLuaClass():

    def __init__(self, prop_dist, global_dist, 
        biomes_objs,
        bfn_all_biome_files_weights,
        bfn_all_valid_start_planets,
        bfn_all_tile_types,
        all_biome_tile_types,
        timestamp):

        self.logger = logging.getLogger(__name__)  #set up logging
    
        try:
            
            self.prop_dist = prop_dist # bool
            self.global_dist = global_dist # bool

            self.biomes_objs = biomes_objs
            self.bfn_all_biome_files_weights = bfn_all_biome_files_weights
            self.bfn_all_valid_start_planets = bfn_all_valid_start_planets
            self.bfn_all_tile_types =bfn_all_tile_types
            self.all_biome_tile_types = all_biome_tile_types

            self.timestamp = timestamp

            self.subfolder = '_BIOMES Exmls Folder Goes Here'

            # check if the code is frozen (compiled to exe) or running as a script
            if getattr(sys, 'frozen', False):
                # if frozen (and running as exe), use this path
                current_directory = os.path.dirname(sys.executable)
                self.lua_biomes_path = os.path.abspath(os.path.join(current_directory, 'Lua Parts', 'biomes'))
                self.lua_spawner_path = os.path.abspath(os.path.join(current_directory, 'Lua Parts', 'spawner'))
                self.save_luas_path = os.path.abspath(os.path.join(current_directory,'__Exported Mod Files', f"New Mod {self.timestamp}"))
            else:
                # if running as script, use this path
                current_directory = os.path.dirname(os.path.realpath(__file__))
                self.lua_biomes_path = os.path.abspath(os.path.join(current_directory, '..', 'Lua Parts', 'biomes'))
                self.lua_spawner_path = os.path.abspath(os.path.join(current_directory, '..', 'Lua Parts', 'spawner'))
                self.save_luas_path = os.path.abspath(os.path.join(current_directory, '..', '__Exported Mod Files', f"New Mod {self.timestamp}"))

            # create save_luas_path if it doesn't exist
            os.makedirs(self.save_luas_path, exist_ok=True)

            # check if 2 directories exist
            if not os.path.exists(self.lua_biomes_path):
                print(f"Directory '{self.lua_biomes_path}' does not exist.")
            if not os.path.exists(self.lua_spawner_path):
                print(f"Directory '{self.lua_spawner_path}' does not exist.")
            
            # initialize variables with default values
            self.header_reg_draw_1a = ""
            self.header_far_draw_1b = ""
            self.header_near_draw_1c = ""
            self.body_2 = ""
            self.biome_3a1 = ""
            self.biome_last_3a2 = ""
            self.biome_dist_3b = ""
            self.biome_landm_3c = ""
            self.biome_obj_3d = ""
            self.biome_detail_3e = ""
            self.biome_end_3f = ""
            self.global_distance_4a = ""
            self.footer_4b = ""

            self.header_1 = ""
            self.bfn_start_2 = ""
            self.each_planet_type_3 = ""
            self.each_filename_weight_4 = ""
            self.valid_start_5 = ""
            self.each_valid_start_planet_6 = ""
            self.common_ext_objs_7 = ""
            self.each_tiletype_8 = ""
            self.each_tiletype_options_9 = ""
            self.each_biome_start_10 = ""
            self.each_biome_tiletype_11 = ""
            self.biome_tiletype_options_12 = ""
            self.close_each_biome_13 = ""
            self.footer_14 = ""
            
            # populate parts of the lua files, to be used later when exporting
            self.populate_biome_objects_parts()
            self.populate_biome_spawner_parts()

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
    def get_biomes_lua_filepath(self):
        return self.first_save_path
    
    def get_spawner_lua_filepath(self):
        return self.second_save_path


    def extract_and_format_ending_name(self, filename):
        file_parts = re.split(r'[\\\/]', filename)  # split filename by '/' or '\'
        ending_name = file_parts[-1].capitalize().replace(" ", "_")  # extract last part, capitalize first letter, replace spaces w/ underscores
        return ending_name


    def make_nms_filename(self, filename):
        file_parts = re.split(r'[\\\/]', filename) # split filename by '/' or '\'
        formatted_filename = '/'.join(part.upper().replace(' ', '_') for part in file_parts) # join parts with '_' and convert to uppercase
        new_filename = f"METADATA/SIMULATION/SOLARSYSTEM/{formatted_filename}.MBIN" # construct new filename
        
        return new_filename



    # export biome objects lua
    def export_biome_objects(self, author, biomes_filen):
        '''
        self.header_reg_draw_1a
        self.header_far_draw_1b
        self.header_near_draw_1c
        self.body_2 ------- @mod_title@ @mod_author@ @biome_name@
        self.biome_3 ------- @biome_name1@ @biome_name2@ @Distant@ @Landmark@ @Object@ @Detail@
        self.biome_3a1 ------- @biome_name1@ @biome_name2@
        self.biome_last_3a2 ------- @biome_name1@
        self.biome_dist_3b ------- @Distant@
        self.biome_landm_3c ------- @Landmark@
        self.biome_obj_3d ------- @Object@
        self.biome_detail_3e ------- @AddDetailPropOption@ @Detail@
        self.biome_end_3f
        self.global_distance_4a
        self.footer_4b
        '''

        try:
            
            entered_author = author
            entered_biomes_filen = biomes_filen

            first_filen_with_timestamp = f"____zBiomes_{entered_biomes_filen}.lua"
            self.first_save_path = os.path.abspath(os.path.join(self.save_luas_path, first_filen_with_timestamp))

            # detail filenames = add wind, etc to exml
            windy_detail_objects = [
                "MODELS/PLANETS/BIOMES/BARREN/HQ/FOLIAGE/BARRENGRASSLARGE.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/BARREN/HQ/FOLIAGE/BARRENGRASSSMALL.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/BARREN/HQ/FOLIAGE/GROUNDFLOWER.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/BARREN/PLANTS/SCRUBGRASS.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/COMMON/GRASS/BUBBLELUSHGRASS.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/COMMON/GRASS/LONGALTGRASS.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/COMMON/GRASS/NEWCROSSGRASS.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/COMMON/GRASS/NEWLUSHGRASS.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/COMMON/GRASS/NEWSCRUBGRASS.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/COMMON/GRASS/TALLGRASSBILLBOARD.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/HQFROZEN/FOLIAGE/FROZENBUSHYGRASS.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/HQFROZEN/FOLIAGE/FROZENGRASSLARGE.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/LIVINGSHIP/SMALL/GLOWGRASS.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/COMMON/GRASS/BARRENGRASSLARGE.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/COMMON/GRASS/BARRENGRASSSMALL.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/COMMON/GRASS/CROSSGRASS.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/BURNT/DETAIL/BURNTTALLGRASS.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/FLORAL/MEDIUMPLANT/FOXGLOVE.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/FLORAL/SMALLPLANT/FLORALPLANTSMALL.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/FLORAL/SMALLPLANT/FLORALPLANTSMALL02.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/NOXIOUS/DETAIL/NOXIOUSGRASS.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/NOXIOUS/DETAIL/NOXIOUSTALLGRASS.SCENE.MBIN",
                "MODELS/PLANETS/BIOMES/SUBZERO/DETAIL/SUBZEROTALLGRASS.SCENE.MBIN"
            ]

            # strings require quotes when passed as arguments in lua funciton
            add_quotes_indices = [0, 1, 2, 16, 17, 18, 19]

            with open(self.first_save_path, "w") as lua_file:

                for idx, biome in enumerate(self.biomes_objs):

                    if '.MBIN' not in biome.get_filename():
                        filename = biome.get_filename()
                    ending_name = self.extract_and_format_ending_name(filename) # get ending word
                    nms_filename = self.make_nms_filename(filename) # add .MBIN, etc.

                    # only do this once, at the start
                    if idx == 0:

                        if self.prop_dist == "far": # True
                            lua_file.write(self.header_far_draw_1b)
                        elif self.prop_dist == "regular":
                            lua_file.write(self.header_reg_draw_1a)
                        else:
                            lua_file.write(self.header_near_draw_1c)



                        body_2_ed = self.body_2 \
                            .replace("@mod_title@", f"____Biomes_{entered_biomes_filen}") \
                            .replace("@mod_author@", entered_author) \
                            .replace("@biome_name@", nms_filename)
                        
                        lua_file.write(body_2_ed)


                    # check if it's the last biome in list, if so, don't copy the last file
                    if idx + 1 < len(self.biomes_objs):
                        next_biome = self.biomes_objs[idx + 1]
                        next_filename = next_biome.get_filename()
                        next_nms_filename = self.make_nms_filename(next_filename)

                        # copy file to continue making biome files
                        biome_3a1_ed = self.biome_3a1 \
                            .replace("@biome_name1@", nms_filename) \
                            .replace("@biome_name2@", next_nms_filename)
                        
                        lua_file.write(biome_3a1_ed)

                    else: # do not copy file, last biome
                        biome_last_3a2_ed = self.biome_last_3a2.replace("@biome_name1@", nms_filename)
                        lua_file.write(biome_last_3a2_ed)
                    
                    # reverse = exported exml order the same as imported exml, i.e. prop order
                    for distant_obj_list in reversed(biome.get_distant_obj_lists()):
                        if '.MBIN' in distant_obj_list[1]:  # verify '.MBIN' string is in the model filepath (otherwise would cause crash)
                            items = [] # empty list ot store prop attributes
                            for i, item in enumerate(distant_obj_list[:24]): # iterate over attributes from index 0-18
                                if item == "": items.append('"' + "FOREST" + '"') # check if missing placement
                                elif isinstance(item, bool): items.append('"' + "TRUE" + '"') # check if missing all caps bool
                                elif i in add_quotes_indices: items.append('"' + str(item) + '"') # add quotes to certain indices
                                else: items.append(str(item))
                            function_arguments = ', '.join(items) # join items into a single string
                            biome_dist_3b_ed = self.biome_dist_3b.replace("@Distant@", function_arguments) # returns entirely new string
                            lua_file.write(biome_dist_3b_ed) # write function call to lua script

                    for landmark_list in reversed(biome.get_landmark_lists()):
                        if '.MBIN' in landmark_list[1]:
                            items = []
                            for i, item in enumerate(landmark_list[:24]):
                                if item == "": items.append('"' + "FOREST" + '"')
                                elif isinstance(item, bool): items.append('"' + "TRUE" + '"')
                                elif i in add_quotes_indices: items.append('"' + str(item) + '"')
                                else: items.append(str(item))
                            function_arguments = ', '.join(items)
                            biome_landm_3c_ed = self.biome_landm_3c.replace("@Landmark@", function_arguments)
                            lua_file.write(biome_landm_3c_ed)

                    for objects_list in reversed(biome.get_objects_lists()):
                        if '.MBIN' in objects_list[1]:
                            items = []
                            for i, item in enumerate(objects_list[:24]):
                                if item == "": items.append('"' + "FOREST" + '"')
                                elif isinstance(item, bool): items.append('"' + "TRUE" + '"')
                                elif i in add_quotes_indices: items.append('"' + str(item) + '"')
                                else: items.append(str(item))
                            function_arguments = ', '.join(items)
                            biome_obj_3d_ed = self.biome_obj_3d.replace("@Object@", function_arguments)
                            lua_file.write(biome_obj_3d_ed)

                    for detail_obj_list in reversed(biome.get_detail_obj_lists()):
                        if '.MBIN' in detail_obj_list[1]:
                            function_call = ""
                            if detail_obj_list[1] in windy_detail_objects:
                                function_call = "AddGrassProp"
                            else:
                                function_call = "AddRockProp"
                            
                            items = []
                            for i, item in enumerate(detail_obj_list[:24]):
                                if item == "": items.append('"' + "FOREST" + '"')
                                elif isinstance(item, bool): items.append('"' + "TRUE" + '"')
                                elif i in add_quotes_indices: items.append('"' + str(item) + '"')
                                else: items.append(str(item))
                            function_arguments = ', '.join(items)

                            biome_detail_3e_ed = self.biome_detail_3e \
                            .replace("@AddDetailPropOption@", function_call) \
                            .replace("@Detail@", function_arguments)

                            lua_file.write(biome_detail_3e_ed)

                    # close call prop functions section
                    lua_file.write(self.biome_end_3f)

                # after loop - close lua file
                if self.global_dist:  # True
                    lua_file.write(self.global_distance_4a)
                else:
                    lua_file.write(self.footer_4b)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    

    # export biome spawner lua
    def export_biome_spawner(self, author, spawner_filen):
        '''
        self.header_1
        self.bfn_start_2 ------- @mod_title@ @mod_author@
        self.each_planet_type_3 ------- @planetType@
        self.each_filename_weight_4 ------- @sub_type@, @filename@, @weight@
        self.valid_start_5
        self.each_valid_start_planet_6 ------- @biome_type@
        self.common_ext_objs_7
        self.each_tiletype_8 ------- @weight@, @tile_type@
        self.each_tiletype_options_9 ------- @biome_objects_name@
        self.each_biome_start_10 ------- @each_biome_mbin@
        self.each_biome_tiletype_11 ------- @tile_type@
        self.biome_tiletype_options_12 ------- @biome_objects_name@
        self.close_each_biome_13
        self.footer_14
        '''

        try:
            
            entered_author = author
            entered_spawner_filen = spawner_filen

            second_filen_with_timestamp = f"____zSpawner_{entered_spawner_filen}.lua"
            self.second_save_path = os.path.abspath(os.path.join(self.save_luas_path, second_filen_with_timestamp))


            with open(self.second_save_path, "w") as lua_file:

                #lua_file.write()
                
                lua_file.write(self.header_1)


                bfn_start_2_ed = self.bfn_start_2 \
                    .replace("@mod_title@", f"____Spawner_{entered_spawner_filen}") \
                    .replace("@mod_author@", entered_author)
                lua_file.write(bfn_start_2_ed)


                #####----- self.bfn_all_biome_files_weights - REVERSE: start with last, otherwise game crash
                for biome_files_weights in reversed(self.bfn_all_biome_files_weights):
                    for biome_name, biome_data in reversed(biome_files_weights.items()):

                        each_planet_type_3_ed = self.each_planet_type_3.replace("@planetType@", biome_name) # i.e. Lush
                        lua_file.write(each_planet_type_3_ed)

                        for data in reversed(biome_data):
                            filename = list(data.keys())[0]
                            wt_stype = data[filename]
                            weight, sub_type, prpl_weight = wt_stype.split()

                            #make sub_type quotes??

                            each_filename_weight_4_ed = self.each_filename_weight_4 \
                                .replace("@sub_type@", sub_type) \
                                .replace("@filename@", filename) \
                                .replace("@weight@", weight) \
                                .replace("@prpl_weight@", prpl_weight)
                            lua_file.write(each_filename_weight_4_ed)


                # valid starting planets
                lua_file.write(self.valid_start_5)

                for valid_planet in reversed(self.bfn_all_valid_start_planets):

                    each_valid_start_planet_6_ed = self.each_valid_start_planet_6.replace("@biome_type@", valid_planet)
                    lua_file.write(each_valid_start_planet_6_ed)


                # self.bfn_all_tile_types - bfn CommonExternalObjectLists tiletypes
                lua_file.write(self.common_ext_objs_7)

                for tile_weight, values in reversed(self.bfn_all_tile_types.items()):

                    tile_type, weight = tile_weight.split()

                    tile_type_ed = re.sub(r'\d+$', '', tile_type) # remove trailing numbers


                    each_tiletype_8_ed = self.each_tiletype_8 \
                        .replace("@weight@", weight) \
                        .replace("@tile_type@", tile_type_ed)
                    lua_file.write(each_tiletype_8_ed)

                    for filen in reversed(values):
                        each_tiletype_options_9_ed = self.each_tiletype_options_9.replace("@biome_objects_name@", filen)
                        lua_file.write(each_tiletype_options_9_ed)



                # each biome file - self.all_biome_tile_types
                for biome_tile_types in reversed(self.all_biome_tile_types):

                    each_filen = biome_tile_types['Filename']

                    filepath_parts = each_filen.split(self.subfolder) # format filename, so it's shorter
                    if len(filepath_parts) > 1:
                        each_filen = filepath_parts[-1]
                        each_filen = re.sub(r'[\\/]+', '/', each_filen) # remove consecutive slashes or backslashes
                        new_filename = "METADATA/SIMULATION/SOLARSYSTEM/" + each_filen

                    each_biome_start_10_ed = self.each_biome_start_10.replace("@each_biome_mbin@", new_filename)
                    lua_file.write(each_biome_start_10_ed)

                    for key, biome_names in reversed(biome_tile_types.items()): # populate listbox with data
                        if key != 'Filename':
                            #listbox.insert(tk.END, f"{key}: {value}")

                            each_tile_type, each_weight = key.split()

                            each_tile_type_ed = re.sub(r'\d+$', '', each_tile_type) # remove trailing numbers

                            each_biome_tiletype_11_ed = self.each_biome_tiletype_11 \
                                    .replace("@weight@", each_weight) \
                                    .replace("@tile_type@", each_tile_type_ed)
                            lua_file.write(each_biome_tiletype_11_ed)

                            for biome_name in reversed(biome_names):
                                biome_name = biome_name.replace(' ', '_') # replace spaces with underscores
                                biome_tiletype_options_12_ed = self.biome_tiletype_options_12.replace("@biome_objects_name@", biome_name)
                                lua_file.write(biome_tiletype_options_12_ed)

                # close lua file
                lua_file.write(self.close_each_biome_13)
                lua_file.write(self.footer_14)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))







    # open file, set contents to variable
    def read_lua_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file '{file_path}': {e}")
            return None


    # populate biome objects parts
    def populate_biome_objects_parts(self):
        self.header_reg_draw_1a = self.read_lua_file(os.path.join(self.lua_biomes_path, '1a_header_reg_draw.lua'))
        self.header_far_draw_1b = self.read_lua_file(os.path.join(self.lua_biomes_path, '1b_header_far_draw.lua'))
        self.header_near_draw_1c = self.read_lua_file(os.path.join(self.lua_biomes_path, '1c_header_near_draw.lua'))
        self.body_2 = self.read_lua_file(os.path.join(self.lua_biomes_path, '2_body.lua'))

        self.biome_3a1 = self.read_lua_file(os.path.join(self.lua_biomes_path, '3a1_biome.lua'))
        self.biome_last_3a2 = self.read_lua_file(os.path.join(self.lua_biomes_path, '3a2_biome_last.lua'))
        self.biome_dist_3b = self.read_lua_file(os.path.join(self.lua_biomes_path, '3b_biome_dist.lua'))
        self.biome_landm_3c = self.read_lua_file(os.path.join(self.lua_biomes_path, '3c_biome_landm.lua'))
        self.biome_obj_3d = self.read_lua_file(os.path.join(self.lua_biomes_path, '3d_biome_obj.lua'))
        self.biome_detail_3e = self.read_lua_file(os.path.join(self.lua_biomes_path, '3e_biome_detail.lua'))
        self.biome_end_3f = self.read_lua_file(os.path.join(self.lua_biomes_path, '3f_biome_end.lua'))

        self.global_distance_4a = self.read_lua_file(os.path.join(self.lua_biomes_path, '4a_global_distance.lua'))
        self.footer_4b = self.read_lua_file(os.path.join(self.lua_biomes_path, '4b_footer.lua'))


    # populate biome spawner parts
    def populate_biome_spawner_parts(self):
        self.header_1 = self.read_lua_file(os.path.join(self.lua_spawner_path, '1_header.lua'))
        self.bfn_start_2 = self.read_lua_file(os.path.join(self.lua_spawner_path, '2_bfn_start.lua'))
        self.each_planet_type_3 = self.read_lua_file(os.path.join(self.lua_spawner_path, '3_each_planet_type.lua'))
        self.each_filename_weight_4 = self.read_lua_file(os.path.join(self.lua_spawner_path, '4_each_filename_weight.lua'))
        self.valid_start_5 = self.read_lua_file(os.path.join(self.lua_spawner_path, '5_valid_start.lua'))
        self.each_valid_start_planet_6 = self.read_lua_file(os.path.join(self.lua_spawner_path, '6_each_valid_start_planet.lua'))
        self.common_ext_objs_7 = self.read_lua_file(os.path.join(self.lua_spawner_path, '7_common_ext_objs.lua'))
        self.each_tiletype_8 = self.read_lua_file(os.path.join(self.lua_spawner_path, '8_each_tiletype.lua'))
        self.each_tiletype_options_9 = self.read_lua_file(os.path.join(self.lua_spawner_path, '9_each_tiletype_options.lua'))
        self.each_biome_start_10 = self.read_lua_file(os.path.join(self.lua_spawner_path, '10_each_biome_start.lua'))
        self.each_biome_tiletype_11 = self.read_lua_file(os.path.join(self.lua_spawner_path, '11_each_biome_tiletype.lua'))
        self.biome_tiletype_options_12 = self.read_lua_file(os.path.join(self.lua_spawner_path, '12_biome_tiletype_options.lua'))
        self.close_each_biome_13 = self.read_lua_file(os.path.join(self.lua_spawner_path, '13_close_each_biome.lua'))
        self.footer_14 = self.read_lua_file(os.path.join(self.lua_spawner_path, '14_footer.lua'))
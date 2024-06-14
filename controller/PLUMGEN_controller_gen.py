'''
File: PLUMGEN_controller_gen.py
'''

import os   # os interactions
import sys
import re
import tkinter as tk
import csv
import random
import copy
import json
import xml.etree.ElementTree as ET
import logging
from tkinter import messagebox

from model.PLUMGEN_model_gen import PlumgenModelGen
from model.PLUMGEN_model_gen import DefaultModelPaths
from model.PLUMGEN_model_gen import DefaultSpawnDensityList
from view.PLUMGEN_view_gen import PlumgenViewGen


class PlumgenControllerGen():
    def __init__(self):

        self.logger = logging.getLogger(__name__)  #set up logging
        
        try:
                
            self.root = tk.Tk()

            self.subfolder = '_BIOMES Exmls Folder Goes Here'
            self.default_subfolder = 'Defaults Json'

            # check if the code is frozen (compiled to exe) or running as script
            if getattr(sys, 'frozen', False):
                # if frozen (and running as exe), use these paths:
                current_directory = os.path.dirname(sys.executable)
                #self.plum_exe = os.path.abspath(os.path.join(current_directory, '_PLUMGEN.exe'))
                self.resources_path = os.path.abspath(os.path.join(current_directory, '_Biome Templates'))
                self.presets_path = os.path.abspath(os.path.join(current_directory, '_Presets'))
                self.csv_file = os.path.abspath(os.path.join(current_directory, '_Biome Templates', '_Current Vanilla+Pre NMS.csv'))
                self.biome_exmls_folder_dir = os.path.abspath(os.path.join(current_directory, self.subfolder))
                self.default_bfn_folder_dir = os.path.abspath(os.path.join(current_directory, self.default_subfolder))
                self.json_lang_path = os.path.abspath(os.path.join(self.default_bfn_folder_dir, 'languages.json'))
            else:
                # if running as script, use these paths:
                current_directory = os.path.dirname(os.path.realpath(__file__))
                #self.plum_exe = None
                self.resources_path = os.path.abspath(os.path.join(current_directory, '..', '_Biome Templates'))
                self.presets_path = os.path.abspath(os.path.join(current_directory, '..', '_Presets'))
                self.csv_file = os.path.abspath(os.path.join(current_directory, '..', '_Biome Templates', '_Current Vanilla+Pre NMS.csv'))
                self.biome_exmls_folder_dir = os.path.abspath(os.path.join(current_directory, '..', self.subfolder))
                self.default_bfn_folder_dir = os.path.abspath(os.path.join(current_directory, '..', self.default_subfolder))
                self.json_lang_path = os.path.abspath(os.path.join(self.default_bfn_folder_dir, 'languages.json'))

            #if not os.path.exists(self.csv_file): # check if the file exists
            #    print("_Current Vanilla+Pre NMS.csv file not found in '_Biome Templates' folder.")

            self.name = ""
            self.counter = 0
            self.copy_counter = 1
            self.matching_lists_count = []
            self.biome_objs = [] # list of all biome objects
            self.csv_compare_list = ["Filename", "Placement", "MinHeight", "MaxHeight", "MinAngle", "MaxAngle",
                        "MinScale", "MaxScale", "MinScaleY", "MaxScaleY", "PatchEdgeScaling",
                        "MaxXZRotation", "DestroyedByPlayerShip", "DestroyedByTerrainEdit",
                        "CreaturesCanEat", "Coverage", "FlatDensity", "SlopeDensity", "SlopeMultiplier", "DrawDistance"] #v4
            

            # store imported EXMLs
            self.bfn_all_biome_files_weights = []
            self.bfn_all_tile_types = {}
            self.bfn_all_valid_start_planets = []
            
            self.all_biome_tile_types = [] # **each** biome file

            # create separate instance of default model paths, to be passed to PlumgenModelGen instance objects
            self.model_paths = DefaultModelPaths()
            self.set_default_model_list()
            # copy of default model paths, if first is overwritten (via. gen using biome template data checkbox)
            self.placem_defaults, self.dist_defaults, self.landm_defaults, self.objs_defaults, self.detail_defaults = self.model_paths.create_default_model_paths()

            # get dictionary of default spawndensitylist strings
            self.sdl = DefaultSpawnDensityList()
            self.default_spawndensitylist = self.sdl.create_default_sdl()

            # get language
            self.langs = None
            self.get_set_lang_from_json_update_plum()
            # if new language window prompt, continue with making window anyway
            if self.langs["Lan"] == "TBD":
                self.lan = "English" # temporarily default to english if none selected
            else:
                self.lan = self.langs["Lan"]

            # pass to new view links on root frame and controller object
            #self.root.title("PLUMGEN - Biome Objects")
            self.root.title(f"v1.1 - {self.langs[self.lan]["controller_init"]["main_title"]}")
            self.view = PlumgenViewGen(self.root, self, self.langs, self.lan)

            self.data = self.load_csv_data()

            self.root.mainloop()

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    def confirm_language_selection(self):
        
        selected_lang = self.selected_language.get() # set new selected language

        confirm = messagebox.askyesno(self.langs[selected_lang]["controller_init"]["confirm"], 
                                    self.langs[selected_lang]["controller_init"]["confirm_desc"], parent=self.lang_window)
        if confirm:
        
            self.lang_window.destroy() # destroy window

            # update JSON file with selected language
            with open(self.json_lang_path, 'r+', encoding='utf-8') as file:
                self.langs = json.load(file)
                self.langs["Lan"] = selected_lang
                file.seek(0)
                json.dump(self.langs, file, indent=4, ensure_ascii=False)
                file.truncate()

            if self.new_lang: # if user selected to choose new lang using main menu
                if messagebox.askyesno(self.langs[selected_lang]["on_close"]["close_title"], self.langs[selected_lang]["on_close"]["close_desc"], parent=self.root):
                    
                    if getattr(sys, 'frozen', False):
                        # if frozen (and running as exe), use these paths:
                        #current_directory = os.path.dirname(sys.executable)
                        os.execl(sys.executable, sys.executable, *sys.argv)
                        #subprocess.Popen(sys.executable)
                        #self.root.destroy()


    def prompt_lang_select(self):
        # new window to select language
        self.lang_window = tk.Toplevel(self.root)
        self.lang_window.title("Language")
        self.lang_window.configure(bg="#333333")
        self.lang_window.geometry("400x125")
        self.lang_window.resizable(False, False)  # prevent resizing
        self.lang_window.grab_set()  # prevent this window from going behind main window

        self.selected_language = tk.StringVar(value="English") # store selected language

        languages = [ # language options
            "Chinese - Simplified (简体中文)",
            "English",
            "Finnish (Suomi)",
            "French (Français)",
            "German (Deutsch)",
            "Italian (Italiano)",
            "Japanese (日本語)",
            "Korean (한국어)",
            "Portuguese (Português)",
            "Russian (Русский)",
            "Spanish (Español)",
                ]

        # dropdown menu for language selection
        lang_dropdown = tk.OptionMenu(self.lang_window, self.selected_language, *languages)
        lang_dropdown.grid(row=0, column=0, padx=(50,25), pady=(50,50), sticky=tk.NSEW)
        lang_dropdown.config(bg='gray30', fg='white')
        lang_dropdown["menu"].config(bg='gray30', fg='white')

        # confirm button
        confirm_button = tk.Button(self.lang_window, text=">>>", command=self.confirm_language_selection)
        confirm_button.grid(row=0, column=1, padx=(25,50), pady=(50,50), sticky=tk.NSEW)
        confirm_button.config(bg='#38943a', fg='white')

        # center elements vert & horiz
        self.lang_window.grid_columnconfigure(0, weight=1)
        self.lang_window.grid_columnconfigure(1, weight=1)
        self.lang_window.grid_rowconfigure(0, weight=1)


    def get_set_lang_from_json_update_plum(self, force_select_new_lang=False):
        self.new_lang = force_select_new_lang
        
        with open(self.json_lang_path, 'r+', encoding='utf-8') as file:
            self.langs = json.load(file)

        if self.langs["Lan"] == "TBD" or self.new_lang:
            self.prompt_lang_select() # on startup, ask for language
    
        self.lan = self.langs["Lan"]



    def show_error_message(self, message, max_length=200):
        if len(message) > max_length:
            truncated_message = message[:max_length] + "..."
        else:
            truncated_message = message
        messagebox.showerror("Error", f"{truncated_message}\n\nIf you're struggling to resolve this error, please share the 'plumgen.log' file with the dev.", master=None)


    # getter methods
    def get_presets_path(self):
        return self.presets_path

    def get_default_bfn_folder_dir(self):
        return self.default_bfn_folder_dir
    def get_biom_exmls_folder_dir(self):
        return self.biome_exmls_folder_dir
    
    def get_bfn_all_biome_files_weights(self):
        return self.bfn_all_biome_files_weights
    def get_bfn_all_tile_types(self):
        return self.bfn_all_tile_types
    def get_bfn_all_valid_start_planets(self):
        return self.bfn_all_valid_start_planets
    def get_all_biome_tile_types(self):
        return self.all_biome_tile_types

    def get_placem_list(self):
        return self.placem_list

    def get_dist_list(self):
        return self.dist_list

    def get_landm_list(self):
        return self.landm_list

    def get_objs_list(self):
        return self.objs_list

    def get_detail_list(self):
        return self.detail_list
    

    def get_resources_path(self):
        return self.resources_path
    

    def get_sdl(self):
        return self.default_spawndensitylist

    def get_csv_file(self):
        return self.csv_file
    
    def get_biome_objs(self):
        return self.biome_objs

    
    def get_placem_defaults(self):
        return self.placem_defaults

    def get_dist_defaults(self):
        return self.dist_defaults

    def get_landm_defaults(self):
        return self.landm_defaults

    def get_objs_defaults(self):
        return self.objs_defaults

    def get_detail_defaults(self):
        return self.detail_defaults


    # setter methods
    def set_bfn_all_biome_files_weights(self, bfn_all_biome_files_weights):
        self.bfn_all_biome_files_weights = bfn_all_biome_files_weights
    def set_bfn_all_tile_types(self, bfn_all_tile_types):
        self.bfn_all_tile_types = bfn_all_tile_types
    def set_bfn_all_valid_start_planets(self, bfn_all_valid_start_planets):
        self.bfn_all_valid_start_planets = bfn_all_valid_start_planets
    def set_all_biome_tile_types(self, all_biome_tile_types):
        self.all_biome_tile_types = all_biome_tile_types

    def set_csv_file_data(self, filename):
        self.csv_file = os.path.abspath(os.path.join(self.resources_path, filename))
        self.data = self.load_csv_data()

    def set_default_model_list(self):
        # set for all: current/future and past biomes
        self.placem_list, self.dist_list, self.landm_list, self.objs_list, self.detail_list = self.model_paths.create_default_model_paths()
        for biome_obj in self.biome_objs:
            biome_obj.set_distant_objs_defaults(self.dist_list)
            biome_obj.set_landmarks_defaults(self.landm_list)
            biome_obj.set_objs_defaults(self.objs_list)
            biome_obj.set_detail_objs_defaults(self.detail_list)


    # set custom model list as the 'key' (based on the biome template) when generating new biomes
    def set_custom_model_list(self):
        column_1_data = [row['Filename'] for row in self.data if 'Filename' in row]
        category_column_data = [row['DrawDistance'] for row in self.data if 'DrawDistance' in row]

        # clear default temp lists
        temp_dist_def = []
        temp_landm_def = []
        temp_objs_def = []
        temp_detail_def = []

        seen_strings = {'DistantObjects': set(), 'Landmarks': set(), 'Objects': set(), 'DetailObjects': set()}

        for string, category in zip(column_1_data, category_column_data):
            if category and string not in seen_strings[category]:
                # add filename to the corresponding list based on the drawdistance category
                if category == 'DistantObjects':
                    temp_dist_def.append(string)
                elif category == 'Landmarks':
                    temp_landm_def.append(string)
                elif category == 'Objects':
                    temp_objs_def.append(string)
                elif category == 'DetailObjects':
                    temp_detail_def.append(string)

                seen_strings[category].add(string)

        # assign current/future biomes, even if empty (checks if empty later in model_gen)
        self.dist_list = temp_dist_def
        self.landm_list = temp_landm_def
        self.objs_list = temp_objs_def
        self.detail_list = temp_detail_def

        # assign past biomes
        for biome_obj in self.biome_objs:
            biome_obj.set_distant_objs_defaults(temp_dist_def)
            biome_obj.set_landmarks_defaults(temp_landm_def)
            biome_obj.set_objs_defaults(temp_objs_def)
            biome_obj.set_detail_objs_defaults(temp_detail_def)


    def set_custom_placem_list(self):
        placement_column_data = [row['Placement'] for row in self.data if 'Placement' in row]

        unique_placement_strings = set()

        for string in placement_column_data:
            if string:
                unique_placement_strings.add(string)

        self.placem_list = list(unique_placement_strings)


    # csv data methods ----------------------------------------------------
        
    def load_csv_data(self):
        data = []
        with open(self.csv_file, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            
            # first row in CSV file = column headers
            columns = next(csv_reader)
            
            for row in csv_reader:
                # create a dictionary for each row
                row_dict = {column: value for column, value in zip(columns, row)}
                data.append(row_dict)
                
        return data


    def compare_and_update(self, target_list):
        matching_lists = []

        for row in self.data:
            if row['Filename'] == target_list[0]:
                #matching_list = [row[column] for column in self.csv_compare_list]
                #replace '\' with '/'
                matching_list = [row[column].replace('\\', '/') for column in self.csv_compare_list]
                matching_lists.append(matching_list)

        #print(f"target_list 1: {target_list}")
        self.matching_lists_count = matching_lists # assign matching items

        if matching_lists:
            selected_matching_list = random.choice(matching_lists)
            # Update values in target_list with the randomly selected matching_list values
            for i in range(len(self.csv_compare_list)):
                target_list[i] = selected_matching_list[i]
        
        #print(f"matching_lists: {matching_lists}")
        #print(f"target_list 2: {target_list}\n")


    def compare_and_recount(self, target_list):
        matching_lists = []

        for row in self.data:
            if row['Filename'] == target_list[0]:
                matching_list = [row[column] for column in self.csv_compare_list]
                matching_lists.append(matching_list)

        self.matching_lists_count = matching_lists # assign matching items


    def recount_models(self):
        for biome_obj in self.biome_objs:
            distant_obj_lists = biome_obj.get_distant_obj_lists()
            landmark_lists = biome_obj.get_landmark_lists()
            objects_lists = biome_obj.get_objects_lists()
            detail_obj_lists = biome_obj.get_detail_obj_lists()

            all_lists_curr_biome = [distant_obj_lists, landmark_lists, objects_lists, detail_obj_lists]

            for i, lists in enumerate(all_lists_curr_biome):
                for j, target_list in enumerate(lists):
                    self.compare_and_recount(target_list)
                    
                    #index = next(index for index, inner_list in enumerate(lists) if inner_list[0] == target_list[0])

                    if i == 0:
                        biome_obj.set_all_distant_model_similar_props(j, self.matching_lists_count)
                    elif i == 1:
                        biome_obj.set_all_landmark_model_similar_props(j, self.matching_lists_count)
                    elif i == 2:
                        biome_obj.set_all_object_model_similar_props(j, self.matching_lists_count)
                    elif i == 3:
                        biome_obj.set_all_detail_model_similar_props(j, self.matching_lists_count)


    def process_recent_lists(self):
        # process the latest asset list added to each list of assets
        lists_to_process = [
        self.model.get_distant_obj_lists()[-1],
        self.model.get_landmark_lists()[-1],
        self.model.get_objects_lists()[-1],
        self.model.get_detail_obj_lists()[-1]
        ]

        for i, target_list in enumerate(lists_to_process):
            self.compare_and_update(target_list)
            
            if i == 0:
                self.model.set_distant_model_similar_props(self.matching_lists_count)
            elif i == 1:
                self.model.set_landmark_model_similar_props(self.matching_lists_count)
            elif i == 2:
                self.model.set_object_model_similar_props(self.matching_lists_count)
            elif i == 3:
                self.model.set_detail_model_similar_props(self.matching_lists_count)


    def process_distant_obj_list(self, biome):
        self.model = biome
        distant_obj_lists = self.model.get_distant_obj_lists()
        # check if distant objects in list, if not it means user using biome template with no distant objects props
        if distant_obj_lists:
            distant_obj_list = distant_obj_lists[-1]
            self.compare_and_update(distant_obj_list)
            self.model.set_distant_model_similar_props(self.matching_lists_count)

    def process_landmark_list(self, biome):
        self.model = biome
        landmark_lists = self.model.get_landmark_lists()
        if landmark_lists:
            landmark_list = landmark_lists[-1]
            self.compare_and_update(landmark_list)
            self.model.set_landmark_model_similar_props(self.matching_lists_count)

    def process_objects_list(self, biome):
        self.model = biome
        objects_lists = self.model.get_objects_lists()
        if objects_lists:
            objects_list = objects_lists[-1]
            self.compare_and_update(objects_list)
            self.model.set_object_model_similar_props(self.matching_lists_count)

    def process_detail_obj_list(self, biome):
        self.model = biome
        detail_obj_lists = self.model.get_detail_obj_lists()
        if detail_obj_lists:
            detail_obj_list = detail_obj_lists[-1]
            self.compare_and_update(detail_obj_list)
            self.model.set_detail_model_similar_props(self.matching_lists_count)


    # biome methods ----------------------------------------------------

    def c_create_default_biome(self):
        # initialize new model with dummy data
        self.counter += 1
        self.name = f"Biomes/Plumgen/Biome {self.counter}"
    
        self.model = PlumgenModelGen(self.name, self.dist_list, self.landm_list, self.objs_list, self.detail_list)
        # compare the 4 randomly selected "model paths" with those in csv and generate vanilla data for them
        self.process_recent_lists()
        self.biome_objs.append(self.model)
        
        return self.model
    

    def c_rename_biome(self, index, new_filename):
        self.index = index
        self.new_filename = new_filename
        self.biome_objs[self.index].set_filename(self.new_filename)
    

    def c_auto_rename_biomes(self):

        for biome_obj in self.biome_objs:
            
            auto_rename = biome_obj.get_filename() # get original name

            # split string using underscores, only take the first part
            #auto_rename = auto_rename.split('_')[0]
            
            distant_obj_lists = biome_obj.get_distant_obj_lists()
            landmark_lists = biome_obj.get_landmark_lists()
            objects_lists = biome_obj.get_objects_lists()
            detail_obj_lists = biome_obj.get_detail_obj_lists()

            all_lists_curr_biome = [distant_obj_lists, landmark_lists, objects_lists, detail_obj_lists]

            for i, lists in enumerate(all_lists_curr_biome):
                for j, target_list in enumerate(lists):
                    
                    # only rename based on objects, landmarks, and distantobjects model names
                    if i >= 0 and i <= 2:

                        prop_model = (target_list[0]).lower()

                        # dictionary to map keywords to suffixes
                        keyword_suffix_mapping = {
                            "toxic": "_Toxic",
                            "scorched": "_Scorched",
                            "radioactive": "_Radioactive",
                            "frozen": "_Frozen",
                            "barren": "_Barren",
                            "dead": "_Dead",
                            "weird": "_Weird",
                            "swamp": "_Swamp",
                            "lava": "_Lava",
                            "alien": "_Alien",
                            "alpine": "_Alpine",
                            "crystal": "_Weird",
                            "livingship": "_Livingship",
                            "nevada": "_Nevada",
                            "rainforest": "_Rainforest",
                            "huge": "_Huge"
                        }

                        # iterate over dictionary to check for each keyword
                        for keyword, suffix in keyword_suffix_mapping.items():
                            if keyword in prop_model:
                                auto_rename += suffix
                        
                        # check for other keywords for industrial & lush
                        if ("building" in prop_model or
                            "flag" in prop_model or
                            "construct" in prop_model or
                            "wreck" in prop_model and
                            "buildableparts" not in prop_model):
                            auto_rename += "_Industrial"
                        if "lush" in prop_model:
                            auto_rename += "_Lush"
                        elif ("tree" in prop_model and
                            "barren" not in prop_model and
                            "dead" not in prop_model and
                            "toxic" not in prop_model and
                            "underwater" not in prop_model and
                            "weird" not in prop_model and
                            "frozen" not in prop_model and
                            "radioactive" not in prop_model and
                            "scorched" not in prop_model and
                            "lava" not in prop_model and
                            "cave" not in prop_model and
                            "hugering" not in prop_model):
                            auto_rename += "_Lush"

            # split string using underscores
            parts = auto_rename.split('_')

            # keep track of unique substrings
            unique_parts = []
            for part in parts:
                if part not in unique_parts:
                    unique_parts.append(part)

            # join unique substrings back together with underscores
            auto_rename = '_'.join(unique_parts)

            biome_obj.set_filename(auto_rename)


    def c_reset_rename_biomes(self):
        for biome_obj in self.biome_objs:
            
            auto_rename = biome_obj.get_filename() # get original name

            # split string using underscores, only take the first part
            auto_rename = auto_rename.split('_')[0]

            biome_obj.set_filename(auto_rename)


    def c_delete_biome(self, index):
        self.index = index
        del self.biome_objs[self.index]

    def c_duplicate_biome(self, index):

        self.index = index
        biome = self.biome_objs[self.index]

        base_name = biome.filename + "_Copy"
        new_name = base_name
        
        #check if name already exists, if so, add a number
        while any(b.filename == new_name for b in self.biome_objs):
            self.copy_counter += 1
            new_name = f"{base_name}_{self.copy_counter}"

        # create deep copy of biome data, because the copied item is mutable
        distant_obj_lists_copy = copy.deepcopy(biome.get_distant_obj_lists())
        landmark_lists_copy = copy.deepcopy(biome.get_landmark_lists())
        objects_lists_copy = copy.deepcopy(biome.get_objects_lists())
        detail_obj_lists_copy = copy.deepcopy(biome.get_detail_obj_lists())

        # create a new instance with the deep-copied data
        self.model = PlumgenModelGen(new_name, self.dist_list, self.landm_list, self.objs_list, self.detail_list)
        
        self.model.set_distant_obj_lists_copy(distant_obj_lists_copy)
        self.model.set_landmark_lists_copy(landmark_lists_copy)
        self.model.set_objects_lists_copy(objects_lists_copy)
        self.model.set_detail_obj_lists_copy(detail_obj_lists_copy)
        
        self.biome_objs.append(self.model)

        return self.model
    

    def save_biome_preset_to_json(self, index):
        # save a biome in self.biome_objs
        
        if len(self.biome_objs) > 0:
            model = self.biome_objs[index]
            filename = model.get_filename()
            filename_base = os.path.basename(filename)

            filename_json = os.path.abspath(os.path.join(self.presets_path, f"{filename_base}.json"))
        
            # serialize the PlumgenModelGen object to JSON
            model_json = {
                "filename": model.get_filename(),
                "all_distant_obj_lists": model.get_distant_obj_lists(),
                "all_landmarks_lists": model.get_landmark_lists(),
                "all_objects_lists": model.get_objects_lists(),
                "all_detail_obj_lists": model.get_detail_obj_lists()
            }

            # Write the JSON data to a file
            with open(filename_json, 'w') as json_file:
                json.dump(model_json, json_file, indent=4)



    def import_model_from_json(self, filename_json):
        # read JSON data from file
        with open(filename_json, 'r') as json_file:
            model_json = json.load(json_file)

        name = model_json["filename"]

        # create new instance of PlumgenModelGen using data from JSON
        self.model = PlumgenModelGen(name, self.dist_list, self.landm_list, self.objs_list, self.detail_list)
        
        # set lists from JSON data
        self.model.set_distant_obj_lists_copy(model_json["all_distant_obj_lists"])
        self.model.set_landmark_lists_copy(model_json["all_landmarks_lists"])
        self.model.set_objects_lists_copy(model_json["all_objects_lists"])
        self.model.set_detail_obj_lists_copy(model_json["all_detail_obj_lists"])

        self.biome_objs.append(self.model)







    # import each exml biome objects files -------------------------------------------

    def before_next_process_directory(self, directory):
        # sort subfolders so that e.g. BIOMES2 is loaded after BIOMES1
        subfolders = sorted(next(os.walk(directory))[1], reverse=True)
        for subfolder in subfolders: # iterate over sorted subfolder names
            subfolder_path = os.path.join(directory, subfolder)
            for root, _, files in os.walk(subfolder_path):
                for filename in files:
                    if (filename.lower().endswith('.exml')
                    and 'biomefilename' not in filename.lower()
                    and 'biomelistperstartype' not in filename.lower()):
                        filepath = os.path.abspath(os.path.join(root, filename))
                        self.before_next_process_exml(filepath)


    def before_next_process_exml(self, filepath):
        exml_data = [[], [], [], []]  # DistantObjects, Landmarks, Objects, DetailObjects

        tree = ET.parse(filepath)
        root = tree.getroot()

        for category_idx, category in enumerate(["DistantObjects", "Landmarks", "Objects", "DetailObjects"]):
            category_list = exml_data[category_idx]

            for obj_spawn_data in root.findall(f".//Property[@name='{category}']/Property[@value='GcObjectSpawnData.xml']"):
                obj_data = []
                # use old var names
                for variable in ["Filename", "Placement", "RestrictionsMinHeight", "RestrictionsMaxHeight", "RestrictionsMinAngle",
                                "RestrictionsMaxAngle", "PositioningMinScale", "PositioningMaxScale", "PositioningMinScaleY", "PositioningMaxScaleY",
                                "PositioningPatchEdgeScaling", "PositioningMaxXZRotation", "DestroyedByPlayerVehicle", "DestroyedByTerrainEdit",
                                "ObjectCreaturesCanEat", "PlacementCoverage", "PlacementFlatDensity", "PlacementSlopeDensity",
                                "PlacementSlopeMultiplier"]:
                    
                    props = obj_spawn_data.findall(f".//Property[@name='{variable}']")

                    if props:
                        # make terrain edit true
                        if variable == "DestroyedByTerrainEdit":
                            prop_value == "TRUE"
                        # check if there is more than one occurrence
                        elif category == "DetailObjects" and len(props) > 2:
                            # grab the third occurrence, aka "ultra" detail objects settings
                            prop_value = props[2].get("value")
                        elif len(props) > 1:
                            # grab the second occurrence, aka "medium" settings
                            prop_value = props[1].get("value")
                        else:
                            prop_value = props[0].get("value")
                    elif variable == "DestroyedByTerrainEdit": # make terrain edit true (did not exist)
                        prop_value = "TRUE"
                    else:
                        prop_value = None

                    if variable == "DestroyedByPlayerVehicle" or variable == "ObjectCreaturesCanEat":
                        if prop_value is None:
                            prop_value = "TRUE" # foundation = did not have vehicles yet
                        else:
                            prop_value = prop_value.upper() # temp fix to match similar props
                    
                    obj_data.append(prop_value)

                obj_data.append(category)  # add DrawDistance
                obj_data.append([]) # add empty list for similar_items

                category_list.append(obj_data)

        # check if exml_data contains any data in 4 lists
        has_data = any(len(category) > 0 for category in exml_data)

        if has_data:
        
            # to merge BIOMES folders: regex pattern to match "BIOMES" possibly with numbers on either side
            biomes_pattern = r'(?<=\\|/)(\d*BIOMES\d*)(?=\\|/|$)'
            custombiomes_pattern = r'(?<=\\|/)(\d*CUSTOMBIOMES\d*)(?=\\|/|$)'
            biomes_matches = re.findall(biomes_pattern, filepath) # find any BIOMES matches in filepath
            custombiomes_matches = re.findall(custombiomes_pattern, filepath) # find any CUSTOMBIOMES matches in filepath

            if biomes_matches: # replace them with "BIOMES" only
                for match in biomes_matches:
                    filepath = filepath.replace(match, "BIOMES")
            elif custombiomes_matches: # replace them with "CUSTOMBIOMES" only
                for match in biomes_matches:
                    filepath = filepath.replace(match, "CUSTOMBIOMES")

            exml_data.append(filepath) # append filename - to name biome objects and keep track of directory structure
            self.exml_files.append(exml_data)



    def after_next_process_directory(self, directory):
        # sort subfolders so that e.g. BIOMES2 is loaded after BIOMES1
        subfolders = sorted(next(os.walk(directory))[1], reverse=True)
        for subfolder in subfolders: # iterate over sorted subfolder names
            subfolder_path = os.path.join(directory, subfolder)
            for root, _, files in os.walk(subfolder_path):
                for filename in files:
                    if (filename.lower().endswith('.exml')
                    and 'biomefilename' not in filename.lower()
                    and 'biomelistperstartype' not in filename.lower()):

                        filepath = os.path.abspath(os.path.join(root, filename))
                        self.after_next_process_exml(filepath)


    def after_next_process_exml(self, filepath):
        exml_data = [[], [], [], []]  # DistantObjects, Landmarks, Objects, DetailObjects

        tree = ET.parse(filepath)
        root = tree.getroot()

        for category_idx, category in enumerate(["DistantObjects", "Landmarks", "Objects", "DetailObjects"]):
            category_list = exml_data[category_idx]

            for obj_spawn_data in root.findall(f".//Property[@name='{category}']/Property[@value='GcObjectSpawnData.xml']"):
                obj_data = []

                for variable in ["Filename", "Placement", "MinHeight", "MaxHeight", "MinAngle", "MaxAngle",
                                "MinScale", "MaxScale", "MinScaleY", "MaxScaleY", "PatchEdgeScaling",
                                "MaxXZRotation", "DestroyedByPlayerShip", "DestroyedByTerrainEdit",
                                "CreaturesCanEat", "Coverage", "FlatDensity", "SlopeDensity", "SlopeMultiplier"]:
                    
                    props = obj_spawn_data.findall(f".//Property[@name='{variable}']")
                    
                    if props:
                        # check if there is more than one occurrence
                        if category == "DetailObjects" and len(props) > 2:
                            # grab the third occurrence, aka "ultra" detail objects settings
                            prop_value = props[2].get("value")
                        elif len(props) > 1:
                            # grab the second occurrence, aka "medium" settings
                            prop_value = props[1].get("value")
                        else:
                            prop_value = props[0].get("value")
                    else:
                        prop_value = None

                    if variable == "DestroyedByPlayerShip" or variable == "DestroyedByTerrainEdit" or variable == "CreaturesCanEat":
                        prop_value = prop_value.upper() # temp fix to match similar props
                    
                    obj_data.append(prop_value)

                obj_data.append(category)  # add DrawDistance
                obj_data.append([]) # add empty list for similar_items

                category_list.append(obj_data)

        # check if exml_data contains any data in 4 lists
        has_data = any(len(category) > 0 for category in exml_data)

        if has_data:
            # to merge BIOMES folders: regex pattern to match "BIOMES" possibly with numbers on either side
            biomes_pattern = r'(?<=\\|/)(\d*BIOMES\d*)(?=\\|/|$)'
            custombiomes_pattern = r'(?<=\\|/)(\d*CUSTOMBIOMES\d*)(?=\\|/|$)'
            biomes_matches = re.findall(biomes_pattern, filepath) # find any BIOMES matches in filepath
            custombiomes_matches = re.findall(custombiomes_pattern, filepath) # find any CUSTOMBIOMES matches in filepath

            if biomes_matches: # replace them with "BIOMES" only
                for match in biomes_matches:
                    filepath = filepath.replace(match, "BIOMES")
            elif custombiomes_matches: # replace them with "CUSTOMBIOMES" only
                for match in biomes_matches:
                    filepath = filepath.replace(match, "CUSTOMBIOMES")

            exml_data.append(filepath) # append filename - to name biome objects and keep track of directory structure
            self.exml_files.append(exml_data)


    # process each BIOMEFILENAMES.EXML file
    def process_bfn_files(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            xml_data = file.read()

            root = ET.fromstring(xml_data)

            # 1. extract BiomeFiles as a list of lists containing dictionaries
            biome_files_weights = []
            for biome_file in root.findall(".//Property[@name='BiomeFiles']/Property"):
                biome_list = []
                
                # identify the first nested list (e.g., Lush or Toxic)
                biome_name = biome_file.get("name")
                if biome_name is not None: # sometimes is None with pre-NEXT NMS
                    
                    for biome_option in biome_file.findall(".//Property[@value='GcBiomeFileListOption.xml']"):
                        biome_dict = {}

                        # XPath expression to target SubType property
                        sub_type = "Standard" # default value
                        sub_type_elem = biome_option.find("./Property/Property[@name='BiomeSubType']")
                        if sub_type_elem is not None:
                            sub_type = sub_type_elem.get("value")
                        
                        # extract information from each Property element
                        for prop in biome_option.findall("./Property"):
                            # look for keywords
                            if prop.get("name") == "Filename":
                                biome_dict[prop.get("value")] = None  # initialize with None, as Weight will be handled separately
                            elif prop.get("name") == "Weight":
                                weight = prop.get("value")
                                biome_dict[next(iter(biome_dict))] = f"{weight} {sub_type}"  # update the value associated with "Filename"
                        biome_list.append(biome_dict)

                    # PRE-NEXT, uses different names + no weights
                    if not biome_list:

                        for biome_option in biome_file.findall(".//Property[@value='NMSString0x80.xml']"):
                            biome_dict = {}
                            
                            # Extract information from each Property element
                            for prop in biome_option.findall("./Property"):
                                # check for the "Value" keyword
                                # FOR PRE-NEXT
                                if prop.get("name") == "Value":
                                    filename = prop.get("value")
                                    biome_dict[filename] = "1 Standard"  # initialize weight with 1 and subbiome Standard

                            biome_list.append(biome_dict)

                    biome_files_weights.append({biome_name: biome_list})

            #print(biome_files)

            # 2. extract TileTypes as a dictionary
            tile_types = {}

            for external_object_list in root.findall(".//Property[@name='CommonExternalObjectLists']/Property[@value='GcExternalObjectListOptions.xml']"):
                probability = external_object_list.find("./Property[@name='Probability']").get("value")
                
                tile_type_name = external_object_list.find("./Property[@name='TileType']/Property[@name='TileType']").get("value")

                # check if the key already exists in the dictionary
                original_tile_type_name = tile_type_name
                count = 2
                
                for item in tile_types:
                    item_parts = item.split() # split each item in biome_tile_types by space
                    first_part = item_parts[0] # get first part (before the space)
                    if tile_type_name == first_part: # compare tile_type_name with the first part
                        tile_type_name = f"{original_tile_type_name}{count}"
                        count += 1

                tile_type_name = f"{tile_type_name} {probability}" # append probability
                ##

                # 2. identify the first nested list (e.g., Cave or Underwater)
                tile_type_values = []
                
                for option in external_object_list.findall(".//Property[@value='NMSString0x80.xml']"):
                    value = option.find("./Property[@name='Value']").get("value")
                    tile_type_values.append(value)

                tile_types[tile_type_name] = tile_type_values

            
            # 3 extract biomes listed under the "ValidStartPlanetBiome" property
            valid_start_biomes = []
            valid_start_property = root.find(".//Property[@name='ValidStartPlanetBiome']")
            if valid_start_property is not None:
                for biome_property in valid_start_property.findall(".//Property[@value='GcBiomeType.xml']"):
                    start_biome_value = biome_property.find("./Property[@name='Biome']").get("value")
                    valid_start_biomes.append(start_biome_value)

            #print(tile_types)

        return biome_files_weights, tile_types, valid_start_biomes


    # 4. **each** biome:
    def process_each_biome_file(self, directory):
        all_biome_tile_types = []

        # iterate over all files and directories in the given directory
        # sort subfolders so that e.g. BIOMES2 is loaded after BIOMES1
        subfolders = sorted(next(os.walk(directory))[1], reverse=True)
        for subfolder in subfolders: # iterate over sorted subfolder names
            subfolder_path = os.path.join(directory, subfolder)
            for root, _, files in os.walk(subfolder_path):
                for filename in files:

                    # check if the file is an EXML file
                    #print(f"Processing file: {filename}")
                    if (filename.lower().endswith('.exml') 
                    #and 'biome' in filename.lower() 
                    and 'biomefilename' not in filename.lower()
                    and 'biomelistperstartype' not in filename.lower()):
                        
                        # construct full path to the EXML file
                        exml_path = os.path.abspath(os.path.join(root, filename))
                        
                        # read content of EXML file
                        with open(exml_path, 'r', encoding='utf-8') as file:
                            xml_data_biomes = file.read()

                        root_biomes = ET.fromstring(xml_data_biomes)  # parse XML data

                        biome_tile_types = {} # dict stores tile types for this biome

                        # iterate over each ExternalObjectLists Property
                        for external_object_lists in root_biomes.findall(".//Property[@name='ExternalObjectLists']"):
                            # iterate over each GcExternalObjectListOptions Property
                            for external_object_list in external_object_lists.findall(".//Property[@value='GcExternalObjectListOptions.xml']"):
                                # extract values
                                probability = external_object_list.find("./Property[@name='Probability']").get("value")
                                
                                tile_type_name = external_object_list.find("./Property[@name='TileType']/Property[@name='TileType']").get("value")

                                # check if the key already exists in the dictionary
                                original_tile_type_name = tile_type_name
                                count = 2
                                
                                for item in biome_tile_types:
                                    item_parts = item.split() # split each item in biome_tile_types by space
                                    first_part = item_parts[0] # get first part (before the space)
                                    if tile_type_name == first_part: # compare tile_type_name with the first part
                                        tile_type_name = f"{original_tile_type_name}{count}"
                                        count += 1

                                tile_type_name = f"{tile_type_name} {probability}" # append probability

                                # extract Options for the TileType
                                tile_type_values = []
                                for option in external_object_list.findall(".//Property[@value='NMSString0x80.xml']"):
                                    value = option.find("./Property[@name='Value']").get("value")
                                    tile_type_values.append(value)

                                # Store the TileType and its Options in the dictionary
                                biome_tile_types[tile_type_name] = tile_type_values
                        

                        # don't append if empty
                        if len(biome_tile_types) > 0:

                            existing_biome_types = [os.path.splitext(os.path.basename(d["Filename"]))[0] for d in all_biome_tile_types]


                            # to merge BIOMES folders: regex pattern to match "BIOMES" possibly with numbers on either side
                            biomes_pattern = r'(?<=\\|/)(\d*BIOMES\d*)(?=\\|/|$)'
                            custombiomes_pattern = r'(?<=\\|/)(\d*CUSTOMBIOMES\d*)(?=\\|/|$)'
                            biomes_matches = re.findall(biomes_pattern, exml_path) # find any BIOMES matches in filepath
                            custombiomes_matches = re.findall(custombiomes_pattern, exml_path) # find any CUSTOMBIOMES matches in filepath

                            if biomes_matches: # replace them with "BIOMES" only
                                for match in biomes_matches:
                                    exml_path = exml_path.replace(match, "BIOMES")
                            elif custombiomes_matches: # replace them with "CUSTOMBIOMES" only
                                for match in biomes_matches:
                                    exml_path = exml_path.replace(match, "CUSTOMBIOMES")


                            biome_tile_types["Filename"] = exml_path  # add filepath as the last item in list

                            temp_name = os.path.splitext(os.path.basename(exml_path))[0]

                            # check if truncated biome file already exists in all_biome_tile_types, if so merge contents
                            if temp_name in existing_biome_types:
                                index = existing_biome_types.index(temp_name)

                                # iterate over each key in biome_tile_types
                                for key, value in biome_tile_types.items():
                                    # check if key exists in all_biome_tile_types[index]
                                    if key in all_biome_tile_types[index]:
                                        # if it exists, append values from biome_tile_types to the existing list

                                        #print(f"Index: {index}, Key: {key}, Value: {value}")
                                        #print(f"Type of Value: {type(value)}")

                                        if not isinstance(value, str): # make sure it's a list, not the filename string
                                            all_biome_tile_types[index][key].extend(value)

                                    else:
                                        # if doesn't exist, create a new key-value pair in all_biome_tile_types[index]
                                        all_biome_tile_types[index][key] = value

                            else:
                                all_biome_tile_types.append(biome_tile_types)
                            

        return all_biome_tile_types



    def c_import_exml_biomes(self, after_next_update, use_default_bfn_dir=False):
        # check whether to use default directory (import default bfn.mbin)
        if use_default_bfn_dir:
            exml_directory = self.default_bfn_folder_dir
        else:
            exml_directory = self.biome_exmls_folder_dir


        # clear all of these-- otherwise, won't detect duplicates
        self.exml_files = []
        self.bfn_all_biome_files_weights = []
        self.bfn_all_valid_start_planets = []
        self.bfn_all_tile_types = {}
        self.all_biome_tile_types = []
        self.biome_objs = []


        if after_next_update:
            self.after_next_process_directory(exml_directory)
        else:
            self.before_next_process_directory(exml_directory)

        # access processed biome objects data:
        for exml_file in self.exml_files:
            
            distant_objects, landmarks, objects, detail_objects, name = exml_file

            self.name = name

            filepath_parts = self.name.split(self.subfolder)
            if len(filepath_parts) > 1:
                self.name = filepath_parts[-1].replace('.exml', '').replace('.EXML', '').replace('\\', '/')
                self.name = '/'.join([word.title() for word in self.name.split('/')])

                # remove consecutive slashes or backslashes
                self.name = re.sub(r'[\\/]+', '/', self.name)

                # remove the first slash if present
                if self.name.startswith('/'):
                    self.name = self.name[1:]

            self.model = PlumgenModelGen(self.name, self.dist_list, self.landm_list, self.objs_list, self.detail_list)

            self.model.set_distant_obj_lists(distant_objects)
            self.model.set_landmark_lists(landmarks)
            self.model.set_objects_lists(objects)
            self.model.set_detail_obj_lists(detail_objects)

            self.biome_objs.append(self.model)

        # process each biome file name files & **each** biome file ---------------------------

        # 1-3 iterate through the directory and its subdirectories
        #for root, dirs, files in os.walk(exml_directory):
        #    for f_name in files:

        # sort subfolders so that e.g. BIOMES2 is loaded after BIOMES1
        subfolders = sorted(next(os.walk(exml_directory))[1], reverse=True)
        for subfolder in subfolders: # iterate over sorted subfolder names
            subfolder_path = os.path.join(exml_directory, subfolder)
            for root, _, files in os.walk(subfolder_path):
                for f_name in files:

                    
                    if f_name.lower().endswith('.exml') and 'biomefilename' in f_name.lower():
                        path_to_bfn = os.path.abspath(os.path.join(root, f_name))
                        # process current BIOMEFILENAMES.EXML file and collect results
                        biome_files_wts_bfn, tile_types_bfn, valid_start_biomes_bfn = self.process_bfn_files(path_to_bfn)
                        
                        # update self.bfn_all_biome_files_weights
                        for item in biome_files_wts_bfn:
                            key = next(iter(item))

                            # check if the key exists in any dictionaries within the list
                            key_exists = any(key in d for d in self.bfn_all_biome_files_weights)

                            if key_exists:
                                # replace values for matching keys
                                for d in self.bfn_all_biome_files_weights:
                                    if key in d:
                                        # compare values and update if necessary
                                        existing_values = d[key]
                                        new_values = item[key]
                                        for new_value in new_values:
                                            new_path = list(new_value.keys())[0]
                                            new_weight = list(new_value.values())[0]
                                            new_weight = new_weight.split()[0] # split on white space
                                            for existing_value in existing_values:
                                                existing_path = list(existing_value.keys())[0]
                                                existing_weight = list(existing_value.values())[0]
                                                if new_path == existing_path:
                                                    # find index of existing_value in existing_values
                                                    index = existing_values.index(existing_value)
                                                    # extract string part from existing value
                                                    existing_string = existing_weight.split()[1]
                                                    # construct new value with updated weight
                                                    existing_values[index] = {new_path: f"{new_weight} {existing_string}"}
                                                    
                                                    break
                                            else:
                                                existing_values.append(new_value)
                            else:
                                # append new key and values
                                self.bfn_all_biome_files_weights.append({key: item[key]})

                        # update self.bfn_all_tile_types
                        for key, value in tile_types_bfn.items():
                            if key in self.bfn_all_tile_types:
                                # extend existing values
                                self.bfn_all_tile_types[key].extend(value)
                            else:
                                # append new key and values
                                #if not self.bfn_all_tile_types:
                                self.bfn_all_tile_types[key] = value #should be dictionary?
                                #else:
                                #    self.bfn_all_tile_types[0][key] = value

                        # update self.bfn_all_valid_start_planets
                        for item in valid_start_biomes_bfn:
                            if item not in self.bfn_all_valid_start_planets:
                                # append new item
                                #if not self.bfn_all_valid_start_planets:
                                self.bfn_all_valid_start_planets.append(item)
                                #else:
                                #    self.bfn_all_valid_start_planets[0].append(item)




        # 4 Process all EXML files in the specified directory
        self.all_biome_tile_types = self.process_each_biome_file(exml_directory)

        # print result
        #for idx, biome_tile_types in enumerate(self.all_biome_tile_types, start=1):
        #    print(f"Biome {idx} tile types:")
        #    print(biome_tile_types)
        #    print()

        #print("test")








    # make biome template from exmls -------------------------------------------

    # after NEXT -------------------------------------------
    def process_after_next_file(self, file_path, csv_writer):
        tree = ET.parse(file_path)
        root = tree.getroot()

        # define the keywords to search for
        keywords = ["DistantObjects", "Landmarks", "Objects", "DetailObjects"]

        for keyword in keywords:
            # find the corresponding section
            if keyword == "Objects":
                section = next((prop for prop in root.iter('Property') if prop.get('name') == 'Objects' and 'value' not in prop.attrib), None)
            else:
                section = root.find(f'.//Property[@name="{keyword}"]')

            # if the section exists, iterate through Filename elements
            if section is not None:
                # iterate through 'GcObjectSpawnData.xml' elements under keywords
                object_spawn_data_elements = section.findall('.//Property[@value="GcObjectSpawnData.xml"]')
                for object_spawn_data in object_spawn_data_elements:
                    row = {"Filename": None}

                    # extract variables under GcObjectSpawnData.xml
                    variables = ["Filename", "Placement", "MinHeight", "MaxHeight", "MinAngle", "MaxAngle",
                                "MinScale", "MaxScale", "MinScaleY", "MaxScaleY", "PatchEdgeScaling",
                                "MaxXZRotation", "DestroyedByPlayerShip", "DestroyedByTerrainEdit",
                                "CreaturesCanEat", "Coverage", "FlatDensity", "SlopeDensity", "SlopeMultiplier"]
                    
                    for variable in variables:
                        variable_elements = object_spawn_data.findall(f'.//Property[@name="{variable}"]')
                        if variable_elements:
                            # check if there is more than one occurrence
                            if keyword == "DetailObjects" and len(variable_elements) > 2:
                                # grab the third occurrence, aka "ultra" detail objects coverage & flatdensity settings
                                variable_value = variable_elements[2].get("value")
                            elif len(variable_elements) > 1:
                                # grab the second occurrence, aka "medium" coverage & flatdensity settings
                                variable_value = variable_elements[1].get("value")
                            else:
                                variable_value = variable_elements[0].get("value")
                            row[variable] = variable_value
                    row["DrawDistance"] = keyword

                    csv_writer.writerow(row)



    def after_next_make_biome_template(self, directory_path, output_csv_path):
        # open CSV file for writing
        with open(output_csv_path, 'w', newline='') as csv_file:
            fieldnames = ["Filename", "Placement", "MinHeight", "MaxHeight", "MinAngle", "MaxAngle",
                        "MinScale", "MaxScale", "MinScaleY", "MaxScaleY", "PatchEdgeScaling",
                        "MaxXZRotation", "DestroyedByPlayerShip", "DestroyedByTerrainEdit",
                        "CreaturesCanEat", "Coverage", "FlatDensity", "SlopeDensity", "SlopeMultiplier", "DrawDistance"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # write the header row
            csv_writer.writeheader()

            # oterate through each file in the directory
            #for root, dirs, files in os.walk(directory_path):
            #    for filename in files:

            # sort subfolders so that e.g. BIOMES2 is loaded after BIOMES1
            subfolders = sorted(next(os.walk(directory_path))[1], reverse=True)
            for subfolder in subfolders: # iterate over sorted subfolder names
                subfolder_path = os.path.join(directory_path, subfolder)
                for root, _, files in os.walk(subfolder_path):
                    for filename in files:

                        if filename.lower().endswith(".exml"):
                            file_path = os.path.abspath(os.path.join(root, filename))

                            # extract portion of the file path starting from "METADATA"
                            #relative_path = "METADATA\\SIMULATION\\SOLARSYSTEM\\BIOMES" + file_path.split("BIOMES")[-1]

                            # Process the file and write to CSV
                            self.process_after_next_file(file_path, csv_writer)










    # before NEXT - part 1A --------------------------------
    def process_before_NEXT_file(self, file_path, csv_writer):
        tree = ET.parse(file_path)
        root = tree.getroot()

        # define the keywords to search for
        keywords = ["DistantObjects", "Landmarks", "Objects", "DetailObjects"]

        for keyword in keywords:
            # find the corresponding section
            if keyword == "Objects":
                section = next((prop for prop in root.iter('Property') if prop.get('name') == 'Objects' and 'value' not in prop.attrib), None)
            else:
                section = root.find(f'.//Property[@name="{keyword}"]')

            # if the section exists, iterate through Filename elements
            if section is not None:
                # iterate through 'GcObjectSpawnData.xml' elements under keywords
                object_spawn_data_elements = section.findall('.//Property[@value="GcObjectSpawnData.xml"]')
                for object_spawn_data in object_spawn_data_elements:
                    row = {"Filename": None}

                    # extract specific variables under GcObjectSpawnData.xml
                    variables = ["Filename", "Placement", "PlacementCoverage", "PlacementFlatDensity", "PlacementSlopeDensity", "PlacementSlopeMultiplier", "RestrictionsMinHeight", "RestrictionsMaxHeight", 
                                "RestrictionsMinAngle", "RestrictionsMaxAngle","PositioningMinScale", "PositioningMaxScale", "PositioningMinScaleY", 
                                "PositioningMaxScaleY", "PositioningPatchEdgeScaling","PositioningMaxXZRotation", 
                                "DestroyedByPlayerVehicle", "ObjectCreaturesCanEat" ]
                    
                    for variable in variables:
                        variable_elements = object_spawn_data.findall(f'.//Property[@name="{variable}"]')
                        if variable_elements:
                            # check if there is more than one occurrence
                            if keyword == "DetailObjects" and len(variable_elements) > 2:
                                # grab the third occurrence, aka "ultra" detail objects coverage & flatdensity settings
                                variable_value = variable_elements[2].get("value")
                            elif len(variable_elements) > 1:
                                # grab the second occurrence, aka "medium" coverage & flatdensity settings
                                variable_value = variable_elements[1].get("value")
                            else:
                                variable_value = variable_elements[0].get("value")
                            row[variable] = variable_value
                    row["DestroyedByTerrainEdit"] = "TRUE"
                    row["DrawDistance"] = keyword

                    csv_writer.writerow(row)


    # before NEXT - part 1B --------------------------------
    def before_next_make_biome_template(self, directory_path, output_csv_path):
        # open the CSV file for writing
        with open(output_csv_path, 'w', newline='') as csv_file:
            fieldnames = ["Filename", "Placement", "PlacementCoverage", "PlacementFlatDensity", "PlacementSlopeDensity", "PlacementSlopeMultiplier", "RestrictionsMinHeight", "RestrictionsMaxHeight", 
                                "RestrictionsMinAngle", "RestrictionsMaxAngle","PositioningMinScale", "PositioningMaxScale", "PositioningMinScaleY", 
                                "PositioningMaxScaleY", "PositioningPatchEdgeScaling","PositioningMaxXZRotation", 
                                "DestroyedByPlayerVehicle", "ObjectCreaturesCanEat", "DestroyedByTerrainEdit", "DrawDistance" ]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # write header row
            csv_writer.writeheader()

            # sort subfolders so that e.g. BIOMES2 is loaded after BIOMES1
            subfolders = sorted(next(os.walk(directory_path))[1], reverse=True)
            for subfolder in subfolders: # iterate over sorted subfolder names
                subfolder_path = os.path.join(directory_path, subfolder)
                for root, _, files in os.walk(subfolder_path):
                    for filename in files:

                        if filename.lower().endswith(".exml"):
                            file_path = os.path.abspath(os.path.join(root, filename))

                            # process the file and write to CSV
                            self.process_before_NEXT_file(file_path, csv_writer)



    # part 2 --------------------------------
    def rename_and_rearrange_before_next_columns(self, input_csv_path, output_csv_path):
        with open(input_csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            # new column names
            new_column_names = ["Filename", "Placement", "MinHeight", "MaxHeight", "MinAngle", "MaxAngle",
                                "MinScale", "MaxScale", "MinScaleY", "MaxScaleY", "PatchEdgeScaling",
                                "MaxXZRotation", "DestroyedByPlayerShip", "DestroyedByTerrainEdit",
                                "CreaturesCanEat", "Coverage", "FlatDensity", "SlopeDensity", "SlopeMultiplier", "DrawDistance"]

            with open(output_csv_path, 'w', newline='') as new_csv_file:
                writer = csv.DictWriter(new_csv_file, fieldnames=new_column_names)
                writer.writeheader()

                for row in reader:
                    # map old column names to new column names
                    new_row = {
                        "Filename": row["Filename"],
                        "Placement": row["Placement"],
                        "MinHeight": row["RestrictionsMinHeight"],
                        "MaxHeight": row["RestrictionsMaxHeight"],
                        "MinAngle": row["RestrictionsMinAngle"],
                        "MaxAngle": row["RestrictionsMaxAngle"],
                        "MinScale": row["PositioningMinScale"],
                        "MaxScale": row["PositioningMaxScale"],
                        "MinScaleY": row["PositioningMinScaleY"],
                        "MaxScaleY": row["PositioningMaxScaleY"],
                        "PatchEdgeScaling": row["PositioningPatchEdgeScaling"],
                        "MaxXZRotation": row["PositioningMaxXZRotation"],
                        "DestroyedByPlayerShip": row["DestroyedByPlayerVehicle"],
                        "DestroyedByTerrainEdit": row["DestroyedByTerrainEdit"],
                        "CreaturesCanEat": row["ObjectCreaturesCanEat"],
                        "Coverage": row["PlacementCoverage"],
                        "FlatDensity": row["PlacementFlatDensity"],
                        "SlopeDensity": row["PlacementSlopeDensity"],
                        "SlopeMultiplier": row["PlacementSlopeMultiplier"],
                        "DrawDistance": row["DrawDistance"]
                    }

                    writer.writerow(new_row)



    def c_make_template_from_exml(self, after_next_update, template_filename):
        output_csv_path =  os.path.abspath(os.path.join(self.resources_path, template_filename))
        
        if after_next_update:
            # search and write to CSV
            self.after_next_make_biome_template(self.biome_exmls_folder_dir, output_csv_path)
            #print(f"Results saved to: {output_csv_path}")

        else:
            output_csv_path_part1 = os.path.abspath(os.path.join(self.resources_path, "_DELETE_THIS Pre-NEXT Biome Template-unsorted.csv"))

            # search and write to CSV
            self.before_next_make_biome_template(self.biome_exmls_folder_dir, output_csv_path_part1)
            #print(f"Results saved to: {output_csv_path_part1}")

            # before NEXT - part 2 --------------------------------------
            self.rename_and_rearrange_before_next_columns(output_csv_path_part1, output_csv_path)
            #print(f"Results saved to: {output_csv_path}")
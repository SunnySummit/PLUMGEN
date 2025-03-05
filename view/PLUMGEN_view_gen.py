'''
File: PLUMGEN_view_sett.py
'''

import os
import tkinter as tk
from tkinter import ttk, messagebox, Scale, Label, Button, IntVar, Listbox, Entry, DoubleVar, DoubleVar, simpledialog
import re
import numbers
import copy
import json
import webbrowser
import threading
import logging
import sys
import ctypes
from view.PLUMGEN_view_gen_bulk import PlumgenViewGenBulk
from view.PLUMGEN_view_gen_export import PlumgenViewGenExport
from view.PLUMGEN_view_menu import MenuBar
from Resources.PLUMGEN_updater import PlumgenUpdater



class PlumgenViewGen:
    #def __init__(self, parent):
    def __init__(self, root, controller, languages, lang):

        self.logger = logging.getLogger(__name__)  #set up logging

        try:
                
            self.root = root # store the root window reference
            self.controller = controller # configure window
            self.langs = languages # languages
            self.lan = lang

            # frame 1
            self.framePanel = tk.Frame(self.root)
            self.framePanel.grid()

            self.root.withdraw()
            self.window = tk.Toplevel(self.root)
            
            # set DPI awareness, handle scaling better
            try: ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except: pass  # DPI awareness not available

            self.window.geometry("1670x845")

            # check if the code is frozen (compiled to exe) or running as a script
            if getattr(sys, 'frozen', False):
                # if frozen (and running as exe), use this path
                self.current_directory = os.path.dirname(sys.executable)
                self.parent_path = tk.StringVar(value=os.path.dirname(os.path.dirname(sys.executable)))
                #exe_dir = sys._MEIPASS
                self.icon_path = os.path.join(self.current_directory, 'images', 'plum_icon_cc0.ico')
                self.image_path = os.path.join(self.current_directory, 'images', 'splash.png')
            else:
                # if running as script, use this path
                # one level up from the current script's directory
                self.parent_path = tk.StringVar(value=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                self.icon_path = os.path.join(self.parent_path.get(), 'images', 'plum_icon_cc0.ico')
                self.image_path = os.path.join(self.parent_path.get(), 'images', 'splash.png')

            self.window.attributes("-alpha", 0.0) # remove flash
            self.window.update() # explicitly update window
            #self.root.iconbitmap(os.path.join(self.parent_path.get(), 'images', 'plum_icon_cc0.ico'))

            self.window.iconbitmap(self.icon_path)

            #self.display_splash()

            self.style = ttk.Style(self.window)
            self.style.theme_use('clam')

            # initialize variables with default values
            self.biome_index = None
            self.distant_index = None
            self.landmark_index = None
            self.obj_index = None
            self.detail_index = None
            self.prop_draw_type = None
            self.prop_attribute_index = None
            self.float_var = DoubleVar()
            self.float_var.set(0.0)
            self.int_var = tk.IntVar()
            self.int_var.set(0)
            self.true_false  = tk.StringVar(value='TRUE')
            self.prop_distant = None
            self.prop_landmark = None
            self.prop_object = None
            self.prop_detail = None
            self.background_c = '#555555'
            self.highlight_c = '#0078d7'
            self.white_c = '#FFFFFF'
            self.placem_val_at_index = None
            self.model_val_at_index = None
            self.open_export_window_and_wait = False
            self.checked_mbc_update_already = False
            # get default model filepaths lists on start
            self.dist_model_list = self.controller.get_dist_list()
            self.landm_model_list = self.controller.get_landm_list()
            self.objs_model_list = self.controller.get_objs_list()
            self.detail_model_list = self.controller.get_detail_list()
            self.date_of_import_folder = None

            self.style_parent()
            self.create_widgets()
            self.layout_widgets()

            self.toggle_tooltip()
            self.populate_csv_combo()

            #self.window.grab_set()

            self.buttons = [
                self.biome_add_button, self.biome_delete_button,
                self.distant_objects_add_button, self.distant_objects_delete_button,
                self.landmark_add_button, self.landmark_delete_button,
                self.objects_add_button, self.objects_delete_button,
                self.detail_objects_add_button, self.detail_objects_delete_button,
                self.duplicate_biome_button, self.duplicate_prop_button,
                self.increment_prop_changes_button, self.decrement_prop_changes_button,
                self.export_to_xml_button, self.save_rename_biome_button,
                self.import_exml_button
            ]

            self.attribute_labels = [
						"Type: ",
                        "Filename: ",
						"Placement: ",
                        "MinHeight: ",
						"MaxHeight: ",
                        "MinAngle: ",
						"MaxAngle: ",
                        "MinScale: ",
						"MaxScale: ",
                        "MinScaleY: ",
						"MaxScaleY: ",
                        "PatchEdgeScaling: ",
						"MaxXZRotation: ",
                        "MaxYRotation: ",
                        "MaxRaise: ",
                        "MaxLower: ",
                        "DestroyedByPlayerShip: ",
						"DestroyedByTerrainEdit: ",
                        "IsFloatingIsland: ",
                        "CreaturesCanEat: ",
						"Coverage: ",
                        "FlatDensity: ",
						"SlopeDensity: ",
                        "SlopeMultiplier: ",
						"DrawDistance: ",
                        "TotalCountInTemplate: "
						]
            
            self.attribute_labels_edited = [label[:-2] for label in self.attribute_labels]

            self.replace_lb_with_template_data_cb.config(state=tk.DISABLED) # disable checkbox

            # populate model and placement listboxes
            self.def_distance_obj_list = self.controller.get_dist_list()
            self.def_landm_list = self.controller.get_landm_list()
            self.def_objs_list = self.controller.get_objs_list()
            self.def_detail_list= self.controller.get_detail_list()

            self.placement_list = self.controller.get_placem_defaults()

            for placem in self.placement_list:
                self.placement_lb.insert(tk.END, placem)

            #self.splash.after(3000, self.splash.withdraw)
            
            # set closing event handler for the Toplevel window
            self.window.protocol("WM_DELETE_WINDOW", self.on_close)

            self.window.after(300, lambda: self.window.attributes("-alpha", 1.0))


        except Exception as e:
            self.logger.exception(f"{self.langs[self.lan]["messagebox"]["error"]}{e}") # log the exception
            self.show_error_message(f"{self.langs[self.lan]["messagebox"]["error_desc_short"]}{e}")

    def show_error_message(self, message, max_length=200):
        if len(message) > max_length:
            truncated_message = message[:max_length] + "..."
        else:
            truncated_message = message
        messagebox.showerror(self.langs[self.lan]["de_select_all"]["Error"], f"{truncated_message}\n\n{self.langs[self.lan]["messagebox"]["error_desc_long"]}", parent=self.window)


    def display_splash(self):
        # splash screen
        self.splash = tk.Toplevel(self.root)
        self.splash.title("Loading...")
        self.splash.geometry(f"400x225") # set size
        self.splash.configure(bg="#ffffff")
        self.splash.configure(borderwidth=1)

        # retrieve parent window's position & size
        parent_width = self.window.winfo_width()
        parent_height = self.window.winfo_height()
        parent_x = self.window.winfo_rootx()
        parent_y = self.window.winfo_rooty()
        # Calculate x and y offsets to position the splash screen relative to the parent window
        splash_width = 400
        splash_height = 225
        splash_x = parent_x + (parent_width - splash_width) // 2
        splash_y = parent_y + (parent_height - splash_height) // 2

        self.splash.geometry(f"+{splash_x}+{splash_y}")  # set location

        self.splash.overrideredirect(True) # remove window decorations

        # load image
        image = tk.PhotoImage(file=self.image_path)

        # display image using a label
        label = tk.Label(self.splash, image=image)
        label.image = image  # keep reference to avoid garbage collection
        label.grid(row=0, column=0, sticky="nsew")

        # grid weights
        self.splash.grid_rowconfigure(0, weight=1)
        self.splash.grid_columnconfigure(0, weight=1)

        #self.splash.grab_set() # prevent from going behind main window
        #self.splash.lift()
        self.splash.attributes("-topmost", True)
        self.splash.update() # explicitly update loading screen


    def customize_style(self):
        hover_bg_color = '#555555'
        hover_fg_color = '#FFFFFF'
        hover_bg_prpl_color = '#0078d7'
        hover_fg_prpl_color = '#2b1c4a'
        red_bg_color = '#473d5c'
        
        self.style.configure('.', background='#333333', foreground=self.white_c, font=('TkDefaultFont', 10))

        self.style.configure('TitleLabel.TLabel', background='#333333', foreground=self.white_c, font=('TkDefaultFont', 14, 'bold'))
        self.style.configure('Title2Label.TLabel', background='#333333', foreground=self.white_c, font=('TkDefaultFont', 12, 'bold'))
        self.style.configure('Title3Label.TLabel', background='#333333', foreground=self.white_c, font=('TkDefaultFont', 12))
        self.style.configure('TLabel', background='#333333', foreground=self.white_c, font=('TkDefaultFont', 10))
        self.style.configure('TButton', background='#666666', foreground=self.white_c, font=('TkDefaultFont', 10))
        self.style.configure('Start.TButton', background=hover_bg_prpl_color, foreground=self.white_c, font=('TkDefaultFont', 10))
        self.style.configure('Gen.TButton', background='#333333', foreground=self.white_c, font=('TkDefaultFont', 10))
        self.style.configure('Create.TButton', background='#008040', foreground=self.white_c, font=('TkDefaultFont', 10)) # make New biome button green
        self.style.configure('Delete.TButton', background=red_bg_color, foreground=self.white_c, font=('TkDefaultFont', 10))
        self.style.configure('TEntry', fieldbackground='#444444', foreground=self.white_c, font=('TkDefaultFont', 10))
        self.style.configure('TText', background='#444444', foreground=self.white_c, font=('TkDefaultFont', 10))
        self.style.configure('TCombobox', background='#444444', foreground=self.white_c)
        self.style.configure("Vertical.TScrollbar", background=self.white_c, troughcolor=self.background_c, activebackground=self.background_c, highlightbackground=self.background_c)
        self.style.configure("Horizontal.TScrollbar", background=self.white_c, troughcolor=self.background_c, activebackground=self.background_c, highlightbackground=self.background_c)

        self.style.map('TCombobox', fieldbackground=[('readonly','!focus','#444444')])
        self.style.map('TCombobox', selectbackground=[('readonly','!focus',self.background_c)])
        self.style.map('TCombobox', selectforeground=[('readonly','!focus',self.white_c)])  
        self.style.map('TCombobox', arrowcolor=[('readonly','!focus',self.white_c)])

        self.style.map('TButton',
                  background=[('active', self.background_c), ('pressed', self.background_c)],
                  foreground=[('active', self.white_c), ('pressed', self.white_c)])
        
        self.style.map('Start.TButton',
              background=[('disabled', 'gray30'), ('active', hover_fg_prpl_color), ('pressed', hover_fg_prpl_color)],
              foreground=[('disabled', hover_fg_prpl_color), ('active', self.white_c), ('pressed', self.white_c)])
        
        self.style.map('Gen.TButton',
              background=[('disabled', 'gray30'), ('active', '#241c30'), ('pressed', '#333333')],
              foreground=[('disabled', hover_fg_prpl_color), ('active', self.white_c), ('pressed', self.white_c)])
        
        self.style.map('Create.TButton', # make New biome button green
              background=[('disabled', 'gray30'), ('active', '#004d26'), ('pressed', '#008040')],
              foreground=[('disabled', hover_fg_prpl_color), ('active', self.white_c), ('pressed', self.white_c)])
        
        self.style.map('Delete.TButton',
              background=[('disabled', 'gray30'), ('active', '#8a4242'), ('pressed', red_bg_color)],
              foreground=[('disabled', hover_fg_prpl_color), ('active', self.white_c), ('pressed', self.white_c)])
        
        self.style.map('TCombobox', 
        fieldbackground=[('!disabled', '#333333')])

        # checkbox hover colors
        self.style.map('TCheckbutton',
              background=[('active', hover_bg_color)])
        
        # radio button hover colors
        self.style.map('TRadiobutton',
                  background=[('active', hover_bg_color)],
                  foreground=[('active', hover_fg_color)])
        



    def style_parent(self):
        self.customize_style()
        self.window.configure(bg='#333333')
        
    def create_widgets(self):
        # modified menubar
        self.mb = MenuBar(self.window, bg='#473d5c', fg='#FFFFFF', overbackground='#2b1c4a')
        self.mb.grid(row=0, column=0, columnspan=10, sticky="ew")

        self.filemenu = tk.Menu(self.mb)
        #filemenu.add_command(label='Import EXML Data/Merge Biome Lists', command=self.import_exml_biomes)
        self.filemenu.add_command(label=self.langs[self.lan]["filemenu_view_gen"]["make_template"], command=self.make_template_from_exml)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=self.langs[self.lan]["filemenu_view_gen"]["auto_rename"], command=self.auto_rename_biomes)
        self.filemenu.add_command(label=self.langs[self.lan]["filemenu_view_gen"]["reset_auto_rename"], command=self.reset_rename_biomes)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Bulk Import & Update", command=self.bulk_import_update)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=self.langs[self.lan]["filemenu_view_gen"]["Exit"], command=self.on_close)

        self.presetsmenu = tk.Menu(self.mb)
        self.presetsmenu.add_command(label=self.langs[self.lan]["filemenu_view_gen"]["save_preset"], command=self.save_biome_preset)
        self.presetsmenu.add_command(label=self.langs[self.lan]["filemenu_view_gen"]["import_preset"], command=self.open_presets)

        self.toolsmenu = tk.Menu(self.mb)
        self.toolsmenu.add_command(label=self.langs[self.lan]["filemenu_view_gen"]["bulk_menu"], command=self.bulk_edit_menu)
        self.toolsmenu.add_command(label=self.langs[self.lan]["filemenu_view_gen"]["refresh_suggested"], command=self.refresh_suggested_props)
        self.toolsmenu.add_separator()
        self.toolsmenu.add_command(label="nums_for_testing", command=self.nums_for_testing_rockdoors_in_biomes)

        self.editmenu = tk.Menu(self.mb)
        self.editmenu.add_command(label=self.langs[self.lan]["filemenu_view_gen"]["Help"], command=self.open_help)
        self.editmenu.add_command(label=self.langs[self.lan]["filemenu_view_gen"]["about"], command=self.open_about)

        # language menu
        self.langmenu = tk.Menu(self.mb)
        self.langmenu.add_command(label='>>>', command=lambda: self.controller.get_set_lang_from_json_update_plum(force_select_new_lang=True))

        # update menu
        self.updatemenu = tk.Menu(self.mb)
        self.updatemenu.add_command(label=self.langs[self.lan]["filemenu_view_gen"]["check_update"], command=lambda: self.check_plum_update())

        self.donatemenu = tk.Menu(self.mb)
        self.donatemenu.add_command(label=self.langs[self.lan]["filemenu_view_gen"]["donate_page"], command=lambda: webbrowser.open_new("https://www.buymeacoffee.com/sunnysummit"))

        self.mb.add_menu(self.langs[self.lan]["filemenu_view_gen"]["File"], self.filemenu)
        self.mb.add_menu(self.langs[self.lan]["filemenu_view_gen"]["Presets"], self.presetsmenu)
        self.mb.add_menu(self.langs[self.lan]["filemenu_view_gen"]["Tools"], self.toolsmenu)
        self.mb.add_menu(self.langs[self.lan]["filemenu_view_gen"]["Help_2"], self.editmenu)
        self.mb.add_menu(self.langs[self.lan]["filemenu_view_gen"]["Update"], self.updatemenu)
        self.mb.add_menu("Language", self.langmenu)
        self.mb.add_menu(self.langs[self.lan]["filemenu_view_gen"]["Donate"], self.donatemenu)
        

        # listboxes
        self.biome_lb = Listbox(self.window, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10))
        self.distant_objects_lb = Listbox(self.window, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=42)
        self.landmarks_lb = Listbox(self.window, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=42)
        self.objects_lb = Listbox(self.window, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=42)
        self.detail_objects_lb = Listbox(self.window, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=42)
        self.prop_attributes_lb = Listbox(self.window, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=40)
        self.placement_lb = Listbox(self.window, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=40)
        self.model_lb = Listbox(self.window, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=80)
        self.similar_props_lb = Listbox(self.window, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=40)

        # scrollbars
        self.biome_scrollbar = ttk.Scrollbar(self.window, orient=tk.HORIZONTAL, command=self.biome_lb.xview, style="Horizontal.TScrollbar")
        self.biome_vscrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.biome_lb.yview, style="Vertical.TScrollbar")
        self.distant_objects_vscrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.distant_objects_lb.yview, style="Vertical.TScrollbar")
        self.landmarks_vscrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.landmarks_lb.yview, style="Vertical.TScrollbar")
        self.objects_vscrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.objects_lb.yview, style="Vertical.TScrollbar")
        self.detail_objects_vscrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.detail_objects_lb.yview, style="Vertical.TScrollbar")
        self.prop_attribute_scrollbar = ttk.Scrollbar(self.window, orient=tk.HORIZONTAL, command=self.prop_attributes_lb.xview, style="Horizontal.TScrollbar")
        #self.prop_attribute_vscrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.prop_attributes_lb.yview, style="Vertical.TScrollbar")
        self.model_scrollbar = ttk.Scrollbar(self.window, orient=tk.HORIZONTAL, command=self.model_lb.xview, style="Horizontal.TScrollbar")
        self.model_vscrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.model_lb.yview, style="Vertical.TScrollbar")
        self.placem_scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.placement_lb.yview, style="Vertical.TScrollbar")
        self.similar_props_vscrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.similar_props_lb.yview, style="Vertical.TScrollbar")
        self.similar_props_scrollbar = ttk.Scrollbar(self.window, orient=tk.HORIZONTAL, command=self.similar_props_lb.xview, style="Horizontal.TScrollbar")
        #
        self.biome_lb.configure(xscrollcommand=self.biome_scrollbar.set, yscrollcommand=self.biome_vscrollbar.set)
        self.distant_objects_lb.configure(yscrollcommand=self.distant_objects_vscrollbar.set)
        self.landmarks_lb.configure(yscrollcommand=self.landmarks_vscrollbar.set)
        self.objects_lb.configure(yscrollcommand=self.objects_vscrollbar.set)
        self.detail_objects_lb.configure(yscrollcommand=self.detail_objects_vscrollbar.set)
        self.prop_attributes_lb.configure(xscrollcommand=self.prop_attribute_scrollbar.set)
        self.model_lb.configure(xscrollcommand=self.model_scrollbar.set, yscrollcommand=self.model_vscrollbar.set)
        self.placement_lb.configure(yscrollcommand=self.placem_scrollbar.set)
        self.similar_props_lb.configure(xscrollcommand=self.similar_props_scrollbar.set, yscrollcommand=self.similar_props_vscrollbar.set)

        #  add/delete buttons
        self.biome_add_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Add_Biome"], command=self.add_default_biome, style='Create.TButton')
        self.biome_delete_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Delete"], command=self.delete_biome, style='Delete.TButton')
        self.distant_objects_add_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Add_Distant"], command=self.add_default_distant_object, style='Gen.TButton')
        self.distant_objects_delete_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Delete"], command=self.delete_distant_object, style='Delete.TButton')
        self.landmark_add_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Add_Landmark"], command=self.add_default_landmark, style='Gen.TButton')
        self.landmark_delete_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Delete"], command=self.delete_landmark, style='Delete.TButton')
        self.objects_add_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Add_Object"], command=self.add_default_object, style='Gen.TButton')
        self.objects_delete_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Delete"], command=self.delete_object, style='Delete.TButton')
        self.detail_objects_add_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Add_Detail"], command=self.add_default_detail_object, style='Gen.TButton')
        self.detail_objects_delete_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Delete"], command=self.delete_detail_object, style='Delete.TButton')
        
        self.biome_add_button.bind("<Button-3>", self.ask_number_biomes_to_add_menu) # display context menu on right-click
        
        # other buttons
        #self.auto_rename_biomes_button = ttk.Button(self.window, text="Auto Rename All", command=self.auto_rename_biomes, style='Start.TButton')
        #self.reset_auto_names_biomes_button = ttk.Button(self.window, text="Reset Rename", command=self.reset_rename_biomes, style='TButton')
        self.save_rename_biome_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Rename"], command=self.save_renamed_biome, style='Gen.TButton')
        self.duplicate_biome_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Duplicate_Biome"], command=self.duplicate_selected_biome, width=40) # width so text not scrunched
        #self.save_biome_preset_button = ttk.Button(self.window, text="Save Biome as Preset", command=self.save_biome_preset, style='Gen.TButton')
        self.duplicate_prop_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Duplicate_Prop"], command=self.duplicate_selected_prop, width=50)
        #self.open_presets_button = ttk.Button(self.window, text="Import Biome Preset", command=self.open_presets, style='Gen.TButton')
        #self.import_lua_button = ttk.Button(self.window, text="Import LUA Scripts", command=self.import_lua_biomes, style='Start.TButton')
        self.import_exml_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Import"], command=self.import_exml_biomes, style='Start.TButton')
        #self.make_template_from_exml_button = ttk.Button(self.window, text="Make Biome Template from EXML", command=self.make_template_from_exml, style='Gen.TButton')
        self.export_to_xml_button = ttk.Button(self.window, text=f"{self.langs[self.lan]["buttons"]["Continue"]}>>", command=self.export_to_xml, style='Start.TButton', width=20)
        #self.refresh_suggested_props_button = ttk.Button(self.window, text="Refresh Suggested Props", command=self.refresh_suggested_props, style='Gen.TButton')
        self.save_prop_changes_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Save"], width=5, command=self.save_prop_changes)
        self.increment_prop_changes_button = ttk.Button(self.window, text="↑", width=2, command=self.increment_prop_changes, style='Start.TButton')
        self.decrement_prop_changes_button = ttk.Button(self.window, text="↓", width=2, command=self.decrement_prop_changes, style='Gen.TButton')
        #self.bulk_edit_button = ttk.Button(self.window, text="Bulk Edit Menu", command=self.bulk_edit_menu, style='Start.TButton')
        self.save_model_choice_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Save_Model"], command=self.save_model_choice, style='Gen.TButton')
        self.save_placem_choice_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons"]["Save_Placem"], command=self.save_placem_choice, style='Gen.TButton')
        #self.deselect_all_props_button = ttk.Button(self.window, text="Deselect All Props", command=self.deselect_all_props, style='TButton')

        # entry
        self.rename_biome_entry = ttk.Entry(self.window, style='TEntry')
        self.attribute_entry = ttk.Entry(self.window, style='TEntry', font=('TkDefaultFont', 12), width=15)

        # text
        self.model_info = tk.Text(self.window, bg='#444444', fg=self.white_c, wrap=tk.WORD, width=30, height=5)

        # combobox
        self.csv_var = tk.StringVar(value="_Vanilla+Pre NMS.csv")
        self.csv_combo = ttk.Combobox(self.window, textvariable=self.csv_var, style='TCombobox', state="readonly", width=30)

        # separators
        self.separator1 = ttk.Separator(self.window, orient="horizontal")
        self.separator2 = ttk.Separator(self.window, orient="vertical")
        self.separator3 = ttk.Separator(self.window, orient="vertical")
        self.separator4 = ttk.Separator(self.window, orient="vertical")

        # labels
        self.biome_label = ttk.Label(self.window, text=self.langs[self.lan]["labels"]["title_1"], style="TitleLabel.TLabel", wraplength=200, justify=tk.CENTER)
        self.biome_props_label = ttk.Label(self.window, text=self.langs[self.lan]["labels"]["title_2"], style="TitleLabel.TLabel", wraplength=200, justify=tk.CENTER)
        self.prop_attribute_label = ttk.Label(self.window, text=self.langs[self.lan]["labels"]["title_3"], style="TitleLabel.TLabel", wraplength=200, justify=tk.CENTER)
        self.prop_modify_attribute_label = ttk.Label(self.window, text=self.langs[self.lan]["labels"]["title_4"], style="TitleLabel.TLabel", wraplength=200, justify=tk.CENTER)
        self.model_label = ttk.Label(self.window, text=self.langs[self.lan]["labels"]["subtitle_1"], style="Title2Label.TLabel", wraplength=300, justify=tk.CENTER)
        self.related_props_label = ttk.Label(self.window, text=self.langs[self.lan]["labels"]["subtitle_2"], style="Title2Label.TLabel", justify=tk.CENTER)
        self.attribute_desc_label = ttk.Label(self.window, text=self.langs[self.lan]["labels"]["subtitle_3"], style="Title2Label.TLabel", wraplength=200, justify=tk.CENTER)
        self.placement_label = ttk.Label(self.window, text=self.langs[self.lan]["labels"]["subtitle_4"], style="Title2Label.TLabel", wraplength=250, justify=tk.CENTER)
        self.biome_template_label = ttk.Label(self.window, text=self.langs[self.lan]["labels"]["subtitle_5"], style="TLabel", wraplength=200)
        # tooltip
        self.tooltip_label = ttk.Label(self.window, text=self.langs[self.lan]["labels"]["tooltip_def"], style="TLabel", wraplength=220, width=40)

        # checkboxes
        self.hide_tooltip_var = tk.BooleanVar(value=False)
        self.hide_tooltip_cb = ttk.Checkbutton(self.window, text=self.langs[self.lan]["checkboxes"]["hide_tooltip"], variable=self.hide_tooltip_var, command=self.toggle_tooltip) #, width=40
        self.gen_using_template_data_var = tk.BooleanVar(value=False)
        self.gen_using_template_data_cb = ttk.Checkbutton(self.window, text=self.langs[self.lan]["checkboxes"]["add_template_data"], variable=self.gen_using_template_data_var, command=self.gen_using_biome_template_data)
        self.replace_lb_with_template_data_var = tk.BooleanVar(value=False)
        self.replace_lb_with_template_data_cb = ttk.Checkbutton(self.window, text=self.langs[self.lan]["checkboxes"]["use_template_stuff"], variable=self.replace_lb_with_template_data_var, command=self.use_template_placem_models)


    def layout_widgets(self):
        # configure grid weights - expand listboxes/other elements
        for i in range(3, 9):  # rows 3 to 9
            if i != 4 and i != 6 and i != 8:  # exclude rows (e.g. button rows)
                self.window.grid_rowconfigure(i, weight=1)

        for j in range(9):  # columns
            self.window.grid_columnconfigure(j, weight=1)

        # listboxes
        self.biome_lb.grid(row=3, column=0, rowspan=7, columnspan=2, padx=15, pady=(0,20), sticky=tk.NSEW)
        self.distant_objects_lb.grid(row=3, column=2, columnspan=2, padx=15, sticky=tk.NSEW)
        self.landmarks_lb.grid(row=5, column=2, columnspan=2, padx=15, sticky=tk.NSEW)
        self.objects_lb.grid(row=7, column=2, columnspan=2, padx=15, sticky=tk.NSEW)
        self.detail_objects_lb.grid(row=9, column=2, columnspan=2, padx=15, sticky=tk.NSEW)
        self.prop_attributes_lb.grid(row=3, column=4, rowspan=5, columnspan=2, padx=(15,0), sticky=tk.NSEW)
        self.placement_lb.grid(row=7, column=6, rowspan=1, columnspan=1, padx=(15,0), sticky=tk.NSEW)
        self.model_lb.grid(row=3, column=8, rowspan=5, columnspan=2, padx=25, sticky=tk.NSEW)
        self.similar_props_lb.grid(row=9, column=6, rowspan=2, columnspan=4, padx=(15, 25), sticky=tk.NSEW)
        #self.biome_lb.bind("<Motion>", self.on_listbox_mouse_move) # Bind mouse movement events to the listbox
        #self.biome_lb.bind("<Leave>", self.on_listbox_mouse_leave)
        
        # do stuff on left-click
        self.biome_lb.bind("<Button-1>", self.on_biome_lb_left_click)
        self.distant_objects_lb.bind("<Button-1>", self.on_distant_objects_lb_left_click)
        self.landmarks_lb.bind("<Button-1>", self.on_landmarks_lb_left_click)
        self.objects_lb.bind("<Button-1>", self.on_objects_lb_left_click)
        self.detail_objects_lb.bind("<Button-1>", self.on_detail_objects_lb_left_click)
        self.prop_attributes_lb.bind("<Button-1>", self.on_prop_attribute_lb_left_click)
        self.placement_lb.bind("<Button-1>", self.on_placement_lb_left_click)
        self.model_lb.bind("<Button-1>", self.on_model_lb_left_click)
        self.similar_props_lb.bind("<Button-1>", self.on_similar_props_lb_left_click)

        # highlight items on select
        self.biome_lb.bind('<<ListboxSelect>>', self.on_select1)
        self.distant_objects_lb.bind('<<ListboxSelect>>', self.on_select2)
        self.landmarks_lb.bind('<<ListboxSelect>>', self.on_select2)
        self.objects_lb.bind('<<ListboxSelect>>', self.on_select2)
        self.detail_objects_lb.bind('<<ListboxSelect>>', self.on_select2)
        self.prop_attributes_lb.bind('<<ListboxSelect>>', self.on_select3)
        self.placement_lb.bind('<<ListboxSelect>>', self.on_select4)
        self.model_lb.bind('<<ListboxSelect>>', self.on_select5)
        self.similar_props_lb.bind('<<ListboxSelect>>', self.on_select6)

        # scrollbars
        self.biome_scrollbar.grid(row=9, column=0, padx=15, pady=(0, 5), columnspan=2, sticky=tk.EW + tk.S)
        self.biome_vscrollbar.grid(row=3, column=1, padx=(0, 0), pady=(0,20), rowspan=7, sticky=tk.NS + tk.E)
        self.distant_objects_vscrollbar.grid(row=3, column=3, padx=(0, 0), pady=0, sticky=tk.NS + tk.E)
        self.landmarks_vscrollbar.grid(row=5, column=3, padx=(0, 0), pady=0, sticky=tk.NS + tk.E)
        self.objects_vscrollbar.grid(row=7, column=3, padx=(0, 0), pady=0, sticky=tk.NS + tk.E)
        self.detail_objects_vscrollbar.grid(row=9, column=3, padx=(0, 0), pady=0, sticky=tk.NS + tk.E)

        #self.prop_attribute_vscrollbar.grid(row=3, column=5, padx=(0, 0), pady=0, rowspan=5, sticky=tk.NS + tk.E)
        self.prop_attribute_scrollbar.grid(row=8, column=4, padx=(15,0), pady=(0, 20), columnspan=2, sticky=tk.EW)
        self.model_scrollbar.grid(row=8, column=8, padx=25, pady=(0, 10), columnspan=2, sticky=tk.EW)
        self.model_vscrollbar.grid(row=3, column=9, padx=(0, 10), pady=0, rowspan=5, sticky=tk.NS + tk.E)
        self.placem_scrollbar.grid(row=7, column=8, padx=(2, 0), pady=0, rowspan=1, sticky=tk.NS + tk.W)
        self.similar_props_vscrollbar.grid(row=9, column=9, padx=(0, 10), pady=0, rowspan=2, sticky=tk.NS + tk.E)
        self.similar_props_scrollbar.grid(row=11, column=6, padx=(15, 25), pady=(0, 10), columnspan=4, sticky=tk.EW)

        # UI element descriptions
        self.gui_element_descriptions = {
            self.biome_add_button: f">New Biome: \nClick to make a biome.\nRight-click for multiple biomes.",
            self.biome_lb: f">{self.langs[self.lan]["tooltip"]["biome_lb"]}",
            self.distant_objects_lb: f">{self.langs[self.lan]["tooltip"]["distant_objects_lb"]}",
            self.landmarks_lb: f">{self.langs[self.lan]["tooltip"]["landmarks_lb"]}",
            self.objects_lb: f">{self.langs[self.lan]["tooltip"]["objects_lb"]}",
            self.detail_objects_lb: f">{self.langs[self.lan]["tooltip"]["detail_objects_lb"]}",
            #self.prop_attributes_lb: "Prop attributes:\nModify selected prop attributes like density or scale. Click on an attribute to view more info under 'Attribute Info'",
            self.biome_template_label: f">{self.langs[self.lan]["tooltip"]["biome_template_label"]}",
            self.csv_combo: f">{self.langs[self.lan]["tooltip"]["csv_combo"]}",
            self.gen_using_template_data_cb: f"{self.langs[self.lan]["tooltip"]["gen_using_template_data_cb"]}",
            #self.refresh_suggested_props_button: "These model reference counts (numbers inside []) don't affect your biomes whatsoever, but are meant to help you decide what props to add (based on the selected biome template). Additionally, these are saved with the JSON file when clicking 'Save Biome as Preset'.",  
            self.import_exml_button: f"{self.langs[self.lan]["tooltip"]["import_exml_button"]}",
            self.model_lb: f"{self.langs[self.lan]["tooltip"]["model_lb"]}",
        }
        for element in self.gui_element_descriptions.keys():
            element.bind("<Motion>", lambda event, element=element: self.on_listbox_mouse_move(event, element))
            element.bind("<Leave>", self.on_listbox_mouse_leave)

        # add/delete buttons
        self.biome_add_button.grid(row=10, column=0, padx=(15,5), pady=(0,5), sticky=tk.EW)
        self.biome_delete_button.grid(row=10, column=1, padx=(20,15), pady=(0,5), sticky=tk.EW)
        self.distant_objects_add_button.grid(row=4, column=2, padx=15, pady=(0,5), sticky=tk.EW)
        self.distant_objects_delete_button.grid(row=4, column=3, padx=15, pady=(0,5), sticky=tk.EW)
        self.landmark_add_button.grid(row=6, column=2, padx=15, pady=(0,5), sticky=tk.EW)
        self.landmark_delete_button.grid(row=6, column=3, padx=15, pady=(0,5), sticky=tk.EW)
        self.objects_add_button.grid(row=8, column=2, padx=15, pady=(0,5), sticky=tk.EW)
        self.objects_delete_button.grid(row=8, column=3, padx=15, pady=(0,5), sticky=tk.EW)
        self.detail_objects_add_button.grid(row=10, column=2, padx=15, pady=(0,5), sticky=tk.EW)
        self.detail_objects_delete_button.grid(row=10, column=3, padx=15, pady=(0,5), sticky=tk.EW)
        # other buttons
        #self.auto_rename_biomes_button.grid(row=1, column=2, padx=(20,0), pady=5, sticky=tk.S)
        #self.reset_auto_names_biomes_button.grid(row=1, column=3, padx=(20,0), pady=5, sticky=tk.W)
        self.save_rename_biome_button.grid(row=1, column=2, pady=5, sticky=tk.W)
        self.duplicate_biome_button.grid(row=11, column=0, columnspan=2, padx=15, pady=5, sticky=tk.EW)
        #self.save_biome_preset_button.grid(row=12, column=0, columnspan=2, padx=60, pady=5, sticky=tk.EW)
        self.duplicate_prop_button.grid(row=11, column=2, columnspan=2, padx=15, pady=5, sticky=tk.EW)
        #self.open_presets_button.grid(row=12, column=4, columnspan=2, padx=60, pady=5, sticky=tk.EW)
        #self.import_lua_button.grid(row=12, column=7, columnspan=1, padx=20, pady=5, sticky=tk.NS)
        self.import_exml_button.grid(row=11, column=4, columnspan=2, padx=20, pady=5, sticky=tk.EW + tk.N)
        #self.make_template_from_exml_button.grid(row=12, column=8, columnspan=1, padx=20, pady=5, sticky=tk.NS)
        self.export_to_xml_button.grid(row=1, column=9, columnspan=1, rowspan = 2, padx=20, pady=5, sticky=tk.EW)
        #self.refresh_suggested_props_button.grid(row=1, column=9, padx=10, pady=5, sticky=tk.E)
        self.save_prop_changes_button.grid(row=3, column=6, columnspan=2, padx=(15,15), pady=(35,5))
        self.increment_prop_changes_button.grid(row=3, column=6, padx=(15,5), pady=(0,50), sticky=tk.W)
        self.decrement_prop_changes_button.grid(row=3, column=6, padx=(15,5), pady=(50,5), sticky=tk.W)
        self.save_model_choice_button.grid(row=7, column=9, columnspan=1, padx=(0, 25), pady=(0,0), sticky=tk.SE)
        self.save_placem_choice_button.grid(row=7, column=6, columnspan=1, padx=0, pady=(0,0), sticky=tk.SE)
        #self.bulk_edit_button.grid(row=3, column=6, padx=20, pady=20, sticky=tk.NW)
        #self.deselect_all_props_button.grid(row=11, column=4, columnspan=2, sticky=tk.NSEW)

        # entry
        self.rename_biome_entry.grid(row=1, column=0, columnspan=2, padx=(10, 10), sticky=tk.EW)
        self.attribute_entry.grid(row=3, column=6, columnspan=2, padx=(15,15), pady=(0,50))

        # Text
        self.model_info.grid(row=4, column=6, columnspan=2, rowspan=2, padx=(15,0), sticky=tk.NSEW)
        #self.model_info.bind("<Key>", lambda e: "break") # bind the <Key> event to make text widget read-only

        # combobox
        self.csv_combo.grid(row=1, column=4, columnspan=2, sticky=tk.W)
        self.csv_combo.bind("<<ComboboxSelected>>", self.csv_selected)

        # separators
        self.separator1.grid(row=2, column=0, columnspan=10, padx=(5, 5), pady=(5,0), sticky=tk.EW)
        self.separator2.grid(row=2, column=2, rowspan=10, padx=(5, 0), pady=(16,0), sticky=tk.NS + tk.W)
        self.separator3.grid(row=2, column=4, rowspan=10, padx=(5, 0), pady=(16,0), sticky=tk.NS + tk.W)
        self.separator4.grid(row=2, column=6, rowspan=10, padx=(5, 0), pady=(16,0), sticky=tk.NS + tk.W)

        # labels
        self.biome_label.grid(row=2, column=0, columnspan=2)
        self.biome_props_label.grid(row=2, column=2, columnspan=2)
        self.prop_attribute_label.grid(row=2, column=4, columnspan=2)
        self.prop_modify_attribute_label.grid(row=2, column=6, columnspan=2)
        self.model_label.grid(row=2, column=8, columnspan=2)
        self.related_props_label.grid(row=8, column=6, columnspan=3, padx=(10, 0), sticky=tk.SW)
        self.attribute_desc_label.grid(row=3, column=6, columnspan=2, sticky=tk.S)
        self.placement_label.grid(row=6, column=6, columnspan=1, sticky=tk.S)
        self.biome_template_label.grid(row=1, column=3, sticky=tk.E)
        # tooltip
        self.tooltip_label.grid(row=9, column=4, columnspan=2, rowspan=2, sticky=tk.NS, padx=(10, 0)) #, padx=(25, 0)

        # checkboxes
        self.hide_tooltip_cb.grid(row=10, column=4, sticky=tk.E)
        self.gen_using_template_data_cb.grid(row=1, column=6, columnspan=1, padx=5, sticky=tk.E)
        self.replace_lb_with_template_data_cb.grid(row=1, column=7, columnspan=2, padx=5, sticky=tk.W)
    

    # getter
    def get_open_export_window_and_wait(self):
        return self.open_export_window_and_wait



    def check_plum_update(self):
        try:
            # search and update app:
            self.updater = PlumgenUpdater(self.window, self.root, self.langs, self.lan)
            connected_to_internet = self.updater.update_plum()

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    def open_help(self):
        try:
                
            help_window = tk.Toplevel(self.window)
            help_window.title("Help")

            # set DPI awareness, handle scaling better
            try: ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except: pass  # DPI awareness not available

            parent_x = self.window.winfo_rootx()
            parent_y = self.window.winfo_rooty()
            help_window.geometry(f"+{parent_x}+{parent_y}")
            help_window.grab_set()  # prevent this window from going behind main window

            label = tk.Label(help_window, text=self.langs[self.lan]["help"]["read_doc_visit"])
            label.grid(row=0, column=0, padx=10, pady=10)
            link_label = tk.Label(help_window, text="https://github.com/SunnySummit", fg="blue", cursor="hand2")
            link_label.grid(row=1, column=0, padx=10, pady=5)
            link_label.bind("<Button-1>", lambda event: webbrowser.open_new("https://github.com/SunnySummit"))

            close_button = tk.Button(help_window, text=self.langs[self.lan]["help"]["close"], command=help_window.destroy)
            close_button.grid(row=2, column=0, pady=10)

            help_window.mainloop()

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    def open_about(self):
        try:
            messagebox.showinfo(self.langs[self.lan]["about"]["about_title"], f"{self.langs[self.lan]["about"]["author"]}SunnySummit aka goosetehmoose"
                                f"\n{self.langs[self.lan]["about"]["website"]}https://github.com/SunnySummit"
                                f"\n{self.langs[self.lan]["about"]["license"]}GPL-3.0"
                                f"\n\n{self.langs[self.lan]["about"]["desc"]}", parent=self.window)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    # highlight selected items in listboxes (╯° °)╯︵ ┻━┻
    def reset_background_color(self, listbox):
        try:
                
            for index in range(listbox.size()):
                listbox.itemconfig(index, {'bg': self.background_c})

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def handle_listbox_selection(self, listbox, selected_index):
        try:
                
            if selected_index: 
                for index in range(listbox.size()):
                    listbox.itemconfig(index, {'bg': self.background_c})
                listbox.itemconfig(selected_index[0], {'bg': self.highlight_c})

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def on_select1(self, event):
        try:
            selected_index = self.biome_lb.curselection()
            self.handle_listbox_selection(self.biome_lb, selected_index)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            
    def on_select2(self, event):
        try:
            selected_index_dio = self.distant_objects_lb.curselection()
            selected_index_l = self.landmarks_lb.curselection()
            selected_index_o = self.objects_lb.curselection()
            selected_index_deo = self.detail_objects_lb.curselection()
            if selected_index_dio:
                self.reset_background_color(self.distant_objects_lb)
                self.reset_background_color(self.landmarks_lb)
                self.reset_background_color(self.objects_lb)
                self.reset_background_color(self.detail_objects_lb)
                self.distant_objects_lb.itemconfig(selected_index_dio[0], {'bg': self.highlight_c})
            if selected_index_l:
                self.reset_background_color(self.distant_objects_lb)
                self.reset_background_color(self.landmarks_lb)
                self.reset_background_color(self.objects_lb)
                self.reset_background_color(self.detail_objects_lb)
                self.landmarks_lb.itemconfig(selected_index_l[0], {'bg': self.highlight_c})
            if selected_index_o:
                self.reset_background_color(self.distant_objects_lb)
                self.reset_background_color(self.landmarks_lb)
                self.reset_background_color(self.objects_lb)
                self.reset_background_color(self.detail_objects_lb)
                self.objects_lb.itemconfig(selected_index_o[0], {'bg': self.highlight_c})
            if selected_index_deo:
                self.reset_background_color(self.distant_objects_lb)
                self.reset_background_color(self.landmarks_lb)
                self.reset_background_color(self.objects_lb)
                self.reset_background_color(self.detail_objects_lb)
                self.detail_objects_lb.itemconfig(selected_index_deo[0], {'bg': self.highlight_c})
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            
    def on_select3(self, event):
        try:
            selected_index = self.prop_attributes_lb.curselection()
            self.handle_listbox_selection(self.prop_attributes_lb, selected_index)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            
    def on_select4(self, event):
        try:
            selected_index = self.placement_lb.curselection()
            self.handle_listbox_selection(self.placement_lb, selected_index)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            
    def on_select5(self, event):
        try:
            selected_index = self.model_lb.curselection()
            self.handle_listbox_selection(self.model_lb, selected_index)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            
    def on_select6(self, event):
        try:
            selected_index = self.similar_props_lb.curselection()
            self.handle_listbox_selection(self.similar_props_lb, selected_index)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    # mouse move/leave listboxes
    def on_listbox_mouse_move(self, event, listbox):

        # Display tooltip with description
        description = self.gui_element_descriptions.get(listbox, "")
        self.tooltip_label.config(text=description)

    def on_listbox_mouse_leave(self, event):
        if not self.biome_lb.get(0, tk.END):
            self.tooltip_label.config(text=self.langs[self.lan]["lb_mouse_leave"]["default"])
        else:
            self.tooltip_label.config(text="")
            

    # populate the combo box from the controller's csv_path
    def populate_csv_combo(self):
        csv_path = self.controller.get_resources_path()
        csv_files = os.listdir(csv_path)
        csv_files = [f for f in csv_files if f.endswith('.csv')]
        
        self.csv_combo['values'] = csv_files

    def csv_selected(self, event):
        try:
                
            selected_csv = self.csv_var.get()
            self.controller.set_csv_file_data(selected_csv)
            self.similar_props_lb.delete(0, tk.END) # empty listbox
            self.model_lb.delete(0, tk.END) # empty listbox
            if self.replace_lb_with_template_data_var.get(): # only refresh placements if replace with template data cb selected
                self.controller.set_custom_placem_list()
                self.placement_list = self.controller.get_placem_list()
                self.placement_lb.delete(0, tk.END) # refresh listbox
                for placem in self.placement_list:
                    self.placement_lb.insert(tk.END, placem)
                self.placem_val_at_index = None #reset selected placement/models
                self.model_val_at_index = None 
                self.attribute_entry.delete(0, 'end')
            # set generation to the biome template, if gen_using_template_data_var cb was checked
            if self.gen_using_template_data_var.get():
                if selected_csv not in [
                    "_FoundPathAtlas_v3.csv",
                    "_Vanilla+Pre NMS.csv",
                    "Barren_v3.csv",
                    "Cave_v3.csv",
                    "Dead_v3.csv",
                    "Frozen_v3.csv",
                    "Lava_v3.csv",
                    "Lush_v3.csv",
                    "Radioactive_v3.csv",
                    "Scorched_v3.csv",
                    "Swamp_v3.csv",
                    "Toxic_v3.csv",
                    "Underwater_v3.csv",
                    "Weird_v3.csv",
                    "WorldsPart1_v3.csv",
					"WorldsPart2_DeepWater_v3.csv",
                    "WorldsPart2_Reg_v3.csv"
                ]:
                    result = messagebox.askyesno(self.langs[self.lan]["csv_selected"]["warning_title"], self.langs[self.lan]["csv_selected"]["warning_desc"], parent=self.window)
                    if not result:
                        self.gen_using_template_data_var.set(False)
                        return
                else: messagebox.showinfo(self.langs[self.lan]["csv_selected"]["info_title"], f"{self.langs[self.lan]["csv_selected"]["info_desc"]} {selected_csv}", parent=self.window)
                # replace default model path list with list of unique models in biome template
                self.controller.set_custom_model_list()
            else:
                self.controller.set_default_model_list()

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    # helper function to update props listboxes
    def update_listbox(self, listbox, matching_props, path):
        # split('/') or '\' string into a list and get last two elements
        parts = re.split(r'[/\\]', path)
        if len(parts) >= 2:
            second_last_part = parts[-2].title()
            last_part = parts[-1].split('.')[0].upper() # remove .SCENE.MBIN
            final_part = f"{second_last_part} / {last_part}"
            
            listbox.insert(tk.END, final_part + "[" + str(len(matching_props)) + "]")


    def on_biome_lb_left_click(self, event):
        """Handle left-click on an item in biome_lb."""
        try:
                
            if self.biome_lb.size() > 0:

                self.biome_index = self.biome_lb.nearest(event.y)
                selected_biome = self.controller.get_biome_objs()[self.biome_index]

                # display biome name in entry
                fname = selected_biome.get_filename()
                self.rename_biome_entry.delete(0, tk.END)
                self.rename_biome_entry.insert(0, fname)

                # update listboxes with self.model_path from the selected biome
                self.distant_objects_lb.delete(0, tk.END)
                self.landmarks_lb.delete(0, tk.END)
                self.objects_lb.delete(0, tk.END)
                self.detail_objects_lb.delete(0, tk.END)

                for distant_obj_list in selected_biome.get_distant_obj_lists():
                    if distant_obj_list[1]:  # verify that the model filepath is not empty
                        self.update_listbox(self.distant_objects_lb, distant_obj_list[25], distant_obj_list[1])
                for landmark_list in selected_biome.get_landmark_lists():
                    if landmark_list[1]:
                        self.update_listbox(self.landmarks_lb, landmark_list[25], landmark_list[1])
                for objects_list in selected_biome.get_objects_lists():
                    if objects_list[1]:
                        self.update_listbox(self.objects_lb, objects_list[25], objects_list[1])
                for detail_obj_list in selected_biome.get_detail_obj_lists():
                    if detail_obj_list[1]:
                        self.update_listbox(self.detail_objects_lb, detail_obj_list[25], detail_obj_list[1])
                
                self.prop_attributes_lb.delete(0, tk.END)
                self.placem_val_at_index = None #reset selected placement/models
                self.model_val_at_index = None 
                self.attribute_entry.delete(0, 'end')
                self.similar_props_lb.delete(0, tk.END) # empty listbox

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def select_and_highlight_item(self, listbox, item_list, item):
        if item in item_list:
            index = item_list.index(item)
            listbox.selection_set(index)
            self.reset_background_color(listbox)
            listbox.itemconfig(index, {'bg': self.highlight_c})
            listbox.see(index)

    def format_filepath_to_camelcase(self, filepath):
        filepath_without_extension = re.sub(r'\.SCENE\.MBIN$', '', filepath) # remove ".SCENE.MBIN"
        # split('/') or '\' string into a list and get last two elements
        parts = re.split(r'[\\/]', filepath_without_extension)

        # capitalize each part except last one, make the last part all uppercase
        camelcase_parts = [part.title() for part in parts[:-1]]
        camelcase_parts.append(parts[-1].upper())

        # join the parts back into a camel case string with '/'
        camelcase_filepath = ' / '.join(camelcase_parts)
        return camelcase_filepath




    def refresh_distant_attr_placem_models(self):

        self.prop_attributes_lb.delete(0, tk.END)

        for label, item in zip(self.attribute_labels, self.prop_distant):
            if label != self.langs[self.lan]["attribute_labels"]["TotalCountInTemplate"]: 
                display_text = f"{label}{item}"
                self.prop_attributes_lb.insert(tk.END, display_text)
            # select items in listboxes
            if label == self.langs[self.lan]["attribute_labels"]["Filename"]:
                self.select_and_highlight_item(self.model_lb, self.dist_model_list, item)
            elif label == self.langs[self.lan]["attribute_labels"]["Placement"]:
                self.select_and_highlight_item(self.placement_lb, self.placement_list, item)
            elif label == self.langs[self.lan]["attribute_labels"]["TotalCountInTemplate"]: # find this prop (up to 25th index) in prop's list of similar_items
                self.select_and_highlight_item(self.similar_props_lb, self.prop_distant[25], self.prop_distant[:25]) # item
                display_text = f"{label}{len(item)}" # display similar items count
                self.prop_attributes_lb.insert(tk.END, display_text)

        self.placem_val_at_index = None #reset selected placement/models
        self.model_val_at_index = None 
        self.attribute_entry.delete(0, 'end')

    def refresh_landmark_attr_placem_models(self):

        self.prop_attributes_lb.delete(0, tk.END)

        for label, item in zip(self.attribute_labels, self.prop_landmark):
            if label != self.langs[self.lan]["attribute_labels"]["TotalCountInTemplate"]: 
                display_text = f"{label}{item}"
                self.prop_attributes_lb.insert(tk.END, display_text)
            # select items in listboxes
            if label == self.langs[self.lan]["attribute_labels"]["Filename"]:
                self.select_and_highlight_item(self.model_lb, self.landm_model_list, item)
            elif label == self.langs[self.lan]["attribute_labels"]["Placement"]:
                self.select_and_highlight_item(self.placement_lb, self.placement_list, item)
            elif label == self.langs[self.lan]["attribute_labels"]["TotalCountInTemplate"]: # find this prop (up to 25th index) in prop's list of similar_items
                self.select_and_highlight_item(self.similar_props_lb, self.prop_landmark[25], self.prop_landmark[:25]) # item
                display_text = f"{label}{len(item)}" # display similar items count
                self.prop_attributes_lb.insert(tk.END, display_text)

        self.placem_val_at_index = None #reset selected placement/models
        self.model_val_at_index = None 
        self.attribute_entry.delete(0, 'end')

    def refresh_object_attr_placem_models(self):

        self.prop_attributes_lb.delete(0, tk.END)

        for label, item in zip(self.attribute_labels, self.prop_object):
            if label != self.langs[self.lan]["attribute_labels"]["TotalCountInTemplate"]: 
                display_text = f"{label}{item}"
                self.prop_attributes_lb.insert(tk.END, display_text)
            # select items in listboxes
            if label == self.langs[self.lan]["attribute_labels"]["Filename"]:
                self.select_and_highlight_item(self.model_lb, self.objs_model_list, item)
            elif label == self.langs[self.lan]["attribute_labels"]["Placement"]:
                self.select_and_highlight_item(self.placement_lb, self.placement_list, item)
            elif label == self.langs[self.lan]["attribute_labels"]["TotalCountInTemplate"]: # find this prop (up to 25th index) in prop's list of similar_items
                self.select_and_highlight_item(self.similar_props_lb, self.prop_object[25], self.prop_object[:25]) # item
                display_text = f"{label}{len(item)}" # display similar items count
                self.prop_attributes_lb.insert(tk.END, display_text)

        self.placem_val_at_index = None #reset selected placement/models
        self.model_val_at_index = None 
        self.attribute_entry.delete(0, 'end')

    def refresh_detail_attr_placem_models(self):

        self.prop_attributes_lb.delete(0, tk.END)

        for label, item in zip(self.attribute_labels, self.prop_detail):
            if label != self.langs[self.lan]["attribute_labels"]["TotalCountInTemplate"]: 
                display_text = f"{label}{item}"
                self.prop_attributes_lb.insert(tk.END, display_text)
            # select items in listboxes
            if label == self.langs[self.lan]["attribute_labels"]["Filename"]:
                self.select_and_highlight_item(self.model_lb, self.detail_model_list, item)
            elif label == self.langs[self.lan]["attribute_labels"]["Placement"]:
                self.select_and_highlight_item(self.placement_lb, self.placement_list, item)
            elif label == self.langs[self.lan]["attribute_labels"]["TotalCountInTemplate"]: # find this prop (up to 25th index) in prop's list of similar_items
                self.select_and_highlight_item(self.similar_props_lb, self.prop_detail[25], self.prop_detail[:25]) # item
                display_text = f"{label}{len(item)}" # display similar items count
                self.prop_attributes_lb.insert(tk.END, display_text)

        self.placem_val_at_index = None #reset selected placement/models
        self.model_val_at_index = None 
        self.attribute_entry.delete(0, 'end')


    def on_distant_objects_lb_left_click(self, event):
        try:
                
            if self.distant_objects_lb.size() > 0:
                self.prop_draw_type = 1 # set which prop category was selected
                self.model_lb.delete(0, tk.END) # refresh listbox
                for dist_model in self.dist_model_list:
                    camelcase_model = self.format_filepath_to_camelcase(dist_model)
                    self.model_lb.insert(tk.END, camelcase_model)
                self.distant_index = self.distant_objects_lb.nearest(event.y)
                selected_biome = self.controller.get_biome_objs()[self.biome_index]
                distant_obj_lists = selected_biome.get_distant_obj_lists()
                self.prop_distant = distant_obj_lists[self.distant_index]
                
                # add matching props to listbox
                self.similar_props_lb.delete(0, tk.END) # empty listbox
                for matching_prop in self.prop_distant[25]:
                    self.similar_props_lb.insert(tk.END, matching_prop)
                
                self.refresh_distant_attr_placem_models()

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def on_landmarks_lb_left_click(self, event):
        try:
                    
            if self.landmarks_lb.size() > 0:
                self.prop_draw_type = 2
                self.model_lb.delete(0, tk.END) # refresh listbox
                for landm_model in self.landm_model_list:
                    camelcase_model = self.format_filepath_to_camelcase(landm_model)
                    self.model_lb.insert(tk.END, camelcase_model)
                self.landmark_index = self.landmarks_lb.nearest(event.y)
                selected_biome = self.controller.get_biome_objs()[self.biome_index]
                landmark_lists = selected_biome.get_landmark_lists()
                self.prop_landmark = landmark_lists[self.landmark_index]

                # add matching props to listbox
                self.similar_props_lb.delete(0, tk.END) # empty listbox
                for matching_prop in self.prop_landmark[25]:
                    self.similar_props_lb.insert(tk.END, matching_prop)

                self.refresh_landmark_attr_placem_models()

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def on_objects_lb_left_click(self, event):
        try:
                
            if self.objects_lb.size() > 0:
                self.prop_draw_type = 3
                self.model_lb.delete(0, tk.END) # refresh listbox
                for objs_model in self.objs_model_list:
                    camelcase_model = self.format_filepath_to_camelcase(objs_model)
                    self.model_lb.insert(tk.END, camelcase_model)
                self.obj_index = self.objects_lb.nearest(event.y)
                selected_biome = self.controller.get_biome_objs()[self.biome_index]
                objects_lists = selected_biome.get_objects_lists()
                self.prop_object = objects_lists[self.obj_index]

                # add matching props to listbox
                self.similar_props_lb.delete(0, tk.END) # empty listbox
                for matching_prop in self.prop_object[25]:
                    self.similar_props_lb.insert(tk.END, matching_prop)

                self.refresh_object_attr_placem_models()

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def on_detail_objects_lb_left_click(self, event):
        try:
                
            if self.detail_objects_lb.size() > 0:
                self.prop_draw_type = 4
                self.model_lb.delete(0, tk.END) # refresh listbox
                for detail_model in self.detail_model_list:
                    camelcase_model = self.format_filepath_to_camelcase(detail_model)
                    self.model_lb.insert(tk.END, camelcase_model)
                self.detail_index = self.detail_objects_lb.nearest(event.y)
                selected_biome = self.controller.get_biome_objs()[self.biome_index]
                detail_obj_lists = selected_biome.get_detail_obj_lists()
                self.prop_detail = detail_obj_lists[self.detail_index]

                # add matching props to listbox
                self.similar_props_lb.delete(0, tk.END) # empty listbox
                for matching_prop in self.prop_detail[25]:
                    self.similar_props_lb.insert(tk.END, matching_prop)

                self.refresh_detail_attr_placem_models()

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def describe_attribute(self, attr_desc):
        self.model_info.delete("1.0", tk.END)
        self.model_info.insert(tk.END, attr_desc)

    def on_prop_attribute_lb_left_click(self, event):
        try:
                
            if self.prop_attributes_lb.size() > 0:
                self.prop_attribute_index = self.prop_attributes_lb.nearest(event.y)
                selected_biome = self.controller.get_biome_objs()[self.biome_index]

                new_desc = ""

                # dictionary to map attribute indexes to descriptions
                attribute_descriptions = {
                    0: "Type: Misc. attributes. 'Instanced' or 'Single'. Instanced = better performance. Single = extreme draw distance & does not disappear on slopes. Could cause crashes.",
                    1: self.langs[self.lan]["attribute_desc"]["desc_0"],
                    2: self.langs[self.lan]["attribute_desc"]["desc_1"],
                    3: self.langs[self.lan]["attribute_desc"]["desc_2"],
                    4: self.langs[self.lan]["attribute_desc"]["desc_3"],
                    5: self.langs[self.lan]["attribute_desc"]["desc_4"],
                    6: self.langs[self.lan]["attribute_desc"]["desc_5"],
                    7: self.langs[self.lan]["attribute_desc"]["desc_6"],
                    8: self.langs[self.lan]["attribute_desc"]["desc_7"],
                    9: self.langs[self.lan]["attribute_desc"]["desc_8"],
                    10: self.langs[self.lan]["attribute_desc"]["desc_9"],
                    11: self.langs[self.lan]["attribute_desc"]["desc_10"],
                    12: self.langs[self.lan]["attribute_desc"]["desc_11"],
                    13: "MaxYRotation: UNKNOWN - WORLDS PART 1 UPDATE",
                    14: "MaxRaise: UNKNOWN - WORLDS PART 1 UPDATE",
                    15: "MaxLower: UNKNOWN - WORLDS PART 1 UPDATE",
                    16: self.langs[self.lan]["attribute_desc"]["desc_12"],
                    17: self.langs[self.lan]["attribute_desc"]["desc_13"],
                    18: "IsFloatingIsland: UNKNOWN - WORLDS PART 1 UPDATE",
                    19: "/ᐠ⎚-⎚マ",
                    20: self.langs[self.lan]["attribute_desc"]["desc_15"],
                    21: self.langs[self.lan]["attribute_desc"]["desc_16"],
                    22: self.langs[self.lan]["attribute_desc"]["desc_17"],
                    23: self.langs[self.lan]["attribute_desc"]["desc_18"],
                    24: self.langs[self.lan]["attribute_desc"]["desc_19"],
                    25: self.langs[self.lan]["attribute_desc"]["desc_20"]
                }

                # get description based on attribute index
                new_desc = attribute_descriptions.get(self.prop_attribute_index, self.langs[self.lan]["attribute_desc"]["error"])

                self.describe_attribute(new_desc)

                # insert prop attribute depending on prop draw distance type
                if self.prop_draw_type == 1:
                    self.attribute_entry.config(state="normal") # enable if can set via entry
                    self.save_prop_changes_button.config(state=tk.NORMAL)
                    self.attribute_entry.delete(0, tk.END)
                    # don't insert some items (either put these in listbox or they can't be modified)
                    if self.prop_attribute_index != 1 and self.prop_attribute_index != 2 and self.prop_attribute_index != 24 and self.prop_attribute_index != 25:
                        self.attribute_entry.insert(0, self.prop_distant[self.prop_attribute_index])
                    else:
                        self.attribute_entry.insert(0, "N/A")
                        self.attribute_entry.config(state="disabled") # disable if can't set via entry 
                        self.save_prop_changes_button.config(state=tk.DISABLED)
                elif self.prop_draw_type == 2:
                    self.attribute_entry.config(state="normal") # enable if can set via entry
                    self.save_prop_changes_button.config(state=tk.NORMAL)
                    self.attribute_entry.delete(0, tk.END)
                    if self.prop_attribute_index != 1 and self.prop_attribute_index != 2 and self.prop_attribute_index != 24 and self.prop_attribute_index != 25:
                        self.attribute_entry.insert(0, self.prop_landmark[self.prop_attribute_index])
                    else:
                        self.attribute_entry.insert(0, "N/A")
                        self.attribute_entry.config(state="disabled")
                        self.save_prop_changes_button.config(state=tk.DISABLED)
                elif self.prop_draw_type == 3:
                    self.attribute_entry.config(state="normal") # enable if can set via entry
                    self.save_prop_changes_button.config(state=tk.NORMAL)
                    self.attribute_entry.delete(0, tk.END)
                    if self.prop_attribute_index != 1 and self.prop_attribute_index != 2 and self.prop_attribute_index != 24 and self.prop_attribute_index != 25:
                        self.attribute_entry.insert(0, self.prop_object[self.prop_attribute_index])
                    else:
                        self.attribute_entry.insert(0, "N/A")
                        self.attribute_entry.config(state="disabled")
                        self.save_prop_changes_button.config(state=tk.DISABLED)
                elif self.prop_draw_type == 4:
                    self.attribute_entry.config(state="normal") # enable if can set via entry 
                    self.save_prop_changes_button.config(state=tk.NORMAL)
                    self.attribute_entry.delete(0, tk.END)
                    if self.prop_attribute_index != 1 and self.prop_attribute_index != 2 and self.prop_attribute_index != 24 and self.prop_attribute_index != 25:
                        self.attribute_entry.insert(0, self.prop_detail[self.prop_attribute_index])
                    else:
                        self.attribute_entry.insert(0, "N/A")
                        self.attribute_entry.config(state="disabled") # disable if can't set via entry
                        self.save_prop_changes_button.config(state=tk.DISABLED)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



    def on_placement_lb_left_click(self, event):
        try:
                
            placem_index = self.placement_lb.nearest(event.y)
            self.placem_val_at_index = self.placement_list[placem_index]

            # get dictionary of spawn density lists from controller
            sdl_dict = self.controller.get_sdl()

            # display spawn density list item if selected placement name matches key
            if self.placem_val_at_index in sdl_dict:
                #print(sdl_dict[self.placem_val_at_index])
                attributes = sdl_dict[self.placem_val_at_index]

                self.model_info.delete("1.0", tk.END)
                self.model_info.insert(tk.END, self.placem_val_at_index + ":\n")
                self.model_info.insert(tk.END, attributes)

            elif 'X' in self.placem_val_at_index:
                self.model_info.delete("1.0", tk.END)
                self.model_info.insert(tk.END, self.placem_val_at_index + ":\n")
                self.model_info.insert(tk.END, self.langs[self.lan]["placem_click"]["desc_extra"])

            else:
                self.model_info.delete("1.0", tk.END)
                self.model_info.insert(tk.END, self.placem_val_at_index + ":\n")
                self.model_info.insert(tk.END, self.langs[self.lan]["placem_click"]["desc_reg"])

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    def on_model_lb_left_click(self, event):
        try:
                
            model_index = self.model_lb.nearest(event.y)
            
            if self.prop_draw_type == 1:
                self.model_val_at_index = self.dist_model_list[model_index]
            elif self.prop_draw_type == 2:
                self.model_val_at_index = self.landm_model_list[model_index]
            elif self.prop_draw_type == 3:
                self.model_val_at_index = self.objs_model_list[model_index]
            elif self.prop_draw_type == 4:
                self.model_val_at_index = self.detail_model_list[model_index]

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    # replace selected prop with one of the suggested
    def on_similar_props_lb_left_click(self, event):
        try:
                    
            if self.similar_props_lb.size() > 0:
            
                result = messagebox.askyesno(self.langs[self.lan]["sim_props_click"]["title"], self.langs[self.lan]["sim_props_click"]["desc"], parent=self.window)
                if not result:
                    return

                similar_prop_index = self.similar_props_lb.nearest(event.y)
                selected_biome = self.controller.get_biome_objs()[self.biome_index]

                self.model_info.delete("1.0", tk.END)

                # proceed with attribute replacement
                if self.prop_draw_type == 1:
                    replacement_prop = self.prop_distant[25][similar_prop_index]
                    for index, replacement_attr in enumerate(replacement_prop):
                        copied_item = copy.deepcopy(replacement_attr) # deep copy because the copied item is mutable
                        selected_biome.set_custom_distant_attr(self.distant_index, index, copied_item)

                    self.refresh_distant_attr_placem_models()

                elif self.prop_draw_type == 2:
                    replacement_prop = self.prop_landmark[25][similar_prop_index]
                    for index, replacement_attr in enumerate(replacement_prop):
                        copied_item = copy.deepcopy(replacement_attr)
                        selected_biome.set_custom_landmark_attr(self.landmark_index, index, copied_item)

                    self.refresh_landmark_attr_placem_models()

                elif self.prop_draw_type == 3:
                    replacement_prop = self.prop_object[25][similar_prop_index]
                    for index, replacement_attr in enumerate(replacement_prop):
                        copied_item = copy.deepcopy(replacement_attr)
                        selected_biome.set_custom_object_attr(self.obj_index, index, copied_item)

                    self.refresh_object_attr_placem_models()

                elif self.prop_draw_type == 4:
                    replacement_prop = self.prop_detail[25][similar_prop_index]
                    for index, replacement_attr in enumerate(replacement_prop):
                        copied_item = copy.deepcopy(replacement_attr)
                        selected_biome.set_custom_detail_attr(self.detail_index, index, copied_item)
                    
                    self.refresh_detail_attr_placem_models()

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            



    def save_model_choice(self):
        try:
                
            if self.prop_attributes_lb.size() > 0:
            
                if self.model_val_at_index is not None and self.model_val_at_index != "--" and self.model_val_at_index != "":
                
                    selected_biome = self.controller.get_biome_objs()[self.biome_index]

                    # set model path of selected prop based on what was selected in model listbox
                    # refresh 4 prop listboxes and attribute listbox
                    if self.prop_draw_type == 1:
                        selected_biome.set_custom_distant_attr(self.distant_index, 1, self.model_val_at_index)
                        
                        self.refresh_distant_attr_placem_models()

                        self.distant_objects_lb.delete(0, tk.END)
                        for distant_obj_list in selected_biome.get_distant_obj_lists():
                            if distant_obj_list[1]:  # verify that the model filepath is not empty
                                self.update_listbox(self.distant_objects_lb, distant_obj_list[25], distant_obj_list[1])
                    elif self.prop_draw_type == 2:
                        selected_biome.set_custom_landmark_attr(self.landmark_index, 1, self.model_val_at_index)
                        
                        self.refresh_landmark_attr_placem_models()

                        self.landmarks_lb.delete(0, tk.END)
                        for landmark_list in selected_biome.get_landmark_lists():
                            if landmark_list[1]:
                                self.update_listbox(self.landmarks_lb, landmark_list[25], landmark_list[1])
                    elif self.prop_draw_type == 3:
                        selected_biome.set_custom_object_attr(self.obj_index, 1, self.model_val_at_index)
                        
                        self.refresh_object_attr_placem_models()

                        self.objects_lb.delete(0, tk.END)
                        for objects_list in selected_biome.get_objects_lists():
                            if objects_list[1]:
                                self.update_listbox(self.objects_lb, objects_list[25], objects_list[1])
                    elif self.prop_draw_type == 4:
                        selected_biome.set_custom_detail_attr(self.detail_index, 1, self.model_val_at_index)
                        
                        self.refresh_detail_attr_placem_models()

                        self.detail_objects_lb.delete(0, tk.END)
                        for detail_obj_list in selected_biome.get_detail_obj_lists():
                            if detail_obj_list[1]:
                                self.update_listbox(self.detail_objects_lb, detail_obj_list[25], detail_obj_list[1])

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    def save_placem_choice(self):
        try:
                
            if self.prop_attributes_lb.size() > 0:
            
                if self.placem_val_at_index is not None and self.placem_val_at_index != "":

                    selected_biome = self.controller.get_biome_objs()[self.biome_index]

                    self.prop_attributes_lb.delete(0, tk.END)

                    # placement
                    if self.prop_draw_type == 1:
                        selected_biome.set_custom_distant_attr(self.distant_index, 2, self.placem_val_at_index)
                        
                        self.refresh_distant_attr_placem_models()

                    elif self.prop_draw_type == 2:
                        selected_biome.set_custom_landmark_attr(self.landmark_index, 2, self.placem_val_at_index)
                        
                        self.refresh_landmark_attr_placem_models()

                    elif self.prop_draw_type == 3:
                        selected_biome.set_custom_object_attr(self.obj_index, 2, self.placem_val_at_index)
                        
                        self.refresh_object_attr_placem_models()

                    elif self.prop_draw_type == 4:
                        selected_biome.set_custom_detail_attr(self.detail_index, 2, self.placem_val_at_index)
                        
                        self.refresh_detail_attr_placem_models()

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    def toggle_tooltip(self):
        try:
            if self.hide_tooltip_var.get():
                self.tooltip_label.grid_remove() # hide tooltip label
            else:
                self.tooltip_label.grid() # show
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    #-----------------------------------------------------------------

    def refresh_suggested_props(self):
        try:
                
            result = messagebox.askyesno(self.langs[self.lan]["refresh_suggested_props"]["Warning"], self.langs[self.lan]["refresh_suggested_props"]["Warning_Desc"], parent=self.window)
            if not result:
                return
            self.controller.recount_models() # refresh model counts for selected biome template
            
            # empty listboxes
            self.biome_lb.delete(0, tk.END)
            self.distant_objects_lb.delete(0, tk.END)
            self.landmarks_lb.delete(0, tk.END)
            self.objects_lb.delete(0, tk.END)
            self.detail_objects_lb.delete(0, tk.END)
            self.prop_attributes_lb.delete(0, tk.END)
            self.model_lb.delete(0, tk.END)
            self.similar_props_lb.delete(0, tk.END) # empty listbox
            self.model_info.delete("1.0", tk.END)

            # repopulate listbox with new counts
            all_biomes = self.controller.get_biome_objs()
            for biome in all_biomes:
                self.biome_lb.insert(tk.END, biome.get_filename())

            # reset biome index
            self.biome_index = None

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    # check if valid index -> validate new_value type -> set new value
    def set_custom_attr(self, selected_biome, index, new_val, set_val):
        
        if self.prop_attribute_index == 0:
            if new_val not in {"Single", "Instanced"}:
                return
        elif index in {3, 4, 5, 6, 12, 13, 14, 15}:
            if not isinstance(new_val, int):
                messagebox.showinfo(self.langs[self.lan]["set_custom_attr"]["Error"], f"{self.attribute_labels_edited[index]}{self.langs[self.lan]["set_custom_attr"]["warn_integer"]}", parent=self.window)
                return
        elif index in {7, 8, 9, 10, 11, 20, 21, 22, 23}:
            if not isinstance(new_val, numbers.Number):
                messagebox.showinfo(self.langs[self.lan]["set_custom_attr"]["Error"], f"{self.attribute_labels_edited[index]}{self.langs[self.lan]["set_custom_attr"]["warn_number"]}", parent=self.window)
                return
        elif index in {16, 17, 18, 19}:
            if new_val not in {"TRUE", "FALSE"}:
                messagebox.showinfo(self.langs[self.lan]["set_custom_attr"]["Error"], f"{self.attribute_labels_edited[index]}{self.langs[self.lan]["set_custom_attr"]["warn_bool"]}", parent=self.window)
                return
        else:
            messagebox.showinfo(self.langs[self.lan]["set_custom_attr"]["Error_0"], f"{self.langs[self.lan]["set_custom_attr"]["index_warn_pt1"]}{index}{self.langs[self.lan]["set_custom_attr"]["index_warn_pt2"]}", parent=self.window)
            return
        
        if set_val:
            # apply modified value if no errors found
            if index == 0 or (index >= 3 and index <= 23):

                self.prop_attributes_lb.delete(0, tk.END)

                if self.prop_draw_type == 1:
                    selected_biome.set_custom_distant_attr(self.distant_index, index, str(new_val))
                    
                    self.refresh_distant_attr_placem_models()

                elif self.prop_draw_type == 2:
                    selected_biome.set_custom_landmark_attr(self.landmark_index, index, str(new_val))
                    
                    self.refresh_landmark_attr_placem_models()

                elif self.prop_draw_type == 3:
                    selected_biome.set_custom_object_attr(self.obj_index, index, str(new_val))
                    
                    self.refresh_object_attr_placem_models()

                elif self.prop_draw_type == 4:
                    selected_biome.set_custom_detail_attr(self.detail_index, index, str(new_val))
                    
                    self.refresh_detail_attr_placem_models()

            else:
                messagebox.showinfo(self.langs[self.lan]["set_custom_attr"]["Error_1"], f"{self.langs[self.lan]["set_custom_attr"]["2_index_warn_pt1"]}{index}{self.langs[self.lan]["set_custom_attr"]["2_index_warn_pt2"]}", parent=self.window)
                return
            
        else:
            return True

    # when 'save [changes]' button clicked
    def save_prop_changes(self):
        try:
                    
            if self.prop_attributes_lb.size() > 0:
                
                new_value = self.attribute_entry.get()
                pattern = r'^[0-9a-zA-Z.*\-.]+$'
                multiply_pattern = r'^([\d.]+)\s*\*\s*([\d.]+)$'

                if re.match(pattern, new_value): # make sure new_value contains only numbers, letters, '.', '-', or '*'
                    
                    match = re.match(multiply_pattern, new_value) # check if multiplying values
                    if match:
                        # extract two numbers from input
                        num1 = match.group(1)
                        num2 = match.group(2)
                        # convert numbers to appropriate data type
                        num1 = float(num1) if '.' in num1 else int(num1)
                        num2 = float(num2) if '.' in num2 else int(num2)

                        new_value = (num1 * num2) # multiply the two values
                        #print(new_value)

                    else:
                        # try to convert new_value to int or float before accepting it as a string
                        try:
                            new_value = int(new_value) # convert to int
                            #print(f"Converted to int: {new_value}")
                        except ValueError:
                            try:
                                new_value = float(new_value) # convert to float
                                #print(f"Converted to float: {new_value}")
                            except ValueError:
                                #print(f"{new_value} = string")
                                pass 

                    selected_biome = self.controller.get_biome_objs()[self.biome_index]
                    
                    # check what drawdistance lb was selected, then validate index, new_value type, & set new value
                    if self.prop_draw_type == 1:
                        self.set_custom_attr(selected_biome, self.prop_attribute_index, new_value, True)
                    elif self.prop_draw_type == 2:
                        self.set_custom_attr(selected_biome, self.prop_attribute_index, new_value, True)
                    elif self.prop_draw_type == 3:
                        self.set_custom_attr(selected_biome, self.prop_attribute_index, new_value, True)
                    elif self.prop_draw_type == 4:
                        self.set_custom_attr(selected_biome, self.prop_attribute_index, new_value, True)

                else:
                    messagebox.showerror(self.langs[self.lan]["save_prop_changes"]["Error"], self.langs[self.lan]["save_prop_changes"]["Error_Desc"], parent=self.window)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    def bulk_edit_menu(self):
        try:
                    
            if self.prop_attributes_lb.size() > 0 and self.prop_draw_type and self.attribute_entry.get():
                
                bulk_new_value = self.attribute_entry.get()
                pattern = r'^[0-9a-zA-Z.\-]+$'
                multiply_pattern = r'^([\d.]+)\s*\*\s*([\d.]+)$'


                match = re.match(multiply_pattern, bulk_new_value) # check if multiplying values
                if match:
                    # extract two numbers from input
                    num1 = match.group(1)
                    num2 = match.group(2)
                    # convert numbers to appropriate data type
                    num1 = float(num1) if '.' in num1 else int(num1)
                    num2 = float(num2) if '.' in num2 else int(num2)

                    bulk_new_value = num2

                    selected_biome = self.controller.get_biome_objs()[self.biome_index]
                    
                    if self.prop_attribute_index == 0 or (self.prop_attribute_index >= 3 and self.prop_attribute_index <= 23):

                        if self.prop_attribute_index == 0:
                            if bulk_new_value not in {"Single", "Instanced"}:
                                return
                        elif self.prop_attribute_index in {3, 4, 5, 6, 12, 13, 14, 15}:
                            if not isinstance(bulk_new_value, int):
                                messagebox.showinfo(self.langs[self.lan]["bulk_edit_menu"]["Error"], f"{self.attribute_labels_edited[self.prop_attribute_index]}{self.langs[self.lan]["set_custom_attr"]["warn_integer"]}", parent=self.window)
                                return
                        elif self.prop_attribute_index in {7, 8, 9, 10, 11, 20, 21, 22, 23}:
                            if not isinstance(bulk_new_value, numbers.Number):
                                messagebox.showinfo(self.langs[self.lan]["bulk_edit_menu"]["Error"], f"{self.attribute_labels_edited[self.prop_attribute_index]}{self.langs[self.lan]["set_custom_attr"]["warn_number"]}", parent=self.window)
                                return
                        elif self.prop_attribute_index in {16, 17, 18, 19}:
                            if bulk_new_value not in {"TRUE", "FALSE"}:
                                messagebox.showinfo(self.langs[self.lan]["bulk_edit_menu"]["Error"], f"{self.attribute_labels_edited[self.prop_attribute_index]}{self.langs[self.lan]["set_custom_attr"]["warn_bool"]}", parent=self.window)
                                return
                        else:
                            messagebox.showinfo(self.langs[self.lan]["set_custom_attr"]["Error_0"], f"{self.langs[self.lan]["set_custom_attr"]["index_warn_pt1"]}{self.prop_attribute_index}{self.langs[self.lan]["set_custom_attr"]["index_warn_pt2"]}", parent=self.window)
                            return
                    
                        plumgen_view_gen_bulk = PlumgenViewGenBulk(self.root, bulk_new_value, selected_biome, self.attribute_labels_edited, self.prop_attribute_index, self.icon_path, self.langs, self.lan, self.apply_bulk_settings, multiply=True)



                elif re.match(pattern, bulk_new_value) or self.attribute_entry.get() == 'N/A': # make sure new_value contains only numbers, letters, '.', or '-'
                    
                    # try to convert new_value to int or float before accepting it as a string
                    try:
                        bulk_new_value = int(bulk_new_value) # convert to int
                    except ValueError:
                        try:
                            bulk_new_value = float(bulk_new_value) # convert to float
                        except ValueError:
                            pass 

                    selected_biome = self.controller.get_biome_objs()[self.biome_index]
                    
                    bulk_val_validated = False

                    # check what drawdistance lb was selected, then validate index, new_value type, & set new value
                    if self.prop_draw_type == 1 and self.prop_attribute_index == 0 or (self.prop_attribute_index >= 3 and self.prop_attribute_index <= 23):
                        bulk_val_validated = self.set_custom_attr(selected_biome, self.prop_attribute_index, bulk_new_value, False)
                    elif self.prop_draw_type == 2 and self.prop_attribute_index == 0 or (self.prop_attribute_index >= 3 and self.prop_attribute_index <= 23):
                        bulk_val_validated = self.set_custom_attr(selected_biome, self.prop_attribute_index, bulk_new_value, False)
                    elif self.prop_draw_type == 3 and self.prop_attribute_index == 0 or (self.prop_attribute_index >= 3 and self.prop_attribute_index <= 23):
                        bulk_val_validated = self.set_custom_attr(selected_biome, self.prop_attribute_index, bulk_new_value, False)
                    elif self.prop_draw_type == 4 and self.prop_attribute_index == 0 or (self.prop_attribute_index >= 3 and self.prop_attribute_index <= 23):
                        bulk_val_validated = self.set_custom_attr(selected_biome, self.prop_attribute_index, bulk_new_value, False)

                    # instantiate bulk view - display new menu
                    if bulk_val_validated:
                        if self.prop_attribute_index == 0 or (self.prop_attribute_index >= 3 and self.prop_attribute_index <= 23):
                            plumgen_view_gen_bulk = PlumgenViewGenBulk(self.root, bulk_new_value, selected_biome, self.attribute_labels_edited, self.prop_attribute_index, self.icon_path, self.langs, self.lan, self.apply_bulk_settings)
                    
                    # if model selected - attempt to get cursor selection and specific model selected
                    if self.prop_attribute_index == 1:
                        selected_indices = self.model_lb.curselection()
                        if selected_indices:
                            selected_index = self.model_lb.curselection()[0]
                            if self.prop_draw_type == 1: selected_item = self.dist_model_list[selected_index]
                            elif self.prop_draw_type == 2: selected_item = self.landm_model_list[selected_index]
                            elif self.prop_draw_type == 3: selected_item = self.objs_model_list[selected_index]
                            elif self.prop_draw_type == 4: selected_item = self.detail_model_list[selected_index]
                            plumgen_view_gen_bulk = PlumgenViewGenBulk(self.root, selected_item, selected_biome, self.attribute_labels_edited, self.prop_attribute_index, self.icon_path, self.langs, self.lan, self.apply_bulk_settings)
                        else:
                            messagebox.showinfo(self.langs[self.lan]["bulk_edit_menu"]["Click_Model"], self.langs[self.lan]["bulk_edit_menu"]["Click_Model_Desc"], parent=self.window)
                    # if placement selected
                    if self.prop_attribute_index == 2:
                        selected_indices = self.placement_lb.curselection()
                        if selected_indices:
                            selected_index = self.placement_lb.curselection()[0]
                            selected_item = self.placement_list[selected_index]
                            plumgen_view_gen_bulk = PlumgenViewGenBulk(self.root, selected_item, selected_biome, self.attribute_labels_edited, self.prop_attribute_index, self.icon_path, self.langs, self.lan, self.apply_bulk_settings)
                        else:
                            messagebox.showinfo(self.langs[self.lan]["bulk_edit_menu"]["Click_Placement"], self.langs[self.lan]["bulk_edit_menu"]["Click_Placement_Desc"], parent=self.window)

                else:
                    messagebox.showerror(self.langs[self.lan]["bulk_edit_menu"]["Error"], self.langs[self.lan]["bulk_edit_menu"]["Info_1"], parent=self.window)
            else:
                messagebox.showerror(self.langs[self.lan]["bulk_edit_menu"]["Error"], self.langs[self.lan]["bulk_edit_menu"]["Info_2"], parent=self.window)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            
    
    
    # apply bulk settings
    def apply_bulk_settings(self, bulk_new_val, selected_biome, distant, landmark, object, detail, level, multiply_val):

        try:

            if level == '1': # selected Biome Only
                
                # get indices of all items in all 4 listboxes
                all_distant_i = list(range(self.distant_objects_lb.size()))
                all_landm_i = list(range(self.landmarks_lb.size()))
                all_obj_i = list(range(self.objects_lb.size()))
                all_detail_i = list(range(self.detail_objects_lb.size()))
                
                if distant:
                    for index in all_distant_i:
                        if multiply_val: selected_biome.set_multiply_custom_distant_attr(index, self.prop_attribute_index, str(bulk_new_val))
                        else: selected_biome.set_custom_distant_attr(index, self.prop_attribute_index, str(bulk_new_val))
                if landmark:
                    for index in all_landm_i:
                        if multiply_val: selected_biome.set_multiply_custom_landmark_attr(index, self.prop_attribute_index, str(bulk_new_val))
                        else: selected_biome.set_custom_landmark_attr(index, self.prop_attribute_index, str(bulk_new_val))
                if object:
                    for index in all_obj_i:
                        if multiply_val: selected_biome.set_multiply_custom_object_attr(index, self.prop_attribute_index, str(bulk_new_val))
                        else: selected_biome.set_custom_object_attr(index, self.prop_attribute_index, str(bulk_new_val))
                if detail:
                    for index in all_detail_i:
                        if multiply_val: selected_biome.set_multiply_custom_detail_attr(index, self.prop_attribute_index, str(bulk_new_val))
                        else: selected_biome.set_custom_detail_attr(index, self.prop_attribute_index, str(bulk_new_val))
                self.attribute_entry.delete(0, tk.END)
                # empty listboxes
                self.distant_objects_lb.delete(0, tk.END)
                self.landmarks_lb.delete(0, tk.END)
                self.objects_lb.delete(0, tk.END)
                self.detail_objects_lb.delete(0, tk.END)
                self.prop_attributes_lb.delete(0, tk.END)
                self.model_lb.delete(0, tk.END)
                self.similar_props_lb.delete(0, tk.END)

            elif level == '2': # ALL biomes
                for biome in self.controller.get_biome_objs():
                    if distant:
                        for index, distant_obj_list in enumerate(biome.get_distant_obj_lists()):
                            if multiply_val: biome.set_multiply_custom_distant_attr(index, self.prop_attribute_index, str(bulk_new_val))
                            else: biome.set_custom_distant_attr(index, self.prop_attribute_index, str(bulk_new_val))
                    if landmark:
                        for index, landmark_list in enumerate(biome.get_landmark_lists()):
                            if multiply_val: biome.set_multiply_custom_landmark_attr(index, self.prop_attribute_index, str(bulk_new_val))
                            else: biome.set_custom_landmark_attr(index, self.prop_attribute_index, str(bulk_new_val))
                    if object:
                        for index, objects_list in enumerate(biome.get_objects_lists()):
                            if multiply_val: biome.set_multiply_custom_object_attr(index, self.prop_attribute_index, str(bulk_new_val))
                            else: biome.set_custom_object_attr(index, self.prop_attribute_index, str(bulk_new_val))
                    if detail:
                        for index, detail_obj_list in enumerate(biome.get_detail_obj_lists()):
                            if multiply_val: biome.set_multiply_custom_detail_attr(index, self.prop_attribute_index, str(bulk_new_val))
                            else: biome.set_custom_detail_attr(index, self.prop_attribute_index, str(bulk_new_val))
                self.attribute_entry.delete(0, tk.END)
                # empty listboxes
                self.distant_objects_lb.delete(0, tk.END)
                self.landmarks_lb.delete(0, tk.END)
                self.objects_lb.delete(0, tk.END)
                self.detail_objects_lb.delete(0, tk.END)
                self.prop_attributes_lb.delete(0, tk.END)
                self.model_lb.delete(0, tk.END)
                self.similar_props_lb.delete(0, tk.END)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    def increment_prop_changes(self):
        try:
                    
            attr_value = self.attribute_entry.get()
            try:
                attr_value_as_int = int(attr_value) # try to convert to int
                #print("integer")
                self.attribute_entry.delete(0, tk.END)
                attr_value_as_int += 1
                self.attribute_entry.insert(0, attr_value_as_int)
            except ValueError:
                try:
                    attr_value_as_float = float(attr_value) # try to convert to float
                    #print("float")
                    decimal_part = str(attr_value_as_float).split(".")[1]  # extract decimal part
                    decimal_length = len(decimal_part)  # determine length of decimal
                    increment_value = 1 / (10 ** decimal_length)  # increment by 1 based on length of decimal
                    attr_value_as_float += increment_value

                    rounded_value = round(attr_value_as_float, decimal_length) # round to original precision

                    self.attribute_entry.delete(0, tk.END)
                    self.attribute_entry.insert(0, rounded_value)
                except ValueError:
                    if attr_value: # if it's a non-empty string
                        attr_value_lower = attr_value.lower()
                        if attr_value_lower == "true" or attr_value_lower == "false":
                            #print("true/false string")
                            self.attribute_entry.delete(0, tk.END)
                            attr_value = "TRUE"
                            self.attribute_entry.insert(0, attr_value)
                        else:
                            messagebox.showerror(self.langs[self.lan]["crement_prop_changes"]["Error"], self.langs[self.lan]["crement_prop_changes"]["error_short"], parent=self.window)
                    else:
                        messagebox.showerror(self.langs[self.lan]["crement_prop_changes"]["Error"], self.langs[self.lan]["crement_prop_changes"]["error_long"], parent=self.window)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def decrement_prop_changes(self):
        try:
                
            attr_value = self.attribute_entry.get()
            try:
                attr_value_as_int = int(attr_value) # try int
                #print("integer")
                self.attribute_entry.delete(0, tk.END)
                attr_value_as_int -= 1
                self.attribute_entry.insert(0, attr_value_as_int)
            except ValueError:
                try:
                    attr_value_as_float = float(attr_value) # try float
                    #print("float")
                    decimal_part = str(attr_value_as_float).split(".")[1]
                    decimal_length = len(decimal_part)
                    increment_value = 1 / (10 ** decimal_length)  # decrement
                    attr_value_as_float -= increment_value

                    rounded_value = round(attr_value_as_float, decimal_length)

                    self.attribute_entry.delete(0, tk.END)
                    self.attribute_entry.insert(0, rounded_value)
                except ValueError:
                    if attr_value: # if non-empty string
                        attr_value_lower = attr_value.lower()
                        if attr_value_lower == "true" or attr_value_lower == "false":
                            #print("true/false string")
                            self.attribute_entry.delete(0, tk.END)
                            attr_value = "FALSE"
                            self.attribute_entry.insert(0, attr_value)
                        else:
                            messagebox.showerror(self.langs[self.lan]["crement_prop_changes"]["Error"], self.langs[self.lan]["crement_prop_changes"]["error_short"], parent=self.window)
                    else:
                        messagebox.showerror(self.langs[self.lan]["crement_prop_changes"]["Error"], self.langs[self.lan]["crement_prop_changes"]["error_long"], parent=self.window)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    def gen_using_biome_template_data(self):
        try:
                    
            selected_csv = self.csv_var.get()
            # show warning if user using custom biome template .csv
            if self.gen_using_template_data_var.get():
                self.replace_lb_with_template_data_cb.config(state=tk.NORMAL)
                if selected_csv not in [
                    "_FoundPathAtlas_v3.csv",
                    "_Vanilla+Pre NMS.csv",
                    "Barren_v3.csv",
                    "Cave_v3.csv",
                    "Dead_v3.csv",
                    "Frozen_v3.csv",
                    "Lava_v3.csv",
                    "Lush_v3.csv",
                    "Radioactive_v3.csv",
                    "Scorched_v3.csv",
                    "Swamp_v3.csv",
                    "Toxic_v3.csv",
                    "Underwater_v3.csv",
                    "Weird_v3.csv",
                    "WorldsPart1_v3.csv",
					"WorldsPart2_DeepWater_v3.csv",
                    "WorldsPart2_Reg_v3.csv"
                ]:
                    result = messagebox.askyesno(self.langs[self.lan]["csv_selected"]["warning_title"], self.langs[self.lan]["csv_selected"]["warning_desc"], parent=self.window)
                    if not result:
                        self.gen_using_template_data_var.set(False)
                        return
                # replace default model path list with list of unique models in biome template
                self.controller.set_custom_model_list()
                self.controller.set_custom_placem_list() # placements
                
                self.biome_add_button['text'] = self.langs[self.lan]["gen_using_biome_template_data"]["Add_BT_Biome"]
                self.distant_objects_add_button['text'] = self.langs[self.lan]["gen_using_biome_template_data"]["Add_BT_Distant"]
                self.landmark_add_button['text'] = self.langs[self.lan]["gen_using_biome_template_data"]["Add_BT_Landmark"]
                self.objects_add_button['text'] = self.langs[self.lan]["gen_using_biome_template_data"]["Add_BT_Object"]
                self.detail_objects_add_button['text'] = self.langs[self.lan]["gen_using_biome_template_data"]["Add_BT_Detail"]
            else:
                if not self.replace_lb_with_template_data_var.get():
                    self.replace_lb_with_template_data_cb.config(state=tk.DISABLED) # disable next checkbox

                self.controller.set_default_model_list()
                
                self.biome_add_button['text'] = self.langs[self.lan]["gen_using_biome_template_data"]["Add_Biome"]
                self.distant_objects_add_button['text'] = self.langs[self.lan]["gen_using_biome_template_data"]["Add_Distant"]
                self.landmark_add_button['text'] = self.langs[self.lan]["gen_using_biome_template_data"]["Add_Landmark"]
                self.objects_add_button['text'] = self.langs[self.lan]["gen_using_biome_template_data"]["Add_Object"]
                self.detail_objects_add_button['text'] = self.langs[self.lan]["gen_using_biome_template_data"]["Add_Detail"]

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

        #----------------------------------------------------------------------------------------
        

    def use_template_placem_models(self):
        try:
                    
            selected_csv = self.csv_var.get()
            # show warning if a custom Biome Template .csv selected
            if self.replace_lb_with_template_data_var.get():

                self.model_label['text'] = self.langs[self.lan]["use_template_placem_models"]["BT_Model_Desc"]
                self.placement_label['text'] = self.langs[self.lan]["use_template_placem_models"]["BT_Placem_Desc"]

                # refresh model list filepaths with custom ones from biome template
                self.dist_model_list = self.controller.get_dist_list()
                self.landm_model_list = self.controller.get_landm_list()
                self.objs_model_list = self.controller.get_objs_list()
                self.detail_model_list = self.controller.get_detail_list()

                self.placement_list = self.controller.get_placem_list()

                # refresh lb with the new model filepaths
                self.model_lb.delete(0, tk.END) # clear listbox
                if self.prop_draw_type == 1:
                    for dist_model in self.dist_model_list:
                        camelcase_model = self.format_filepath_to_camelcase(dist_model)
                        self.model_lb.insert(tk.END, camelcase_model)
                elif self.prop_draw_type == 2:
                    for landm_model in self.landm_model_list:
                        camelcase_model = self.format_filepath_to_camelcase(landm_model)
                        self.model_lb.insert(tk.END, camelcase_model)
                elif self.prop_draw_type == 3:
                    for objs_model in self.objs_model_list:
                        camelcase_model = self.format_filepath_to_camelcase(objs_model)
                        self.model_lb.insert(tk.END, camelcase_model)
                elif self.prop_draw_type == 4:
                    for detail_model in self.detail_model_list:
                        camelcase_model = self.format_filepath_to_camelcase(detail_model)
                        self.model_lb.insert(tk.END, camelcase_model)
                
                self.placement_lb.delete(0, tk.END)
                for placem in self.placement_list:
                    self.placement_lb.insert(tk.END, placem)

                self.placem_val_at_index = None #reset selected placement/models
                self.model_val_at_index = None 
                self.attribute_entry.delete(0, 'end')
                self.similar_props_lb.delete(0, 'end')

            else:
                if not self.gen_using_template_data_var.get():
                    self.replace_lb_with_template_data_cb.config(state=tk.DISABLED) # disable next checkbox

                self.model_label['text'] = self.langs[self.lan]["use_template_placem_models"]["Model_Desc"]
                self.placement_label['text'] = self.langs[self.lan]["use_template_placem_models"]["Placem_Desc"]
                #self.controller.set_default_model_list() #set default model paths to the default lists

                # refresh model list filepaths with default ones
                self.dist_model_list = self.controller.get_dist_defaults()
                self.landm_model_list = self.controller.get_landm_defaults()
                self.objs_model_list = self.controller.get_objs_defaults()
                self.detail_model_list = self.controller.get_detail_defaults()

                self.placement_list = self.controller.get_placem_defaults()
                
                # refresh lb with the default model filepaths
                self.model_lb.delete(0, tk.END) # clear listbox
                if self.prop_draw_type == 1:
                    for dist_model in self.dist_model_list:
                        camelcase_model = self.format_filepath_to_camelcase(dist_model)
                        self.model_lb.insert(tk.END, camelcase_model)
                elif self.prop_draw_type == 2:
                    for landm_model in self.landm_model_list:
                        camelcase_model = self.format_filepath_to_camelcase(landm_model)
                        self.model_lb.insert(tk.END, camelcase_model)
                elif self.prop_draw_type == 3:
                    for objs_model in self.objs_model_list:
                        camelcase_model = self.format_filepath_to_camelcase(objs_model)
                        self.model_lb.insert(tk.END, camelcase_model)
                elif self.prop_draw_type == 4:
                    for detail_model in self.detail_model_list:
                        camelcase_model = self.format_filepath_to_camelcase(detail_model)
                        self.model_lb.insert(tk.END, camelcase_model)

                self.placement_lb.delete(0, tk.END)
                for placem in self.placement_list:
                    self.placement_lb.insert(tk.END, placem)

                self.placem_val_at_index = None #reset selected placement/models
                self.model_val_at_index = None 
                self.attribute_entry.delete(0, 'end')
                self.similar_props_lb.delete(0, 'end')

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    def save_renamed_biome(self):
        try:
                
            if self.biome_index is not None:
                
                #result = messagebox.askyesno(self.langs[self.lan]["save_renamed_biome"]["Auto_Rename_title"], self.langs[self.lan]["save_renamed_biome"]["Auto_Rename_desc"], parent=self.window)
                #if not result:
                #    return
                
                index = self.biome_index
                new_filename = self.rename_biome_entry.get().strip()
                new_filename = re.sub(r'[^a-zA-Z0-9_\-/\\ ]', '', new_filename) # filter unwanted characters using regex
                if new_filename is not None and new_filename != "" and new_filename != " ":
                    if new_filename not in self.biome_lb.get(0, tk.END):
                        self.controller.c_rename_biome(index, new_filename)
                        self.biome_lb.delete(index)
                        self.biome_lb.insert(index, new_filename)
                    else: 
                        messagebox.showerror(self.langs[self.lan]["save_renamed_biome"]["Duplicate_filen"], self.langs[self.lan]["save_renamed_biome"]["Duplicate_filen_Desc"], parent=self.window)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            
    

    def auto_rename_biomes(self):
        try:
                
            if self.biome_lb.size() > 0:
                
                result = messagebox.askyesno(self.langs[self.lan]["auto_rename_biomes"]["Auto_Rename_title_all"], self.langs[self.lan]["auto_rename_biomes"]["Auto_Rename_desc_all"], parent=self.window)
                if not result:
                    return
                
                self.controller.c_auto_rename_biomes()

                self.biome_lb.delete(0, tk.END)
                self.rename_biome_entry.delete(0, 'end')

                biome_objs = self.controller.get_biome_objs()

                for biome in biome_objs:
                    self.biome_lb.insert(tk.END, biome.get_filename())

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    def reset_rename_biomes(self):
        try:
                
            if self.biome_lb.size() > 0:
                
                result = messagebox.askyesno(self.langs[self.lan]["reset_rename_biomes"]["Reset_rename_title"], self.langs[self.lan]["reset_rename_biomes"]["Reset_rename_desc"], parent=self.window)
                if not result:
                    return
                
                self.controller.c_reset_rename_biomes()

                self.biome_lb.delete(0, tk.END)

                biome_objs = self.controller.get_biome_objs()

                for biome in biome_objs:
                    self.biome_lb.insert(tk.END, biome.get_filename())

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    # biomes
    def add_default_biome(self, times=1):
        try: 
            for _ in range(times):
                new_biome = self.controller.c_create_default_biome()
                self.biome_lb.insert(tk.END, new_biome.get_filename())
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    def ask_number_biomes_to_add_menu(self, event):
        try: 

            # display context menu on right-click. dialog to ask how many biomes to add
            num_times = simpledialog.askstring("Enter Number", "Enter the number of biomes to generate:")
            if num_times is not None:
                if self.is_positive_integer(num_times): # validate input is positive integer
                    
                    num_times = int(num_times)  # convert string to int
                    #if num_times > 500:
                    #    caution = messagebox.askyesno("Caution", 
                    #        "Generating over 500 may cause crashes in-game in the galaxy map\ni think this is the cause? as of NMS v5.29-Jan, '25\nedit: might not be the case anymore with worlds 2, no time to test\n\nDo you want to proceed?", parent=self.window)
                    #    if caution: # user clicks Yes
                    #        self.add_default_biome(num_times)
                    #else:
                    self.add_default_biome(num_times)

                else:
                    messagebox.showerror("Invalid Number", "Please enter a positive integer.", parent=self.window)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))

    def is_positive_integer(self, value):
        try:
            number = int(value)
            return number > 0
        except ValueError:
            return False
            

    def delete_biome(self):
        try:
                
            if self.biome_index is not None:
                result = messagebox.askyesno(self.langs[self.lan]["delete_biome"]["delete_biome_title"], f"{self.langs[self.lan]["delete_biome"]["delete_biome_desc"]}", parent=self.window)
                if not result:
                    return
                
                self.controller.c_delete_biome(self.biome_index)
                self.rename_biome_entry.delete(0, tk.END)  # Clear the entry
                self.biome_lb.delete(self.biome_index)
                # clear listboxes
                self.distant_objects_lb.delete(0, tk.END)
                self.landmarks_lb.delete(0, tk.END)
                self.objects_lb.delete(0, tk.END)
                self.detail_objects_lb.delete(0, tk.END)
                self.prop_attributes_lb.delete(0, tk.END)
                self.model_lb.delete(0, tk.END)
                self.similar_props_lb.delete(0, tk.END)
                self.model_info.delete("1.0", tk.END)

                # reset biome index
                self.biome_index = None
                self.placem_val_at_index = None # reset selected placement/models
                self.model_val_at_index = None 

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def duplicate_selected_biome(self):
        try:
            if self.biome_index is not None:
                new_biome = self.controller.c_duplicate_biome(self.biome_index)
                self.biome_lb.insert(tk.END, new_biome.get_filename())
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    # props
    def repopulate_listbox(self, listbox, biome, get_list_func):
        try: 
            listbox.delete(0, tk.END)
            for obj_list in get_list_func():
                self.update_listbox(listbox, obj_list[25], obj_list[1])
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    # distant objects
    def add_default_distant_object(self):
        try:
            if self.biome_index is not None:
                selected_biome = self.controller.get_biome_objs()[self.biome_index]
                selected_biome.add_distant_obj_list()
                self.controller.process_distant_obj_list(selected_biome)
                self.repopulate_listbox(self.distant_objects_lb, selected_biome, selected_biome.get_distant_obj_lists)
                self.placem_val_at_index = None # reset selected placement/models
                self.model_val_at_index = None 
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def delete_distant_object(self):
        try:
                
            if self.biome_index is not None:
                selected_biome = self.controller.get_biome_objs()[self.biome_index]
                selected_index_tuple = self.distant_objects_lb.curselection()
                if selected_index_tuple:
                    selected_index = selected_index_tuple[0]
                    selected_biome.delete_distant_obj(selected_index)
                    self.prop_attributes_lb.delete(0, tk.END)
                    self.repopulate_listbox(self.distant_objects_lb, selected_biome, selected_biome.get_distant_obj_lists)
                    self.placem_val_at_index = None
                    self.model_val_at_index = None 
                    self.model_lb.delete(0, tk.END)
                    self.similar_props_lb.delete(0, tk.END)
                    self.model_info.delete("1.0", tk.END)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    # landmark
    def add_default_landmark(self):
        try:
                
            if self.biome_index is not None:
                selected_biome = self.controller.get_biome_objs()[self.biome_index]
                selected_biome.add_landmark_list()
                self.controller.process_landmark_list(selected_biome)
                self.repopulate_listbox(self.landmarks_lb, selected_biome, selected_biome.get_landmark_lists)
                self.placem_val_at_index = None
                self.model_val_at_index = None 

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def delete_landmark(self):
        try:
                
            if self.biome_index is not None:
                selected_biome = self.controller.get_biome_objs()[self.biome_index]
                selected_index_tuple = self.landmarks_lb.curselection()
                if selected_index_tuple:
                    selected_index = selected_index_tuple[0]
                    selected_biome.delete_landmark(selected_index)
                    self.prop_attributes_lb.delete(0, tk.END)
                    self.repopulate_listbox(self.landmarks_lb, selected_biome, selected_biome.get_landmark_lists)
                    self.placem_val_at_index = None
                    self.model_val_at_index = None 
                    self.model_lb.delete(0, tk.END)
                    self.similar_props_lb.delete(0, tk.END)
                    self.model_info.delete("1.0", tk.END)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    # objects
    def add_default_object(self):
        try:
                
            if self.biome_index is not None:
                selected_biome = self.controller.get_biome_objs()[self.biome_index]

                selected_csv = self.csv_var.get()
                biome_number = 0
                if "NUMBERS_FOR_TESTING" in selected_csv and self.replace_lb_with_template_data_var.get() and self.gen_using_template_data_var.get():
                    name = selected_biome.get_filename()
                    # split by spaces and check if the last part is a valid number
                    parts = name.split()
                    last_part = parts[-1]

                    if last_part.isdigit():
                        biome_number = int(last_part)

                selected_biome.add_objects_list(biome_number)
                self.controller.process_objects_list(selected_biome)
                self.repopulate_listbox(self.objects_lb, selected_biome, selected_biome.get_objects_lists)
                self.placem_val_at_index = None
                self.model_val_at_index = None 

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def delete_object(self):
        try:
                
            if self.biome_index is not None:
                selected_biome = self.controller.get_biome_objs()[self.biome_index]
                selected_index_tuple = self.objects_lb.curselection()
                if selected_index_tuple:
                    selected_index = selected_index_tuple[0]
                    selected_biome.delete_object(selected_index)
                    self.prop_attributes_lb.delete(0, tk.END)
                    self.repopulate_listbox(self.objects_lb, selected_biome, selected_biome.get_objects_lists)
                    self.placem_val_at_index = None
                    self.model_val_at_index = None
                    self.model_lb.delete(0, tk.END)
                    self.similar_props_lb.delete(0, tk.END)
                    self.model_info.delete("1.0", tk.END)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    # detail objects
    def add_default_detail_object(self):
        try:
                
            if self.biome_index is not None:
                selected_biome = self.controller.get_biome_objs()[self.biome_index]
                selected_biome.add_detail_obj_list()
                self.controller.process_detail_obj_list(selected_biome)
                self.repopulate_listbox(self.detail_objects_lb, selected_biome, selected_biome.get_detail_obj_lists)
                self.placem_val_at_index = None
                self.model_val_at_index = None

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def delete_detail_object(self):
        try:
                
            if self.biome_index is not None:
                selected_biome = self.controller.get_biome_objs()[self.biome_index]
                selected_index_tuple = self.detail_objects_lb.curselection()
                if selected_index_tuple:
                    selected_index = selected_index_tuple[0]
                    selected_biome.delete_detail_obj(selected_index)
                    self.prop_attributes_lb.delete(0, tk.END)
                    self.repopulate_listbox(self.detail_objects_lb, selected_biome, selected_biome.get_detail_obj_lists)
                    self.placem_val_at_index = None
                    self.model_val_at_index = None
                    self.model_lb.delete(0, tk.END)
                    self.similar_props_lb.delete(0, tk.END)
                    self.model_info.delete("1.0", tk.END)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def nums_for_testing_rockdoors_in_biomes(self):
        try:

            selected_csv = self.csv_var.get()
            biome_number = 0
            if "NUMBERS_FOR_TESTING" in selected_csv and self.replace_lb_with_template_data_var.get() and self.gen_using_template_data_var.get():
                # repopulate listbox with new counts
                all_biomes = self.controller.get_biome_objs()
                for bme in all_biomes:
                    name = bme.get_filename()
                    # split by spaces and check if the last part is a valid number
                    parts = name.split()
                    last_part = parts[-1]
                    #all_but_last = parts[:-1]
                    all_but_last = ' '.join(parts[:-1])

                    if last_part.isdigit():
                        biome_number = int(last_part)

                        # rename biomes to fit rock door type
                        if biome_number >= 1 and biome_number <= 50:
                            new_name = all_but_last + f"_{biome_number}_SMALL_FLOAT"
                            bme.set_filename(new_name)
                        elif biome_number >= 51 and biome_number <= 100:
                            new_name = all_but_last + f"_{biome_number-50}_REG"
                            bme.set_filename(new_name)
                        elif biome_number >= 101 and biome_number <= 150:
                            new_name = all_but_last + f"_{biome_number-100}_BIG"
                            bme.set_filename(new_name)
                        elif biome_number >= 151 and biome_number <= 200:
                            new_name = all_but_last + f"_{biome_number-150}_TALL"
                            bme.set_filename(new_name)

                    bme.add_objects_list(biome_number)
                    self.controller.process_objects_list(bme)
                    self.repopulate_listbox(self.objects_lb, bme, bme.get_objects_lists)
                    self.placem_val_at_index = None
                    self.model_val_at_index = None 

                self.biome_lb.delete(0, tk.END)
                all_biomes = self.controller.get_biome_objs()
                for biome in all_biomes:
                    self.biome_lb.insert(tk.END, biome.get_filename())

                if self.biome_index is not None:
                    selected_biome = self.controller.get_biome_objs()[self.biome_index]
                    self.repopulate_listbox(self.objects_lb, selected_biome, selected_biome.get_objects_lists)

                messagebox.showinfo("Affirmative, Dave. I read you.", "Rock doors correctly added to up to 200 biomes.", parent=self.window)
            else:
                messagebox.showinfo("I'm sorry, Dave. I'm afraid I can't do that.", "First, select NUMBERS_FOR_TESTING.csv and two checkmarks.\n\nThis requires ROCKDOORS_TEST_CustomModels.", parent=self.window)




        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))

    # duplicate
    def duplicate_selected_prop(self):
        try:
                
            if self.biome_index is not None:
                selected_biome = self.controller.get_biome_objs()[self.biome_index]
                # list of tuples with listbox, duplication function, and list retrieval function
                listboxes = [
                    (self.distant_objects_lb, selected_biome.duplicate_distant_obj, selected_biome.get_distant_obj_lists),
                    (self.landmarks_lb, selected_biome.duplicate_landmark, selected_biome.get_landmark_lists),
                    (self.objects_lb, selected_biome.duplicate_object, selected_biome.get_objects_lists),
                    (self.detail_objects_lb, selected_biome.duplicate_detail_obj, selected_biome.get_detail_obj_lists)
                ]
                for listbox, duplicate_func, get_lists_func in listboxes:
                    selected_indices = listbox.curselection()
                    if selected_indices:
                        selected_index = selected_indices[0]
                        duplicate_func(selected_index) # call duplication function for selected item
                        # repopulate listbox
                        listbox.delete(0, tk.END)
                        for obj_list in get_lists_func():
                            self.update_listbox(listbox, obj_list[25], obj_list[1])
                        self.placem_val_at_index = None
                        self.model_val_at_index = None

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    # presets
    def save_biome_preset(self):
        try:
                
            if self.biome_lb.size() > 0:
                response = messagebox.askyesno(self.langs[self.lan]["save_biome_preset"]["title"], self.langs[self.lan]["save_biome_preset"]["desc"], parent=self.window)
                if not response:
                    return
                
                # save selected biome to json file in '_Presets' folder
                self.controller.save_biome_preset_to_json(self.biome_index)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    def open_presets(self):
        try:
                
            presets_path = self.controller.get_presets_path()
            
            # verify that the 'presets' directory exists
            if not os.path.exists(presets_path):
                messagebox.showerror(self.langs[self.lan]["open_presets"]["Error"], f"{self.langs[self.lan]["open_presets"]["open_desc_pt1"]}{presets_path}"
                                    f"{self.langs[self.lan]["open_presets"]["open_desc_pt2"]}", parent=self.window)
                return
            else:
                if not os.listdir(presets_path):
                    messagebox.showerror(self.langs[self.lan]["open_presets"]["Error"], f"{self.langs[self.lan]["open_presets"]["2_open_desc_pt1"]}{presets_path}"
                                        f"{self.langs[self.lan]["open_presets"]["2_open_desc_pt2"]}", parent=self.window)
                    return
            
            self.presets_window = tk.Toplevel(self.window) # new window to display list of JSON files
            self.presets_window.title(self.langs[self.lan]["open_presets"]["window_title"])
            self.presets_window.configure(bg="#333333")
            parent_x = self.window.winfo_rootx()
            parent_y = self.window.winfo_rooty()
            self.presets_window.geometry(f"500x600+{parent_x}+{parent_y}")
            
            frame = tk.Frame(self.presets_window, bg="#333333") # frame to contain listbox
            frame.pack(fill=tk.BOTH, expand=True)

            # set weights
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
            
            # listbox to display JSON files
            self.presets_listbox = tk.Listbox(frame, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10))
            self.presets_listbox.grid(row=0, column=0, sticky=tk.NSEW)

            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL) # add scrollbar to listbox
            scrollbar.grid(row=0, column=1, sticky=tk.NS)
            scrollbar.config(command=self.presets_listbox.yview)
            self.presets_listbox.config(yscrollcommand=scrollbar.set)

            # populate the listbox with JSON files in the presets_path directory
            json_files = [file for file in os.listdir(presets_path) if file.endswith('.json')]
            for json_file in json_files:
                self.presets_listbox.insert(tk.END, json_file)

            # close button
            close_button = tk.Button(self.presets_window, text=self.langs[self.lan]["open_presets"]["Close"], command=self.presets_window.destroy)
            close_button.pack(side=tk.BOTTOM, pady=10)

            # bind function to handle selection in the listbox
            self.presets_listbox.bind('<<ListboxSelect>>', self.select_json_preset)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    
    def select_json_preset(self, event):
        try:
                
            selected_index = self.presets_listbox.curselection() # get selected item from the listbox
            if selected_index:
                selected_item = self.presets_listbox.get(selected_index)
                full_filepath = os.path.abspath(os.path.join(self.controller.get_presets_path(), selected_item)) # construct full file path
                # import the selected json file, set as biome object, and append to biome_objs list
                self.controller.import_model_from_json(full_filepath)  # Pass full file path for further processing
                self.biome_lb.delete(0, tk.END) # clear and repopulate listbox
                self.rename_biome_entry.delete(0, 'end')

                biome_objs = self.controller.get_biome_objs()

                for biome in biome_objs:
                    self.biome_lb.insert(tk.END, biome.get_filename())

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    # create and show loading screen
    def show_loading_screen(self):
        # clear listboxes
        self.biome_lb.delete(0, tk.END)
        self.distant_objects_lb.delete(0, tk.END)
        self.landmarks_lb.delete(0, tk.END)
        self.objects_lb.delete(0, tk.END)
        self.detail_objects_lb.delete(0, tk.END)
        self.prop_attributes_lb.delete(0, tk.END)
        self.model_lb.delete(0, tk.END)
        self.similar_props_lb.delete(0, tk.END)
        self.model_info.delete("1.0", tk.END)
        self.attribute_entry.delete(0, 'end') # clear entries
        self.rename_biome_entry.delete(0, tk.END)
        
        for button in self.buttons: # disable import, export, & biome buttons
            button.configure(state="disabled")
        # disable presets menu items
        self.presetsmenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["save_preset"], state='disabled')
        self.presetsmenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["import_preset"], state='disabled')
        self.filemenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["auto_rename"], state='disabled')
        self.filemenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["reset_auto_rename"], state='disabled')
        self.toolsmenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["bulk_menu"], state='disabled')
        self.toolsmenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["refresh_suggested"], state='disabled')
        
        
        loading_screen = tk.Toplevel(self.window)
        loading_screen.title(self.langs[self.lan]["show_loading_screen"]["Loading"])
        loading_screen.configure(bg="#9275bd")
        loading_screen.configure(borderwidth=3)

        loading_screen_width = 325
        loading_screen_height = 170
        parent_width = self.window.winfo_width()
        parent_height = self.window.winfo_height()
        x_offset = (parent_width - loading_screen_width) // 2
        y_offset = (parent_height - loading_screen_height) // 2

        loading_screen.geometry(f"+{self.window.winfo_rootx() + x_offset}+{self.window.winfo_rooty() + y_offset}")
        loading_screen.overrideredirect(True) # remove window decorations
        
        # create and place label widget with loading message
        loading_label = ttk.Label(loading_screen, text=self.langs[self.lan]["show_loading_screen"]["Loading_Desc"], justify=tk.CENTER, style="Title3Label.TLabel")
        loading_label.grid(row=0, column=0, padx=0, pady=0)

        loading_screen.attributes("-topmost", True)
        #loading_screen.grab_set()
        loading_screen.update()
        
        return loading_screen


    def reenable_buttons(self):
        # re-enable UI elements
        for button in self.buttons:
            button.configure(state="normal")
        self.presetsmenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["save_preset"], state='normal')
        self.presetsmenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["import_preset"], state='normal')
        self.filemenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["auto_rename"], state='normal')
        self.filemenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["reset_auto_rename"], state='normal')
        self.toolsmenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["bulk_menu"], state='normal')
        self.toolsmenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["refresh_suggested"], state='normal')


    def complete_import(self, loading_screen):
        # repopulate listbox with new counts
        all_biomes = self.controller.get_biome_objs()

        self.import_exml_button.configure(state="normal")
        self.reenable_buttons()

        biomes_to_delete = []
        for index, biome in enumerate(all_biomes):
            self.biome_lb.insert(tk.END, biome.get_filename())
            if "/Objects/" in biome.get_filename() or "vfx" in biome.get_filename():
                #print("Problem biome file index:", index)
                biomes_to_delete.append(index)

        loading_screen.destroy()

        if len(biomes_to_delete) > 0:
            response = messagebox.askyesno(self.langs[self.lan]["complete_import"]["warn_title"], f"{self.langs[self.lan]["complete_import"]["warn_desc_pt1"]}{len(biomes_to_delete)}{self.langs[self.lan]["complete_import"]["warn_desc_pt2"]}", parent=self.window)
            if response:
                # delete biomes from controller after iterating through all_biomes
                for index in reversed(biomes_to_delete):
                    self.controller.c_delete_biome(index)

                # repopulate listbox
                self.biome_lb.delete(0, tk.END)
                for index, biome in enumerate(all_biomes):
                    self.biome_lb.insert(tk.END, biome.get_filename())




        # reset biome index
        self.biome_index = None

        if len(self.controller.get_bfn_all_biome_files_weights()) < 17:
            messagebox.showinfo(f"<{self.langs[self.lan]["complete_import"]["warn_missing_title"]}", self.langs[self.lan]["complete_import"]["warn_missing_desc"], parent=self.window)
        else:
            messagebox.showinfo(self.langs[self.lan]["complete_import"]["info_title"], self.langs[self.lan]["complete_import"]["info_desc"], parent=self.window)

        #self.controller.recount_models() # refresh model counts for selected Biome Template



    # import
        
    #def import_lua_biomes(self):
    #    pass
        

    def import_exml_biomes_threaded(self, loading_screen, temp_date_of_import_folder):
        self.controller.c_import_xml_biomes(temp_date_of_import_folder)
        self.window.after(0, lambda: self.complete_import(loading_screen))

    def import_exml_biomes(self):
        try:
                    
            biom_exmls_folder_dir = self.controller.get_biom_exmls_folder_dir()
            biomes_folder = os.path.abspath(os.path.join(biom_exmls_folder_dir, 'BIOMES'))

            # verify that the '_BIOMES Xmls Folder Goes Here' directory exists
            if not os.path.exists(biom_exmls_folder_dir):
                messagebox.showerror(self.langs[self.lan]["import_exml_biomes"]["Error"], f"{self.langs[self.lan]["import_exml_biomes"]["no_dir_pt1"]}{biom_exmls_folder_dir}{self.langs[self.lan]["import_exml_biomes"]["no_dir_pt2"]}", parent=self.window)
                return
            else:
                if not os.listdir(biom_exmls_folder_dir):
                    messagebox.showerror(self.langs[self.lan]["import_exml_biomes"]["Error"], f"{self.langs[self.lan]["import_exml_biomes"]["empty_dir_pt1"]}{biom_exmls_folder_dir}{self.langs[self.lan]["import_exml_biomes"]["empty_dir_pt2"]}", parent=self.window)
                    return
                else:
                    if not os.path.exists(biomes_folder): # check if 'BIOMES' folder in directory
                        response = messagebox.askyesnocancel(self.langs[self.lan]["import_exml_biomes"]["Question"], f"{self.langs[self.lan]["import_exml_biomes"]["ques_pt1"]}{biom_exmls_folder_dir}{self.langs[self.lan]["import_exml_biomes"]["ques_pt2"]}", parent=self.window)
                        if not response:
                            return

            # check if imported already, show overwrite message if yes
            imported_variables = []
            if self.controller.get_biome_objs():  imported_variables.append("biome_objs")
            if self.controller.get_bfn_all_biome_files_weights():  imported_variables.append("bfn_all_biome_files_weights")
            if self.controller.get_bfn_all_tile_types(): imported_variables.append("bfn_all_tile_types")
            if self.controller.get_bfn_all_valid_start_planets(): imported_variables.append("bfn_all_valid_start_planets")
            if self.controller.get_bfn_valid_purple_moon_biomes(): imported_variables.append("bfn_valid_purple_moon_biomes_planets") # worlds pt II
            if self.controller.get_bfn_valid_giant_planet_biomes(): imported_variables.append("bfn_valid_giant_planet_biomes")
            if self.controller.get_all_biome_tile_types(): imported_variables.append("all_biome_tile_types")

            if imported_variables:

                response = messagebox.askyesno(self.langs[self.lan]["import_exml_biomes"]["overwrite_ques_title"], self.langs[self.lan]["import_exml_biomes"]["overwrite_ques_desc"], parent=self.window)
                if not response:
                    return


            #after_next_update = messagebox.askyesnocancel(self.langs[self.lan]["import_exml_biomes"]["Question"], self.langs[self.lan]["import_exml_biomes"]["after_before_next_ques_desc"], parent=self.window)
            


            self.date_of_import_folder = None # reset
            self.make_game_date_window()





            self.import_exml_button.configure(state="disabled")
            # show loading screen
            loading_screen = self.show_loading_screen()
            self.window.update_idletasks()  # all pending events processed to show loading screen
            
            if self.date_of_import_folder is not None:  # check if user clicked Yes or No

                self.open_export_window_and_wait = False
                temp_date_of_import_folder= self.date_of_import_folder
                import_thread = threading.Thread(target=self.import_exml_biomes_threaded, args=(loading_screen, temp_date_of_import_folder))
                import_thread.start()
            
            else:
                self.reenable_buttons()
                loading_screen.destroy()
                return

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            





    def bulk_import_update(self):
        try:
                    
            biom_exmls_folder_dir = self.controller.get_biom_exmls_folder_dir()
            biomes_folder = os.path.abspath(os.path.join(biom_exmls_folder_dir, 'BIOMES'))

            # verify that the '_BIOMES Xmls Folder Goes Here' directory exists
            if not os.path.exists(biom_exmls_folder_dir):
                messagebox.showerror(self.langs[self.lan]["import_exml_biomes"]["Error"], f"{self.langs[self.lan]["import_exml_biomes"]["no_dir_pt1"]}{biom_exmls_folder_dir}{self.langs[self.lan]["import_exml_biomes"]["no_dir_pt2"]}", parent=self.window)
                return
            else:
                if not os.listdir(biom_exmls_folder_dir):
                    messagebox.showerror(self.langs[self.lan]["import_exml_biomes"]["Error"], f"{self.langs[self.lan]["import_exml_biomes"]["empty_dir_pt1"]}{biom_exmls_folder_dir}{self.langs[self.lan]["import_exml_biomes"]["empty_dir_pt2"]}", parent=self.window)
                    return
                else:
                    if not os.path.exists(biomes_folder): # check if 'BIOMES' folder in directory
                        response = messagebox.askyesnocancel(self.langs[self.lan]["import_exml_biomes"]["Question"], f"{self.langs[self.lan]["import_exml_biomes"]["ques_pt1"]}{biom_exmls_folder_dir}{self.langs[self.lan]["import_exml_biomes"]["ques_pt2"]}", parent=self.window)
                        if not response:
                            return

            # check if imported already, show overwrite message if yes
            imported_variables = []
            if self.controller.get_biome_objs():  imported_variables.append("biome_objs")
            if self.controller.get_bfn_all_biome_files_weights():  imported_variables.append("bfn_all_biome_files_weights")
            if self.controller.get_bfn_all_tile_types(): imported_variables.append("bfn_all_tile_types")
            if self.controller.get_bfn_all_valid_start_planets(): imported_variables.append("bfn_all_valid_start_planets")
            if self.controller.get_bfn_valid_purple_moon_biomes(): imported_variables.append("bfn_valid_purple_moon_biomes_planets") # worlds pt II
            if self.controller.get_bfn_valid_giant_planet_biomes(): imported_variables.append("bfn_valid_giant_planet_biomes")
            if self.controller.get_all_biome_tile_types(): imported_variables.append("all_biome_tile_types")

            if imported_variables:

                response = messagebox.askyesno(self.langs[self.lan]["import_exml_biomes"]["overwrite_ques_title"], self.langs[self.lan]["import_exml_biomes"]["overwrite_ques_desc"], parent=self.window)
                if not response:
                    return


            #after_next_update = messagebox.askyesnocancel(self.langs[self.lan]["import_exml_biomes"]["Question"], self.langs[self.lan]["import_exml_biomes"]["after_before_next_ques_desc"], parent=self.window)

            self.date_of_import_folder = None # reset
            self.make_game_date_window()

            #TODO

            
            self.import_exml_button.configure(state="disabled")
            # show loading screen
            #loading_screen = self.show_loading_screen()
            self.window.update_idletasks()  # all pending events processed to show loading screen
            
            if self.date_of_import_folder is not None:  # check if user clicked

                self.open_export_window_and_wait = True
                self.controller.c_import_xml_biomes(self.date_of_import_folder)
                self.open_export_window_and_wait = False
                self.biome_lb.delete(0, tk.END)
                self.import_exml_button.configure(state="normal")
                self.reenable_buttons()
            
            else:
                self.reenable_buttons()
                #loading_screen.destroy()
                return

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



    def make_game_date_window(self):
        # create window
        select_game_date_window = tk.Toplevel(self.window)
        select_game_date_window.title("_BIOMES Xmls Folder Goes Here/BIOMES")
        select_game_date_window.configure(bg="#333333")
        select_game_date_window.iconbitmap(self.icon_path)
        #select_game_date_window.geometry("300x150")
        # set DPI awareness, handle scaling better
        try: ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except: pass  # DPI awareness not available

        parent_x = self.window.winfo_rootx()
        parent_y = self.window.winfo_rooty()
        select_game_date_window.geometry(f"+{parent_x}+{parent_y}")
        select_game_date_window.resizable(False, False)  # prevent resizing
        select_game_date_window.grab_set()  # prevent this window from going behind main window

        # label with question
        label = ttk.Label(select_game_date_window, text="When was the 'BIOMES' folder created?", style="Title3Label.TLabel", justify=tk.CENTER)
        label2 = ttk.Label(select_game_date_window, text="--- Answering this incorrectly WILL cause issues. ---", style="TLabel", justify=tk.CENTER)
        label.grid(row=0, column=0, columnspan=3, pady=10)
        label2.grid(row=4, column=0, columnspan=3, pady=10)

        # function to set result and close dialog
        def set_result(option):
            self.date_of_import_folder = option
            select_game_date_window.destroy()

        # buttons
        button1 = tk.Button(select_game_date_window, text="Worlds Part 2 or later (02/25)", command=lambda: set_result("1. After Worlds 1"))
        button1.grid(row=1, column=0, padx=(100), pady=(12,12), sticky=tk.NSEW)
        button1.config(bg='#38943a', fg='white')

        button2 = tk.Button(select_game_date_window, text="NEXT to Worlds Pt. 1 (07/18-01/25)", command=lambda: set_result("2. NEXT to Worlds Part 1"))
        button2.grid(row=2, column=0, padx=(100), pady=(12,12), sticky=tk.NSEW)
        button2.config(bg='#943866', fg='white')

        button3 = tk.Button(select_game_date_window, text="Atlas Rises or earlier (07/18)", command=lambda: set_result("3. Before NEXT"))
        button3.grid(row=3, column=0, padx=(100), pady=(12,12), sticky=tk.NSEW)
        button3.config(bg='#389494', fg='white')

        # Wait for the dialog to close and return the result
        select_game_date_window.wait_window(select_game_date_window)





    def complete_template(self, loading_screen):
        loading_screen.destroy()
        self.populate_csv_combo()

        self.reenable_buttons()
        self.filemenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["make_template"], state='normal') # re-enable template menu item

        # repopulate listbox
        all_biomes = self.controller.get_biome_objs()
        self.biome_lb.delete(0, tk.END)
        for index, biome in enumerate(all_biomes):
            self.biome_lb.insert(tk.END, biome.get_filename())

        messagebox.showinfo(self.langs[self.lan]["complete_template"]["info_title"], self.langs[self.lan]["complete_template"]["info_desc"], parent=self.window)


    def make_template_from_exml_threaded(self, template_filename, loading_screen, temp_date_of_import_folder):
        # import exml files in "_BIOMES Xmls Folder Goes Here" folder, pass if after next update or not
        self.controller.c_make_template_from_xml(template_filename, temp_date_of_import_folder)
        self.window.after(0, lambda: self.complete_template(loading_screen))


    def make_template_from_exml(self):
        try:
                
            self.populate_csv_combo()

            biom_exmls_folder_dir = self.controller.get_biom_exmls_folder_dir()
            biomes_folder = os.path.abspath(os.path.join(biom_exmls_folder_dir, 'BIOMES'))

            # verify that the '_BIOMES Xmls Folder Goes Here' directory exists
            if not os.path.exists(biom_exmls_folder_dir):
                messagebox.showerror(self.langs[self.lan]["make_template_from_exml"]["Error"], f"{self.langs[self.lan]["make_template_from_exml"]["desc_1_pt1"]}{biom_exmls_folder_dir}{self.langs[self.lan]["make_template_from_exml"]["desc_1_pt2"]}", parent=self.window)
                return
            else:
                if not os.listdir(biom_exmls_folder_dir):
                    messagebox.showerror(self.langs[self.lan]["make_template_from_exml"]["Error"], f"{self.langs[self.lan]["make_template_from_exml"]["desc_2_pt1"]}{biom_exmls_folder_dir}{self.langs[self.lan]["make_template_from_exml"]["desc_2_pt2"]}", parent=self.window)
                    return
                else:
                    if not os.path.exists(biomes_folder): # check if 'BIOMES' folder in directory
                        response = messagebox.askyesnocancel(self.langs[self.lan]["make_template_from_exml"]["Question"], f"{self.langs[self.lan]["make_template_from_exml"]["desc_3_pt1"]}{biom_exmls_folder_dir}{self.langs[self.lan]["make_template_from_exml"]["desc_3_pt2"]}", parent=self.window)
                        if not response:
                            return

            #after_next_update = messagebox.askyesnocancel(self.langs[self.lan]["make_template_from_exml"]["Question"], self.langs[self.lan]["make_template_from_exml"]["desc_4"], parent=self.window)




            self.date_of_import_folder = None # reset
            self.make_game_date_window()


            
            if self.date_of_import_folder is not None:
                # create pop-up window to enter filename
                template_filename = simpledialog.askstring(self.langs[self.lan]["make_template_from_exml"]["template_title"], self.langs[self.lan]["make_template_from_exml"]["template_desc"], parent=self.window)
                # verify filename contains numbers, letters, or underscores
                if template_filename and re.match("^[a-zA-Z0-9_]+$", template_filename):
                    template_filename = f"{template_filename}-unsorted.csv" # add '-unsorted.csv'
                else:
                    messagebox.showerror(self.langs[self.lan]["make_template_from_exml"]["Invalid_Filename_title"], self.langs[self.lan]["make_template_from_exml"]["Invalid_Filename_desc"], parent=self.window)
                    return
            
            self.filemenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["make_template"], state='disabled') # disable make biome template
            # show loading screen
            loading_screen = self.show_loading_screen()
            self.window.update_idletasks()  # all pending events processed to show loading screen
            
            if self.date_of_import_folder is not None:  # check if user clicked
                temp_date_of_import_folder = self.date_of_import_folder
                import_thread = threading.Thread(target=self.make_template_from_exml_threaded, args=(template_filename, loading_screen, temp_date_of_import_folder))
                import_thread.start()

            else:
                self.reenable_buttons()
                self.filemenu.entryconfig(self.langs[self.lan]["filemenu_view_gen"]["make_template"], state='normal')
                loading_screen.destroy() # hide loading screen
                return

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            
    


    # -------------------------------------------------
    # ------------------- KEEP THIS -------------------
    # -------------------------------------------------
    '''
    def export_to_json(self, filename):
        try:
            data = {
                "bfn_all_biome_files_weights": self.controller.get_bfn_all_biome_files_weights(),
                "bfn_all_tile_types": self.controller.get_bfn_all_tile_types(),
                "bfn_all_valid_start_planets": self.controller.get_bfn_all_valid_start_planets(),
                "bfn_valid_purple_moon_biomes_planets": self.controller.get_bfn_valid_purple_moon_biomes(), # worlds pt II
                "bfn_valid_giant_planet_biomes": self.controller.get_bfn_valid_giant_planet_biomes(),
                "all_biome_tile_types": self.controller.get_all_biome_tile_types()
            }

            with open(filename, "w") as json_file:
                json.dump(data, json_file, indent=4)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
    '''

    def import_from_json(self, filename):
        with open(filename, "r") as json_file:
            data = json.load(json_file)
        
        bfn_all_biome_files_weights = data["bfn_all_biome_files_weights"]
        bfn_all_tile_types = data["bfn_all_tile_types"]
        bfn_all_valid_start_planets = data["bfn_all_valid_start_planets"]
        bfn_valid_purple_moon_biomes_planets = data["bfn_valid_purple_moon_biomes_planets"] # worlds pt II
        bfn_valid_giant_planet_biomes = data["bfn_valid_giant_planet_biomes"]
        all_biome_tile_types = data["all_biome_tile_types"]

        return bfn_all_biome_files_weights, bfn_all_tile_types, bfn_all_valid_start_planets, bfn_valid_purple_moon_biomes_planets, bfn_valid_giant_planet_biomes, all_biome_tile_types



    # export
    def export_to_xml(self):
        try:
            
            biomes_objs = self.controller.get_biome_objs()

            # get any imported data
            bfn_all_biome_files_weights = self.controller.get_bfn_all_biome_files_weights()
            bfn_all_tile_types = self.controller.get_bfn_all_tile_types()
            bfn_all_valid_start_planets = self.controller.get_bfn_all_valid_start_planets()
            bfn_valid_purple_moon_biomes_planets = self.controller.get_bfn_valid_purple_moon_biomes() # worlds pt II
            bfn_valid_giant_planet_biomes = self.controller.get_bfn_valid_giant_planet_biomes()
            all_biome_tile_types = self.controller.get_all_biome_tile_types() # **each** biome file
            
            # -------------------------------------------------
            # ------------------- KEEP THIS -------------------
            # -------------------------------------------------
            # ---EXPORT--- data to JSON - use if vanilla biomefilenames.MBIN or each ___biome.MBIN files ever receive update (i.e. new biomes)
            #default_bfn_folder_dir = self.controller.get_default_bfn_folder_dir()
            #json_file_path = os.path.abspath(os.path.join(default_bfn_folder_dir, 'default_bfn_and_biomes.json'))
            #self.export_to_json(json_file_path)


            missing_variables = []
            missing_var_a = False
            missing_var_b = False
            missing_var_c = False
            response = False # track auto import JSON data or user's response
                
            if not bfn_all_biome_files_weights:
                missing_variables.append("A. bfn_weights")
                missing_var_a = True
            if not bfn_all_tile_types:
                missing_variables.append("B. bfn_tiles")
                missing_var_b = True
            if not all_biome_tile_types:
                missing_variables.append("C. biome_tiles")
                missing_var_c = True

            if missing_var_a and missing_var_b and missing_var_c:
                response = True # automatically import spawner data if all are missing
            
            if missing_variables:
                missing_variables_str = ", ".join(missing_variables)

                if not response: # if not all spawner data is missing, prompt to ask what data to replace

                    response = messagebox.askyesnocancel(self.langs[self.lan]["export_script"]["import_json_title"], f"{self.langs[self.lan]["export_script"]["import_json_desc_pt1"]}{missing_variables_str}{self.langs[self.lan]["export_script"]["import_json_desc_pt2"]}", parent=self.window)

                #response = messagebox.askyesnocancel("Import Vanilla JSON?", f"Some spawner data not configured. Details: \n{missing_variables_str}"
                #                            "\n\nTo create this, we'll import data to fill in an empty \"spawner canvas.\""
                #                            "\n\nContinue with creating the spawner canvas?"
                #                            "\nThis will not replace your current Biome Objects List."
                #                            "\n\nYes = Replace any MISSING spawner data."
                #                            "\nNo = Replace ALL spawner data.", parent=self.window)

                replace_missing_vars_w_json = False
                if response is None: # cancel
                    return
                elif response: # yes
                    replace_missing_vars_w_json = True
                # no = replace_missing_vars_w_json stays False


                default_bfn_folder_dir = self.controller.get_default_bfn_folder_dir()
                json_file_path = os.path.abspath(os.path.join(default_bfn_folder_dir, 'default_bfn_and_biomes.json'))

                # verify that the '_BIOMES Xmls Folder Goes Here' directory exists
                if not os.path.exists(default_bfn_folder_dir):
                    messagebox.showerror("Error", f"{self.langs[self.lan]["export_script"]["missing_dir_pt1"]}{default_bfn_folder_dir}{self.langs[self.lan]["export_script"]["missing_dir_pt2"]}", parent=self.window)
                    return

                if not os.path.isfile(json_file_path):
                    messagebox.showerror("Error", f"{self.langs[self.lan]["export_script"]["missing_json_pt1"]}{json_file_path}{self.langs[self.lan]["export_script"]["missing_json_pt2"]}", parent=self.window)
                    return

                # import data from JSON file
                bfn_all_biome_files_weights_c, bfn_all_tile_types_c, bfn_all_valid_start_planets_c, bfn_valid_purple_moon_biomes_planets_c, bfn_valid_giant_planet_biomes_c, all_biome_tile_types_c = self.import_from_json(json_file_path)
                # set default values
                if replace_missing_vars_w_json: # True
                    if missing_var_a:
                        self.controller.set_bfn_all_biome_files_weights(bfn_all_biome_files_weights_c)
                    if missing_var_b:
                        self.controller.set_bfn_all_tile_types(bfn_all_tile_types_c)
                    if missing_var_c:
                        self.controller.set_all_biome_tile_types(all_biome_tile_types_c)
                    self.controller.set_bfn_all_valid_start_planets(bfn_all_valid_start_planets_c) # replace regardless
                    self.controller.set_bfn_valid_purple_moon_biomes(bfn_valid_purple_moon_biomes_planets_c)
                    self.controller.set_bfn_valid_giant_planet_biomes(bfn_valid_giant_planet_biomes_c)


                else: # False - replace ALL
                    self.controller.set_bfn_all_biome_files_weights(bfn_all_biome_files_weights_c)
                    self.controller.set_bfn_all_tile_types(bfn_all_tile_types_c)
                    self.controller.set_bfn_all_valid_start_planets(bfn_all_valid_start_planets_c)
                    self.controller.set_bfn_valid_purple_moon_biomes(bfn_valid_purple_moon_biomes_planets_c)
                    self.controller.set_bfn_valid_giant_planet_biomes(bfn_valid_giant_planet_biomes_c)
                    self.controller.set_all_biome_tile_types(all_biome_tile_types_c)

                # refresh for any recently modified imported data
                bfn_all_biome_files_weights = self.controller.get_bfn_all_biome_files_weights()
                bfn_all_tile_types = self.controller.get_bfn_all_tile_types()
                bfn_all_valid_start_planets = self.controller.get_bfn_all_valid_start_planets()
                bfn_valid_purple_moon_biomes_planets = self.controller.get_bfn_valid_purple_moon_biomes() # worlds pt II
                bfn_valid_giant_planet_biomes = self.controller.get_bfn_valid_giant_planet_biomes()
                all_biome_tile_types = self.controller.get_all_biome_tile_types() # **each** biome file


            # check if user ignored error message when importing
            if len(bfn_all_biome_files_weights) < 17:
                response = messagebox.askyesno(self.langs[self.lan]["export_script"]["error_missing_16_title"], self.langs[self.lan]["export_script"]["error_missing_16_desc"], parent=self.window)
                if not response:
                    return
                else:
                    default_bfn_folder_dir = self.controller.get_default_bfn_folder_dir()
                    json_file_path = os.path.abspath(os.path.join(default_bfn_folder_dir, 'default_bfn_and_biomes.json'))

                    # verify that the '_BIOMES Xmls Folder Goes Here' directory exists
                    if not os.path.exists(default_bfn_folder_dir):
                        messagebox.showerror("Error", f"{self.langs[self.lan]["export_script"]["missing_dir_pt1"]}{default_bfn_folder_dir}{self.langs[self.lan]["export_script"]["missing_dir_pt2"]}", parent=self.window)
                        return

                    if not os.path.isfile(json_file_path):
                        messagebox.showerror("Error", f"{self.langs[self.lan]["export_script"]["missing_json_pt1"]}{json_file_path}{self.langs[self.lan]["export_script"]["missing_json_pt2"]}", parent=self.window)
                        return

                    # import data from JSON file
                    bfn_all_biome_files_weights, bfn_all_tile_types, bfn_all_valid_start_planets, bfn_valid_purple_moon_biomes_planets, bfn_valid_giant_planet_biomes, all_biome_tile_types = self.import_from_json(json_file_path)
                    # set default values
                    self.controller.set_bfn_all_biome_files_weights(bfn_all_biome_files_weights)
                    self.controller.set_bfn_all_tile_types(bfn_all_tile_types)
                    self.controller.set_bfn_all_valid_start_planets(bfn_all_valid_start_planets)
                    self.controller.set_bfn_valid_purple_moon_biomes(bfn_valid_purple_moon_biomes_planets)
                    self.controller.set_bfn_valid_giant_planet_biomes(bfn_valid_giant_planet_biomes)
                    self.controller.set_all_biome_tile_types(all_biome_tile_types)

                    if not self.open_export_window_and_wait:
                        messagebox.showinfo(self.langs[self.lan]["export_script"]["export_info_title"], self.langs[self.lan]["export_script"]["export_info_desc"], parent=self.window)

            else:
                if not self.open_export_window_and_wait:
                    messagebox.showinfo(self.langs[self.lan]["export_script"]["export_info_title"], self.langs[self.lan]["export_script"]["export_info_desc"], parent=self.window)

            #self.root.withdraw()
            plumgen_view_gen_export = PlumgenViewGenExport(
                self.root,
                self.window,
                biomes_objs,
                bfn_all_biome_files_weights,
                bfn_all_valid_start_planets,
                bfn_valid_purple_moon_biomes_planets, # worlds pt II
                bfn_valid_giant_planet_biomes,
                bfn_all_tile_types,
                all_biome_tile_types,
                self.icon_path,
                self.langs,
                self.lan,
                self.open_export_window_and_wait,
                self.checked_mbc_update_already,
                self.apply_export_settings
            )

            self.root.wait_window(plumgen_view_gen_export.window)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def apply_export_settings(self, bfn_all_biome_files_weights_c, bfn_all_valid_start_planets_c, bfn_valid_purple_moon_biomes_planets_c, bfn_valid_giant_planet_biomes_c, bfn_all_tile_types_c, all_biome_tile_types_c, checked_mbc_update_already):
        try:
            self.controller.set_bfn_all_biome_files_weights(bfn_all_biome_files_weights_c)
            self.controller.set_bfn_all_tile_types(bfn_all_tile_types_c)
            self.controller.set_bfn_all_valid_start_planets(bfn_all_valid_start_planets_c)
            self.controller.set_bfn_valid_purple_moon_biomes(bfn_valid_purple_moon_biomes_planets_c)
            self.controller.set_bfn_valid_giant_planet_biomes(bfn_valid_giant_planet_biomes_c)
            self.controller.set_all_biome_tile_types(all_biome_tile_types_c)
            self.checked_mbc_update_already = checked_mbc_update_already
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    # called when the Toplevel window is closed
    def on_close(self):
        try:
            if messagebox.askyesno(self.langs[self.lan]["on_close"]["close_title"], self.langs[self.lan]["on_close"]["close_desc"], parent=self.window):
                self.root.destroy()
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
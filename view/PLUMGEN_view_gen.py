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

class PlumgenViewGen:
    #def __init__(self, parent):
    def __init__(self, root, controller):

        self.logger = logging.getLogger(__name__)  #set up logging

        try:
                
            self.root = root # store the root window reference
            self.controller = controller # configure window

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
            # get default model filepaths lists on start
            self.dist_model_list = self.controller.get_dist_list()
            self.landm_model_list = self.controller.get_landm_list()
            self.objs_model_list = self.controller.get_objs_list()
            self.detail_model_list = self.controller.get_detail_list()

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
                self.export_script_button, self.save_rename_biome_button
            ]

            self.attribute_labels = ["Filename: ", "Placement: ", "MinHeight: ", "MaxHeight: ", "MinAngle: ", "MaxAngle: ",
                        "MinScale: ", "MaxScale: ", "MinScaleY: ", "MaxScaleY: ", "PatchEdgeScaling: ",
                        "MaxXZRotation: ", "DestroyedByPlayerShip: ", "DestroyedByTerrainEdit: ",
                        "CreaturesCanEat: ", "Coverage: ", "FlatDensity: ", "SlopeDensity: ", "SlopeMultiplier: ", "DrawDistance: ", "TotalCountInTemplate: "]
            
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
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    def show_error_message(self, message, max_length=200):
        if len(message) > max_length:
            truncated_message = message[:max_length] + "..."
        else:
            truncated_message = message
        messagebox.showerror("Error", f"{truncated_message}\n\nIf you're struggling to resolve this error, please share the 'plumgen.log' file with the dev.", parent=self.window)


    def display_splash(self):
        # splash screen
        self.splash = tk.Toplevel(self.root)
        self.splash.title("Loading...")
        self.splash.geometry(f"400x225") # set size # 550x309
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
        self.filemenu.add_command(label='Make Biome Template from EXML', command=self.make_template_from_exml)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Auto-Rename All Biomes', command=self.auto_rename_biomes)
        self.filemenu.add_command(label='Reset Auto-Rename', command=self.reset_rename_biomes)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.on_close)

        self.presetsmenu = tk.Menu(self.mb)
        self.presetsmenu.add_command(label='Save Biome as Preset', command=self.save_biome_preset)
        self.presetsmenu.add_command(label='Import Biome Preset', command=self.open_presets)

        self.toolsmenu = tk.Menu(self.mb)
        self.toolsmenu.add_command(label='Bulk Edit Menu', command=self.bulk_edit_menu)
        self.toolsmenu.add_command(label='Refresh Suggested Props', command=self.refresh_suggested_props)

        self.editmenu = tk.Menu(self.mb)
        self.editmenu.add_command(label='Help', command=self.open_help)
        self.editmenu.add_command(label='About...', command=self.open_about)

        self.donatemenu = tk.Menu(self.mb)
        self.donatemenu.add_command(label='Open Donate Page', command=lambda: webbrowser.open_new("https://www.buymeacoffee.com/sunnysummit"))

        self.mb.add_menu('File', self.filemenu)
        self.mb.add_menu('Presets', self.presetsmenu)
        self.mb.add_menu('Tools', self.toolsmenu)
        self.mb.add_menu('Help', self.editmenu)
        self.mb.add_menu('Donate', self.donatemenu)

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
        self.biome_add_button = ttk.Button(self.window, text="Add Biome", command=self.add_default_biome, style='Gen.TButton')
        self.biome_delete_button = ttk.Button(self.window, text="Delete", command=self.delete_biome, style='Delete.TButton')
        self.distant_objects_add_button = ttk.Button(self.window, text="Add Distant Object", command=self.add_default_distant_object, style='Gen.TButton')
        self.distant_objects_delete_button = ttk.Button(self.window, text="Delete", command=self.delete_distant_object, style='Delete.TButton')
        self.landmark_add_button = ttk.Button(self.window, text="Add Landmark", command=self.add_default_landmark, style='Gen.TButton')
        self.landmark_delete_button = ttk.Button(self.window, text="Delete", command=self.delete_landmark, style='Delete.TButton')
        self.objects_add_button = ttk.Button(self.window, text="Add Object", command=self.add_default_object, style='Gen.TButton')
        self.objects_delete_button = ttk.Button(self.window, text="Delete", command=self.delete_object, style='Delete.TButton')
        self.detail_objects_add_button = ttk.Button(self.window, text="Add Detail Object", command=self.add_default_detail_object, style='Gen.TButton')
        self.detail_objects_delete_button = ttk.Button(self.window, text="Delete", command=self.delete_detail_object, style='Delete.TButton')
        # other buttons
        #self.auto_rename_biomes_button = ttk.Button(self.window, text="Auto Rename All", command=self.auto_rename_biomes, style='Start.TButton')
        #self.reset_auto_names_biomes_button = ttk.Button(self.window, text="Reset Rename", command=self.reset_rename_biomes, style='TButton')
        self.save_rename_biome_button = ttk.Button(self.window, text="Rename", command=self.save_renamed_biome, style='Gen.TButton')
        self.duplicate_biome_button = ttk.Button(self.window, text="Duplicate Selected Biome", command=self.duplicate_selected_biome, width=40) # width so text not scrunched
        #self.save_biome_preset_button = ttk.Button(self.window, text="Save Biome as Preset", command=self.save_biome_preset, style='Gen.TButton')
        self.duplicate_prop_button = ttk.Button(self.window, text="Duplicate Selected Prop", command=self.duplicate_selected_prop, width=50)
        #self.open_presets_button = ttk.Button(self.window, text="Import Biome Preset", command=self.open_presets, style='Gen.TButton')
        #self.import_lua_button = ttk.Button(self.window, text="Import LUA Scripts", command=self.import_lua_biomes, style='Start.TButton')
        self.import_exml_button = ttk.Button(self.window, text="Import EXMLs/Merge Biomes", command=self.import_exml_biomes, style='Start.TButton')
        #self.make_template_from_exml_button = ttk.Button(self.window, text="Make Biome Template from EXML", command=self.make_template_from_exml, style='Gen.TButton')
        self.export_script_button = ttk.Button(self.window, text="Continue >>", command=self.export_script, style='Start.TButton', width=20)
        #self.refresh_suggested_props_button = ttk.Button(self.window, text="Refresh Suggested Props", command=self.refresh_suggested_props, style='Gen.TButton')
        self.save_prop_changes_button = ttk.Button(self.window, text="Save", width=5, command=self.save_prop_changes)
        self.increment_prop_changes_button = ttk.Button(self.window, text="↑", width=2, command=self.increment_prop_changes, style='Start.TButton')
        self.decrement_prop_changes_button = ttk.Button(self.window, text="↓", width=2, command=self.decrement_prop_changes, style='Gen.TButton')
        #self.bulk_edit_button = ttk.Button(self.window, text="Bulk Edit Menu", command=self.bulk_edit_menu, style='Start.TButton')
        self.save_model_choice_button = ttk.Button(self.window, text="Save Model", command=self.save_model_choice, style='Gen.TButton')
        self.save_placem_choice_button = ttk.Button(self.window, text="Save Placem", command=self.save_placem_choice, style='Gen.TButton')
        #self.deselect_all_props_button = ttk.Button(self.window, text="Deselect All Props", command=self.deselect_all_props, style='TButton')

        # entry
        self.rename_biome_entry = ttk.Entry(self.window, style='TEntry')
        self.attribute_entry = ttk.Entry(self.window, style='TEntry', font=('TkDefaultFont', 12), width=15)

        # text
        self.model_info = tk.Text(self.window, bg='#444444', fg=self.white_c, wrap=tk.WORD, width=30, height=5)

        # combobox
        self.csv_var = tk.StringVar(value="_Current Vanilla+Pre NMS.csv")
        self.csv_combo = ttk.Combobox(self.window, textvariable=self.csv_var, style='TCombobox', state="readonly", width=30)

        # separators
        self.separator1 = ttk.Separator(self.window, orient="horizontal")
        self.separator2 = ttk.Separator(self.window, orient="vertical")
        self.separator3 = ttk.Separator(self.window, orient="vertical")
        self.separator4 = ttk.Separator(self.window, orient="vertical")

        # labels
        self.biome_label = ttk.Label(self.window, text=" Biome Objects List ", style="TitleLabel.TLabel", wraplength=200, justify=tk.CENTER)
        self.biome_props_label = ttk.Label(self.window, text=" Biome Props ", style="TitleLabel.TLabel", wraplength=200, justify=tk.CENTER)
        self.prop_attribute_label = ttk.Label(self.window, text=" Prop Attributes ", style="TitleLabel.TLabel", wraplength=200, justify=tk.CENTER)
        self.prop_modify_attribute_label = ttk.Label(self.window, text=" Modify Attribute ", style="TitleLabel.TLabel", wraplength=200, justify=tk.CENTER)
        self.model_label = ttk.Label(self.window, text=" Default Model List ", style="Title2Label.TLabel", wraplength=300, justify=tk.CENTER)
        self.related_props_label = ttk.Label(self.window, text="Suggested Props (click to replace)", style="Title2Label.TLabel", justify=tk.CENTER)
        self.attribute_desc_label = ttk.Label(self.window, text="Attribute Description", style="Title2Label.TLabel", wraplength=200, justify=tk.CENTER)
        self.placement_label = ttk.Label(self.window, text="Default Placement List", style="Title2Label.TLabel", wraplength=250, justify=tk.CENTER)
        self.biome_template_label = ttk.Label(self.window, text="Biome Template: ", style="TLabel", wraplength=200)
        # tooltip
        self.tooltip_label = ttk.Label(self.window, text="Click 'Add Biome' to get started.", style="TLabel", wraplength=220, width=40)

        # checkboxes
        self.hide_tooltip_var = tk.BooleanVar(value=False)
        self.hide_tooltip_cb = ttk.Checkbutton(self.window, text="Hide Tooltip", variable=self.hide_tooltip_var, command=self.toggle_tooltip) #, width=40
        self.gen_using_template_data_var = tk.BooleanVar(value=False)
        self.gen_using_template_data_cb = ttk.Checkbutton(self.window, text="Add via Template Data", variable=self.gen_using_template_data_var, command=self.gen_using_biome_template_data)
        self.replace_lb_with_template_data_var = tk.BooleanVar(value=False)
        self.replace_lb_with_template_data_cb = ttk.Checkbutton(self.window, text="Use Template Placements/Models", variable=self.replace_lb_with_template_data_var, command=self.use_template_placem_models)


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
            self.biome_lb: "> Biome Objects List:\nEach biome represents a potential \"spawning point\" on a given planet (e.g. mountains, base, beach, etc. terrain-- you will pick this later). For instance, you might keep biome prop density low if you want to combine multiple biomes on a single planet.",
            self.distant_objects_lb: "> Distant Objects:\nProps with the highest draw distance and largest scale. The more props in this category, the lower the performance.",
            self.landmarks_lb: "> Landmarks:\nProps with higher draw distance and medium to large scale.\ne.g. vanilla-sized trees.",
            self.objects_lb: "> Objects:\nProps with lower draw distance and smaller scale.\ne.g. vanilla-sized rocks, bushes.",
            self.detail_objects_lb: "> Detail Objects:\nProps with the lowest draw distance and smallest scale.\ne.g. vanilla-sized grass, small plants. For reference, this category holds the highest number of props in the vanilla game.",
            #self.prop_attributes_lb: "Prop attributes:\nModify selected prop attributes like density or scale. Click on an attribute to view more info under 'Attribute Info'",
            self.biome_template_label: "> Biome Template:\nA giant collection of 'Object Spawn Data' from biome .MBIN files. Clicking any 'Add' button will create a new biome (or prop) based on the currently selected template. Click File > Make Biome Template from EXML to create your own biome template.",
            self.csv_combo: "> Biome Template:\nA giant collection of 'Object Spawn Data' from biome .MBIN files. Clicking any 'Add' button will create a new biome (or prop) based on the currently selected template. Click File > Make Biome Template from EXML to create your own biome template.",
            self.gen_using_template_data_cb: "Uses selected biome template model filepaths as the key when adding new biomes/props via 'Add' buttons. If left off, it still uses the .CSV data but sticks to a standard model filepath list for the key. It will not add props to Biome Props list if none are found.",
            #self.refresh_suggested_props_button: "These model reference counts (numbers inside []) don't affect your biomes whatsoever, but are meant to help you decide what props to add (based on the selected biome template). Additionally, these are saved with the JSON file when clicking 'Save Biome as Preset'.",  
            self.import_exml_button: "Analyze EXML files in your '_BIOMES Exmls Folder Goes Here' folder and convert to PLUMGEN's format. \n\n*To merge biome lists* FIRST, move all BIOMES folders to BEFGH, THEN import.",
            self.model_lb: "Props after '--' line are pre-release models or models normally in a different prop draw distance category. They've been moved here to extend the draw distance for those props (e.g. some props don't have LOD imposters, so you could move those to Distant Objects). ",
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
        self.export_script_button.grid(row=1, column=9, columnspan=1, rowspan = 2, padx=20, pady=5, sticky=tk.EW)
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
    

    def open_help(self):
        try:
                
            help_window = tk.Toplevel(self.window)
            help_window.title("Help")
            parent_x = self.window.winfo_rootx()
            parent_y = self.window.winfo_rooty()
            help_window.geometry(f"+{parent_x}+{parent_y}")
            help_window.grab_set()  # prevent this window from going behind main window

            label = tk.Label(help_window, text="To read documentation, please visit: ")
            label.grid(row=0, column=0, padx=10, pady=10)
            link_label = tk.Label(help_window, text="https://github.com/SunnySummit", fg="blue", cursor="hand2")
            link_label.grid(row=1, column=0, padx=10, pady=5)
            link_label.bind("<Button-1>", lambda event: webbrowser.open_new("https://github.com/SunnySummit"))

            close_button = tk.Button(help_window, text="Close", command=help_window.destroy)
            close_button.grid(row=2, column=0, pady=10)

            help_window.mainloop()

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    def open_about(self):
        try:
                
            messagebox.showinfo("About PLUMGEN", f"Author: SunnySummit aka goosetehmoose"
                                "\nWebsite: https://github.com/SunnySummit"
                                "\nLicense: GPL-3.0"
                                "\n\nI kindly ask that you do not distribute this application "
                                "for use in other Hello Games-related projects or games other than No Man's Sky.", parent=self.window)

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
            self.tooltip_label.config(text="Click 'Add Biome' to get started.")
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
                if selected_csv != "_Current Vanilla+Pre NMS.csv":
                    result = messagebox.askyesno("Warning: Generating using Custom Models", "It seems you're using a custom biome template (not '_Current Vanilla+Pre NMS.csv')."
                                            "\n\nThis could indicate that your custom .CSV refers to outdated or broken models, which might cause issues with your mod."
                                            "\n\nYou'll also need a PAK of the custom models for them to show up in-game."
                                            "\n\nDo you want to proceed?", parent=self.window)
                    if not result:
                        self.gen_using_template_data_var.set(False)
                        return
                else: messagebox.showinfo("Info: Generation Switched", "'Add Using Template Model' Checkbox checked.\n Switching to '_Current Vanilla+Pre NMS.csv' generation.", parent=self.window)
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
                    if distant_obj_list[0]:  # verify that the model filepath is not empty
                        self.update_listbox(self.distant_objects_lb, distant_obj_list[20], distant_obj_list[0])
                for landmark_list in selected_biome.get_landmark_lists():
                    if landmark_list[0]:
                        self.update_listbox(self.landmarks_lb, landmark_list[20], landmark_list[0])
                for objects_list in selected_biome.get_objects_lists():
                    if objects_list[0]:
                        self.update_listbox(self.objects_lb, objects_list[20], objects_list[0])
                for detail_obj_list in selected_biome.get_detail_obj_lists():
                    if detail_obj_list[0]:
                        self.update_listbox(self.detail_objects_lb, detail_obj_list[20], detail_obj_list[0])
                
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
            if label != "TotalCountInTemplate: ": 
                display_text = f"{label}{item}"
                self.prop_attributes_lb.insert(tk.END, display_text)
            # select items in listboxes
            if label == "Filename: ":
                self.select_and_highlight_item(self.model_lb, self.dist_model_list, item)
            elif label == "Placement: ":
                self.select_and_highlight_item(self.placement_lb, self.placement_list, item)
            elif label == "TotalCountInTemplate: ": # find this prop (up to 20th index) in prop's list of similar_items
                self.select_and_highlight_item(self.similar_props_lb, self.prop_distant[20], self.prop_distant[:20]) # item
                display_text = f"{label}{len(item)}" # display similar items count
                self.prop_attributes_lb.insert(tk.END, display_text)

        self.placem_val_at_index = None #reset selected placement/models
        self.model_val_at_index = None 
        self.attribute_entry.delete(0, 'end')

    def refresh_landmark_attr_placem_models(self):

        self.prop_attributes_lb.delete(0, tk.END)

        for label, item in zip(self.attribute_labels, self.prop_landmark):
            if label != "TotalCountInTemplate: ": 
                display_text = f"{label}{item}"
                self.prop_attributes_lb.insert(tk.END, display_text)
            # select items in listboxes
            if label == "Filename: ":
                self.select_and_highlight_item(self.model_lb, self.landm_model_list, item)
            elif label == "Placement: ":
                self.select_and_highlight_item(self.placement_lb, self.placement_list, item)
            elif label == "TotalCountInTemplate: ": # find this prop (up to 20th index) in prop's list of similar_items
                self.select_and_highlight_item(self.similar_props_lb, self.prop_landmark[20], self.prop_landmark[:20]) # item
                display_text = f"{label}{len(item)}" # display similar items count
                self.prop_attributes_lb.insert(tk.END, display_text)

        self.placem_val_at_index = None #reset selected placement/models
        self.model_val_at_index = None 
        self.attribute_entry.delete(0, 'end')

    def refresh_object_attr_placem_models(self):

        self.prop_attributes_lb.delete(0, tk.END)

        for label, item in zip(self.attribute_labels, self.prop_object):
            if label != "TotalCountInTemplate: ": 
                display_text = f"{label}{item}"
                self.prop_attributes_lb.insert(tk.END, display_text)
            # select items in listboxes
            if label == "Filename: ":
                self.select_and_highlight_item(self.model_lb, self.objs_model_list, item)
            elif label == "Placement: ":
                self.select_and_highlight_item(self.placement_lb, self.placement_list, item)
            elif label == "TotalCountInTemplate: ": # find this prop (up to 20th index) in prop's list of similar_items
                self.select_and_highlight_item(self.similar_props_lb, self.prop_object[20], self.prop_object[:20]) # item
                display_text = f"{label}{len(item)}" # display similar items count
                self.prop_attributes_lb.insert(tk.END, display_text)

        self.placem_val_at_index = None #reset selected placement/models
        self.model_val_at_index = None 
        self.attribute_entry.delete(0, 'end')

    def refresh_detail_attr_placem_models(self):

        self.prop_attributes_lb.delete(0, tk.END)

        for label, item in zip(self.attribute_labels, self.prop_detail):
            if label != "TotalCountInTemplate: ": 
                display_text = f"{label}{item}"
                self.prop_attributes_lb.insert(tk.END, display_text)
            # select items in listboxes
            if label == "Filename: ":
                self.select_and_highlight_item(self.model_lb, self.detail_model_list, item)
            elif label == "Placement: ":
                self.select_and_highlight_item(self.placement_lb, self.placement_list, item)
            elif label == "TotalCountInTemplate: ": # find this prop (up to 20th index) in prop's list of similar_items
                self.select_and_highlight_item(self.similar_props_lb, self.prop_detail[20], self.prop_detail[:20]) # item
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
                for matching_prop in self.prop_distant[20]:
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
                for matching_prop in self.prop_landmark[20]:
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
                for matching_prop in self.prop_object[20]:
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
                for matching_prop in self.prop_detail[20]:
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
                    0: "Model path.",
                    1: "Tile type affecting prop placement spacing. Be sure to use distinct placement, coverage, or density values per prop in a biome to prevent overlapping props. If 'X' in the name, it might be deactivated and may not spawn.",
                    2: "Lowest spawn height relative to sea level. Note: For props in 'Underwater' tile types/terrain, set this to -128 so they spawn correctly.",
                    3: "Highest spawn height.",
                    4: "Min terrain angle at which the prop will spawn. 180 = all angles -> lowers performance because more props.",
                    5: "Max terrain angle at which the prop will spawn. 180 = all angles -> lowers performance because more props.",
                    6: "Smallest scale for an instance of a prop to spawn on a biome. Large range = extremely varied prop scale on a biome.",
                    7: "Largest scale for an instance of a prop to spawn on a biome. Large range = extremely varied prop scale on a biome.",
                    8: "Min height scale for an instance of a prop to spawn on a biome. Mostly used for detail objects, as this value will distort large props.",
                    9: "Max height scale for an instance of a prop to spawn on a biome. Mostly used for detail objects, as this value will distort large props.",
                    10: "Scale variation at edges of a group of spawned props. Typically applied to high-density detail objects like grass to add a scale transition from grass to dirt/beach/etc. Not recommended with large or low-density props -> spawns highly erratic scale variations. Instead, use MinScale and MaxScale.",
                    11: "Maximum rotation of a spawned prop around the X and Z axes. Limits range of vertical rotation.",
                    12: "Player's ship impact on prop destruction. Note: Players may get stuck on planets after takeoff due to huge, unbreakable props.",
                    13: "Terrain manipulator impact on prop destruction.",
                    14: "/ᐠ⎚-⎚マ",
                    15: "AFAIK impact on spacing/grouping of props, not total number of props. Changing placement is usually more useful than changing coverage, imo. Note: High coverage e.g. 1 = crash.",
                    16: "Density of props on flat terrain, useful for dense forests. Always check placement attribute, high density + densely grouped prop placement = crash.",
                    17: "Density of props on sloped terrain. Note: spawning huge props on sloped terrain = issue where these props \"despawn\" as you approach. Always check placement attribute, high density + densely grouped prop placement = crash.",
                    18: "Density multiplier of props on sloped terrain.",
                    19: "DrawDistance from biome template .CSV file, may not necessarily represent draw distance of your prop. Note: These categories are hardcoded, meaning some props may not spawn if moved to a category other than vanilla one.",
                    20: "Total model references in selected biome template. If you change biome template, click Tools > Refresh Suggested Props to update suggestions."
                }

                # get description based on attribute index
                new_desc = attribute_descriptions.get(self.prop_attribute_index, "Error: Attribute index out of range.")

                self.describe_attribute(new_desc)

                # insert prop attribute depending on prop draw distance type
                if self.prop_draw_type == 1:
                    self.attribute_entry.config(state="normal") # enable if can set via entry
                    self.save_prop_changes_button.config(state=tk.NORMAL)
                    self.attribute_entry.delete(0, tk.END)
                    # don't insert some items (either put these in listbox or they can't be modified)
                    if self.prop_attribute_index != 0 and self.prop_attribute_index != 1 and self.prop_attribute_index != 19 and self.prop_attribute_index != 20:
                        self.attribute_entry.insert(0, self.prop_distant[self.prop_attribute_index])
                    else:
                        self.attribute_entry.insert(0, "N/A")
                        self.attribute_entry.config(state="disabled") # disable if can't set via entry 
                        self.save_prop_changes_button.config(state=tk.DISABLED)
                elif self.prop_draw_type == 2:
                    self.attribute_entry.config(state="normal") # enable if can set via entry
                    self.save_prop_changes_button.config(state=tk.NORMAL)
                    self.attribute_entry.delete(0, tk.END)
                    if self.prop_attribute_index != 0 and self.prop_attribute_index != 1 and self.prop_attribute_index != 19 and self.prop_attribute_index != 20:
                        self.attribute_entry.insert(0, self.prop_landmark[self.prop_attribute_index])
                    else:
                        self.attribute_entry.insert(0, "N/A")
                        self.attribute_entry.config(state="disabled")
                        self.save_prop_changes_button.config(state=tk.DISABLED)
                elif self.prop_draw_type == 3:
                    self.attribute_entry.config(state="normal") # enable if can set via entry
                    self.save_prop_changes_button.config(state=tk.NORMAL)
                    self.attribute_entry.delete(0, tk.END)
                    if self.prop_attribute_index != 0 and self.prop_attribute_index != 1 and self.prop_attribute_index != 19 and self.prop_attribute_index != 20:
                        self.attribute_entry.insert(0, self.prop_object[self.prop_attribute_index])
                    else:
                        self.attribute_entry.insert(0, "N/A")
                        self.attribute_entry.config(state="disabled")
                        self.save_prop_changes_button.config(state=tk.DISABLED)
                elif self.prop_draw_type == 4:
                    self.attribute_entry.config(state="normal") # enable if can set via entry 
                    self.save_prop_changes_button.config(state=tk.NORMAL)
                    self.attribute_entry.delete(0, tk.END)
                    if self.prop_attribute_index != 0 and self.prop_attribute_index != 1 and self.prop_attribute_index != 19 and self.prop_attribute_index != 20:
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
                self.model_info.insert(tk.END, "Probably a custom placement value. Look for SPAWNDENSITYLIST.MBIN in the modded MBINs to locate this info. "
                                    "'X' in the name might indicate this placement prevents this prop from spawning.")

            else:
                self.model_info.delete("1.0", tk.END)
                self.model_info.insert(tk.END, self.placem_val_at_index + ":\n")
                self.model_info.insert(tk.END, "Probably a custom placement value. Look for SPAWNDENSITYLIST.MBIN in the modded MBINs to locate this info.")

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
            
                result = messagebox.askyesno("Replace?", "\nReplace the current prop with the suggested prop?", parent=self.window)
                if not result:
                    return

                similar_prop_index = self.similar_props_lb.nearest(event.y)
                selected_biome = self.controller.get_biome_objs()[self.biome_index]

                self.model_info.delete("1.0", tk.END)

                # proceed with attribute replacement
                if self.prop_draw_type == 1:
                    replacement_prop = self.prop_distant[20][similar_prop_index]
                    for index, replacement_attr in enumerate(replacement_prop):
                        copied_item = copy.deepcopy(replacement_attr) # deep copy because the copied item is mutable
                        selected_biome.set_custom_distant_attr(self.distant_index, index, copied_item)

                    self.refresh_distant_attr_placem_models()

                elif self.prop_draw_type == 2:
                    replacement_prop = self.prop_landmark[20][similar_prop_index]
                    for index, replacement_attr in enumerate(replacement_prop):
                        copied_item = copy.deepcopy(replacement_attr)
                        selected_biome.set_custom_landmark_attr(self.landmark_index, index, copied_item)

                    self.refresh_landmark_attr_placem_models()

                elif self.prop_draw_type == 3:
                    replacement_prop = self.prop_object[20][similar_prop_index]
                    for index, replacement_attr in enumerate(replacement_prop):
                        copied_item = copy.deepcopy(replacement_attr)
                        selected_biome.set_custom_object_attr(self.obj_index, index, copied_item)

                    self.refresh_object_attr_placem_models()

                elif self.prop_draw_type == 4:
                    replacement_prop = self.prop_detail[20][similar_prop_index]
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
                        selected_biome.set_custom_distant_attr(self.distant_index, 0, self.model_val_at_index)
                        
                        self.refresh_distant_attr_placem_models()

                        self.distant_objects_lb.delete(0, tk.END)
                        for distant_obj_list in selected_biome.get_distant_obj_lists():
                            if distant_obj_list[0]:  # verify that the model filepath is not empty
                                self.update_listbox(self.distant_objects_lb, distant_obj_list[20], distant_obj_list[0])
                    elif self.prop_draw_type == 2:
                        selected_biome.set_custom_landmark_attr(self.landmark_index, 0, self.model_val_at_index)
                        
                        self.refresh_landmark_attr_placem_models()

                        self.landmarks_lb.delete(0, tk.END)
                        for landmark_list in selected_biome.get_landmark_lists():
                            if landmark_list[0]:
                                self.update_listbox(self.landmarks_lb, landmark_list[20], landmark_list[0])
                    elif self.prop_draw_type == 3:
                        selected_biome.set_custom_object_attr(self.obj_index, 0, self.model_val_at_index)
                        
                        self.refresh_object_attr_placem_models()

                        self.objects_lb.delete(0, tk.END)
                        for objects_list in selected_biome.get_objects_lists():
                            if objects_list[0]:
                                self.update_listbox(self.objects_lb, objects_list[20], objects_list[0])
                    elif self.prop_draw_type == 4:
                        selected_biome.set_custom_detail_attr(self.detail_index, 0, self.model_val_at_index)
                        
                        self.refresh_detail_attr_placem_models()

                        self.detail_objects_lb.delete(0, tk.END)
                        for detail_obj_list in selected_biome.get_detail_obj_lists():
                            if detail_obj_list[0]:
                                self.update_listbox(self.detail_objects_lb, detail_obj_list[20], detail_obj_list[0])

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
                        selected_biome.set_custom_distant_attr(self.distant_index, 1, self.placem_val_at_index)
                        
                        self.refresh_distant_attr_placem_models()

                    elif self.prop_draw_type == 2:
                        selected_biome.set_custom_landmark_attr(self.landmark_index, 1, self.placem_val_at_index)
                        
                        self.refresh_landmark_attr_placem_models()

                    elif self.prop_draw_type == 3:
                        selected_biome.set_custom_object_attr(self.obj_index, 1, self.placem_val_at_index)
                        
                        self.refresh_object_attr_placem_models()

                    elif self.prop_draw_type == 4:
                        selected_biome.set_custom_detail_attr(self.detail_index, 1, self.placem_val_at_index)
                        
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
                
            result = messagebox.askyesno("Warning", "This will overwrite suggested props for all your biomes (based on the selected biome template)."
                                    "\n\nDo you want to proceed?", parent=self.window)
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
        if index in {2, 3, 4, 5, 11}:
            if not isinstance(new_val, int):
                messagebox.showinfo("Error", f"{self.attribute_labels_edited[index]} must be an integer.", parent=self.window)
                return
        elif index in {6, 7, 8, 9, 10, 15, 16, 17, 18}:
            if not isinstance(new_val, numbers.Number):
                messagebox.showinfo("Error", f"{self.attribute_labels_edited[index]} must be a number.", parent=self.window)
                return
        elif index in {12, 13, 14}:
            if new_val not in {"TRUE", "FALSE"}:
                messagebox.showinfo("Error", f"{self.attribute_labels_edited[index]} must be either 'TRUE' or 'FALSE'.", parent=self.window)
                return
        else:
            messagebox.showinfo("Error 0", f"Did you add a new index? Index '{index}' out of range?", parent=self.window)
            return
        
        if set_val:
            # apply modified value if no errors found
            if index >= 2 and index <= 18:

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
                messagebox.showinfo("Error 1", f"Index '{index}' out of range.", parent=self.window)
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
                    messagebox.showerror("Error", "Modified value must only contain numbers, letters,\nor characters: '.' or '-'"
                                        "\n\nIf trying to multiply, remove empty spaces, e.g. 4*2", parent=self.window)

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
                    
                    if self.prop_attribute_index >= 2 and self.prop_attribute_index <= 18:

                        if self.prop_attribute_index in {2, 3, 4, 5, 11}:
                            if not isinstance(bulk_new_value, int):
                                messagebox.showinfo("Error", f"{self.attribute_labels_edited[self.prop_attribute_index]} must be an integer.", parent=self.window)
                                return
                        elif self.prop_attribute_index in {6, 7, 8, 9, 10, 15, 16, 17, 18}:
                            if not isinstance(bulk_new_value, numbers.Number):
                                messagebox.showinfo("Error", f"{self.attribute_labels_edited[self.prop_attribute_index]} must be a number.", parent=self.window)
                                return
                        elif self.prop_attribute_index in {12, 13, 14}:
                            if bulk_new_value not in {"TRUE", "FALSE"}:
                                messagebox.showinfo("Error", f"{self.attribute_labels_edited[self.prop_attribute_index]} must be either 'TRUE' or 'FALSE'.", parent=self.window)
                                return
                        else:
                            messagebox.showinfo("Error 0", f"Did you add a new index? Index '{self.prop_attribute_index}' out of range?", parent=self.window)
                            return
                    
                        plumgen_view_gen_bulk = PlumgenViewGenBulk(self.root, bulk_new_value, selected_biome, self.attribute_labels_edited, self.prop_attribute_index, self.icon_path, self.apply_bulk_settings, multiply=True)



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
                    if self.prop_draw_type == 1 and self.prop_attribute_index >= 2 and self.prop_attribute_index <= 18:
                        bulk_val_validated = self.set_custom_attr(selected_biome, self.prop_attribute_index, bulk_new_value, False)
                    elif self.prop_draw_type == 2 and self.prop_attribute_index >= 2 and self.prop_attribute_index <= 18:
                        bulk_val_validated = self.set_custom_attr(selected_biome, self.prop_attribute_index, bulk_new_value, False)
                    elif self.prop_draw_type == 3 and self.prop_attribute_index >= 2 and self.prop_attribute_index <= 18:
                        bulk_val_validated = self.set_custom_attr(selected_biome, self.prop_attribute_index, bulk_new_value, False)
                    elif self.prop_draw_type == 4 and self.prop_attribute_index >= 2 and self.prop_attribute_index <= 18:
                        bulk_val_validated = self.set_custom_attr(selected_biome, self.prop_attribute_index, bulk_new_value, False)

                    # instantiate bulk view - display new menu
                    if bulk_val_validated:
                        if self.prop_attribute_index >= 2 and self.prop_attribute_index <= 18:
                            plumgen_view_gen_bulk = PlumgenViewGenBulk(self.root, bulk_new_value, selected_biome, self.attribute_labels_edited, self.prop_attribute_index, self.icon_path, self.apply_bulk_settings)
                    
                    # if model selected - attempt to get cursor selection and specific model selected
                    if self.prop_attribute_index == 0:
                        selected_indices = self.model_lb.curselection()
                        if selected_indices:
                            selected_index = self.model_lb.curselection()[0]
                            if self.prop_draw_type == 1: selected_item = self.dist_model_list[selected_index]
                            elif self.prop_draw_type == 2: selected_item = self.landm_model_list[selected_index]
                            elif self.prop_draw_type == 3: selected_item = self.objs_model_list[selected_index]
                            elif self.prop_draw_type == 4: selected_item = self.detail_model_list[selected_index]
                            plumgen_view_gen_bulk = PlumgenViewGenBulk(self.root, selected_item, selected_biome, self.attribute_labels_edited, self.prop_attribute_index, self.apply_bulk_settings)
                        else:
                            messagebox.showinfo("Click Model", "Click on the model you want before selecting 'Bulk Edit Menu'", parent=self.window)
                    # if placement selected
                    if self.prop_attribute_index == 1:
                        selected_indices = self.placement_lb.curselection()
                        if selected_indices:
                            selected_index = self.placement_lb.curselection()[0]
                            selected_item = self.placement_list[selected_index]
                            plumgen_view_gen_bulk = PlumgenViewGenBulk(self.root, selected_item, selected_biome, self.attribute_labels_edited, self.prop_attribute_index, self.icon_path, self.apply_bulk_settings)
                        else:
                            messagebox.showinfo("Click Placement", "Click on the placement you want before selecting 'Bulk Edit Menu'", parent=self.window)

                else:
                    messagebox.showerror("Error", "Modified value must only contain numbers, letters,\nor characters: '.' or '-'", parent=self.window)
            else:
                messagebox.showerror("Error", "First, select an attribute for bulk editing. Then, either edit the value next to 'Save' or select a Placement or Model item.", parent=self.window)

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
                            messagebox.showerror("Error", "Invalid entry type. Please enter a string, an integer, or a float."
                                                "\n\nOtherwise, select an item from a listbox to modify it.", parent=self.window)
                    else:
                        messagebox.showerror("Error", "Empty or invalid entry type. Please enter a string, an integer, or a float."
                                                "\n\nOtherwise, select an item from a listbox to modify it.", parent=self.window)

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
                            messagebox.showerror("Error", "Invalid entry type. Please enter a string, an integer, or a float."
                                                "\n\nOtherwise, select an item from the listbox to modify it.", parent=self.window)
                    else:
                        messagebox.showerror("Error", "Empty or invalid entry type. Please enter a string, an integer, or a float."
                                                "\n\nOtherwise, select an item from the listbox to modify it.", parent=self.window)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    def gen_using_biome_template_data(self):
        try:
                    
            selected_csv = self.csv_var.get()
            # show warning if user using custom biome template .csv
            if self.gen_using_template_data_var.get():
                self.replace_lb_with_template_data_cb.config(state=tk.NORMAL)
                if selected_csv != "_Current Vanilla+Pre NMS.csv":
                    result = messagebox.askyesno("Warning: Generating using Custom Models", "It seems you're using a custom biome template (not '_Current Vanilla+Pre NMS.csv')."
                                            "\n\nThis could indicate that your custom .CSV refers to outdated or broken models, which might cause issues with your mod."
                                            "\n\nYou'll also need a PAK of the custom models for them to show up in-game."
                                            "\n\nDo you want to proceed?", parent=self.window)
                    if not result:
                        self.gen_using_template_data_var.set(False)
                        return
                # replace default model path list with list of unique models in biome template
                self.controller.set_custom_model_list()
                self.controller.set_custom_placem_list() # placements
                
                self.biome_add_button['text'] = "Add BT Biome"
                self.distant_objects_add_button['text'] = "Add BT Distant Object"
                self.landmark_add_button['text'] = "Add BT Landmark"
                self.objects_add_button['text'] = "Add BT Object"
                self.detail_objects_add_button['text'] = "Add BT Detail Object"
            else:
                if not self.replace_lb_with_template_data_var.get():
                    self.replace_lb_with_template_data_cb.config(state=tk.DISABLED) # disable next checkbox

                self.controller.set_default_model_list()
                
                self.biome_add_button['text'] = "Add Biome"
                self.distant_objects_add_button['text'] = "Add Distant Object"
                self.landmark_add_button['text'] = "Add Landmark"
                self.objects_add_button['text'] = "Add Object"
                self.detail_objects_add_button['text'] = "Add Detail Object"

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

        #----------------------------------------------------------------------------------------
        

    def use_template_placem_models(self):
        try:
                    
            selected_csv = self.csv_var.get()
            # show warning if a custom Biome Template .csv selected
            if self.replace_lb_with_template_data_var.get():

                self.model_label['text'] = "Biome Template Model List"
                self.placement_label['text'] = "Biome Template Placement List"

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

                self.model_label['text'] = " Default Model List "
                self.placement_label['text'] = " Default Placement List "
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
                
                result = messagebox.askyesno("Auto Rename Biome?",
                    "Do not rename biomes that already have custom names, "
                    "as their filenames are referenced in many files (especially in big biome gen mods). "
                    "If you change these filenames, the game will crash when attempting to spawn the renamed biomes."
                    "\n\nDo you want to proceed?", parent=self.window)
                if not result:
                    return
                
                index = self.biome_index
                new_filename = self.rename_biome_entry.get().strip()
                new_filename = re.sub(r'[^a-zA-Z0-9_\-/\\ ]', '', new_filename) # filter unwanted characters using regex
                if new_filename is not None and new_filename != "" and new_filename != " ":
                    if new_filename not in self.biome_lb.get(0, tk.END):
                        self.controller.c_rename_biome(index, new_filename)
                        self.biome_lb.delete(index)
                        self.biome_lb.insert(index, new_filename)
                    else: 
                        messagebox.showerror("Duplicate filename.", "The entered biome name is a duplicate in the list.\nPlease enter a different name.", parent=self.window)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            
    

    def auto_rename_biomes(self):
        try:
                
            if self.biome_lb.size() > 0:
                
                result = messagebox.askyesno("Auto Rename All Biomes?",
                    "This will rename biomes based on the model names in each biome.\n\n"
                    "Do not attempt this with biomes that already have custom names, "
                    "as their filenames are referenced in many files (especially in big biome gen mods). "
                    "If you change these filenames, the game will crash when attempting to spawn the renamed biomes."
                    "\n\nDo you want to proceed?", parent=self.window)
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
                
                result = messagebox.askyesno("Reset Renamed Biomes?",
                    "This truncates text after the first underscore in the biome name (or leaves it alone if no underscore found).\n\n"
                    "Do not attempt this with biomes that already have custom names, "
                    "as their filenames are referenced in many files (especially in big biome gen mods). "
                    "If you change these filenames, the game will crash when attempting to spawn the renamed biomes."
                    "\n\nDo you want to proceed?", parent=self.window)
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
    def add_default_biome(self):
        try: 
            new_biome = self.controller.c_create_default_biome()
            self.biome_lb.insert(tk.END, new_biome.get_filename())
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def delete_biome(self):
        try:
                
            if self.biome_index is not None:
                result = messagebox.askyesno("Delete Selected Biome?", "Delete biome?"
                                        "\n\nCaution: This action cannot be undone.", parent=self.window)
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
                self.update_listbox(listbox, obj_list[20], obj_list[0])
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
                selected_biome.add_objects_list()
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
                            self.update_listbox(listbox, obj_list[20], obj_list[0])
                        self.placem_val_at_index = None
                        self.model_val_at_index = None

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    # presets
    def save_biome_preset(self):
        try:
                
            if self.biome_lb.size() > 0:
                response = messagebox.askyesno("Save Biome as Preset?", "This will save the selected biome as a JSON file "
                                                "located in your '_Presets' folder. It will use the biome's name as the filename, "
                                                "potentially overwriting any existing file with the same name."
                                                "\n\nCreate preset?", parent=self.window)
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
                messagebox.showerror("Error", f"The '_Presets' directory does not exist: \n\n{presets_path}"
                                    "\n\nPlease do not delete or rename this directory.", parent=self.window)
                return
            else:
                if not os.listdir(presets_path):
                    messagebox.showerror("Error", f"The '_Presets' directory is empty: \n\n{presets_path}"
                                        "\n\nFirst, save a biome as a preset, this will save the biome as a json file.", parent=self.window)
                    return
            
            self.presets_window = tk.Toplevel(self.window) # new window to display list of JSON files
            self.presets_window.title("Biome Presets")
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
            close_button = tk.Button(self.presets_window, text="Close", command=self.presets_window.destroy)
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
        self.presetsmenu.entryconfig('Save Biome as Preset', state='disabled')
        self.presetsmenu.entryconfig('Import Biome Preset', state='disabled')
        self.filemenu.entryconfig('Auto-Rename All Biomes', state='disabled')
        self.filemenu.entryconfig('Reset Auto-Rename', state='disabled')
        self.toolsmenu.entryconfig('Bulk Edit Menu', state='disabled')
        self.toolsmenu.entryconfig('Refresh Suggested Props', state='disabled')
        
        
        loading_screen = tk.Toplevel(self.window)
        loading_screen.title("Loading...")
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
        loading_label = ttk.Label(loading_screen, text="Please wait, importing files... This could take several minutes.\n"
                                "Do not open BT .CSV files while this is running.\n", justify=tk.CENTER, style="Title3Label.TLabel")
        loading_label.grid(row=0, column=0, padx=0, pady=0)

        loading_screen.attributes("-topmost", True)
        #loading_screen.grab_set()
        loading_screen.update()
        
        return loading_screen


    def reenable_buttons(self):
        # re-enable UI elements
        for button in self.buttons:
            button.configure(state="normal")
        self.presetsmenu.entryconfig('Save Biome as Preset', state='normal')
        self.presetsmenu.entryconfig('Import Biome Preset', state='normal')
        self.filemenu.entryconfig('Auto-Rename All Biomes', state='normal')
        self.filemenu.entryconfig('Reset Auto-Rename', state='normal')
        self.toolsmenu.entryconfig('Bulk Edit Menu', state='normal')
        self.toolsmenu.entryconfig('Refresh Suggested Props', state='normal')


    def complete_import(self, loading_screen):
        # repopulate listbox with new counts
        all_biomes = self.controller.get_biome_objs()

        self.import_exml_button.configure(state="normal")
        self.reenable_buttons()

        biomes_to_delete = []
        for index, biome in enumerate(all_biomes):
            self.biome_lb.insert(tk.END, biome.get_filename())
            if "/Objects/" in biome.get_filename():
                #print("Problem biome file index:", index)
                biomes_to_delete.append(index)

        loading_screen.destroy()

        if len(biomes_to_delete) > 0:
            response = messagebox.askyesno("Issue with Biome Objects Files", f"The imported biome objects files list contains {len(biomes_to_delete)} /OBJECTS/* MBINs. "
                                "\n\nThese files may contain unique props with unique attributes, e.g. word stones, which PLUMGEN will make uninteractable."
                                "\n\nYes = Auto. remove these files for you from your Biome Objects List "
                                "so props retain unique attributes."
                                "\n\nNo = Manually remove problematic MBINS in the /OBJECTS/ folder."
                                "\n\n(If 200+ found, remove subfolders as needed before importing)", parent=self.window)
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

        if len(self.controller.get_bfn_all_biome_files_weights()) < 16:
            messagebox.showinfo("< 16 Biome Entries", 
                                "The missing or imported BIOMEFILENAMES.EXML contains less than 16 sub-biomes entries, a fixed-size array. "
                                "This happens with outdated NMS versions which supported only 10 sub-biomes."
                                "\n\n(Recommended) Fix 1: After clicking 'Export', choose 'NO' to create a vanilla canvas, then add biomes manually."
                                "\n\n(Advanced) Fix 2: Add an EXTRA up-to-date vanilla (or custom) BIOMEFILENAMES.EXML to the import folder's top-most directory. "
                                "Python will process it first, then handle the outdated BFN file, attempting a merge.", parent=self.window)
        else:
            messagebox.showinfo("Import EXML Complete", "Import EXML complete. All relevant biome data added.", parent=self.window)

        #self.controller.recount_models() # refresh model counts for selected Biome Template



    # import
        
    #def import_lua_biomes(self):
    #    pass
        

    def import_exml_biomes_threaded(self, after_next_update, loading_screen):
        self.controller.c_import_exml_biomes(after_next_update)
        self.window.after(0, lambda: self.complete_import(loading_screen))

    def import_exml_biomes(self):
        try:
                    
            biom_exmls_folder_dir = self.controller.get_biom_exmls_folder_dir()
            biomes_folder = os.path.abspath(os.path.join(biom_exmls_folder_dir, 'BIOMES'))

            # verify that the '_BIOMES Exmls Folder Goes Here' directory exists
            if not os.path.exists(biom_exmls_folder_dir):
                messagebox.showerror("Error", f"The import directory does not exist: \n\n{biom_exmls_folder_dir}"
                                    "\n\nPlease do not delete or rename this directory.", parent=self.window)
                return
            else:
                if not os.listdir(biom_exmls_folder_dir):
                    messagebox.showerror("Error", f"The import directory is empty: \n\n{biom_exmls_folder_dir}"
                                        "\n\nDecompile MBINs to EXML, then move one or more 'BIOMES' folder to this directory."
                                        "\nSee: '_Biome Templates/__template README.txt' for more info.", parent=self.window)
                    return
                else:
                    if not os.path.exists(biomes_folder): # check if 'BIOMES' folder in directory
                        response = messagebox.askyesnocancel("Question", f"No 'BIOMES' folder found in directory: \n\n{biom_exmls_folder_dir}"
                                        "\n\nThis folder contains all necessary EXML files for biome conversion into PLUMGEN data. "
                                        "Without it, data WILL be missing."
                                        "\n\n*I do not recommend importing folders other than 'BIOMES'."
                                        "\n\n*Renaming the 'BIOMES' folder may cause LUA script errors "
                                        "(ignore this if importing a renamed/modded 'BIOMES' folder)."
                                        "\n\nContinue anyway?", parent=self.window)
                        if not response:
                            return

            # check if imported already, show overwrite message if yes
            imported_variables = []
            if self.controller.get_biome_objs():  imported_variables.append("biome_objs")
            if self.controller.get_bfn_all_biome_files_weights():  imported_variables.append("bfn_all_biome_files_weights")
            if self.controller.get_bfn_all_tile_types(): imported_variables.append("bfn_all_tile_types")
            if self.controller.get_bfn_all_valid_start_planets(): imported_variables.append("bfn_all_valid_start_planets")
            if self.controller.get_all_biome_tile_types(): imported_variables.append("all_biome_tile_types")

            if imported_variables:

                response = messagebox.askyesno("Overwrite Data?", "---------------------------WARNING---------------------------\n\n"
                                                        "This will replace *ALL* your work with the newly imported EXML data. "
                                                        "\n\nIf you want to import EXML without losing your current work:"
                                                        
                                                        "\n\n(Recommended) Fix 1:\nA) For each biome objects item, click Presets > Save Biome as Preset. "
                                                        "B) Add new 'BIOMES' folder to '_BIOMES Exmls Folder Goes Here' and import EXML. "
                                                        "C) Click Presets > Import Biome Presets, and click on each file you just saved."
                                                        
                                                        "\n\n(Advanced) Fix 2:\nA) Click 'No', B) Export, "
                                                        "C) Extract EXML with AMUMSS or MBINCompiler (from PAK file), "
                                                        "D) Add (or combine) 'BIOMES' folder(s) to '_BIOMES Exmls Folder Goes Here', E) Import EXML"
                                                        "\n\nDo you want to continue?"
                                                        "\n\n---------------------------WARNING---------------------------", parent=self.window)
                if not response:
                    return


            after_next_update = messagebox.askyesnocancel("Question", "Was the 'BIOMES' folder in the directory '_BIOMES Exmls Folder Goes Here' "
                                                        "created after NMS 'NEXT' update?\n(Update 1.5-July, 2018)"
                                                        "\n\nYes = After\nNo = Before"
                                                        "\n\n--- Answering this incorrectly WILL cause issues. ---", parent=self.window)
            
            self.import_exml_button.configure(state="disabled")
            # show loading screen
            loading_screen = self.show_loading_screen()
            self.window.update_idletasks()  # all pending events processed to show loading screen
            
            if after_next_update is not None:  # check if user clicked Yes or No

                import_thread = threading.Thread(target=self.import_exml_biomes_threaded, args=(after_next_update, loading_screen))
                import_thread.start()
            
            else:
                self.reenable_buttons()
                loading_screen.destroy()
                return

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            
        

    def complete_template(self, loading_screen):
        loading_screen.destroy()
        self.populate_csv_combo()

        self.reenable_buttons()
        self.filemenu.entryconfig('Make Biome Template from EXML', state='normal') # re-enable template menu item

        messagebox.showinfo("New Biome Template Added", "Biome Template .CSV created. Select the new biome template in the dropdown menu, "
                            "and select any relevant checkboxes to start using the new Biome Template."
                            "\n\nSee '_Biome Templates/__template README.txt' for instructions on how to sort the .CSV file + other info.", parent=self.window)


    def make_template_from_exml_threaded(self, after_next_update, template_filename, loading_screen):
        # import exml files in "_BIOMES Exmls Folder Goes Here" folder, pass if after next update or not
        self.controller.c_make_template_from_exml(after_next_update, template_filename)
        self.window.after(0, lambda: self.complete_template(loading_screen))


    def make_template_from_exml(self):
        try:
                
            self.populate_csv_combo()

            biom_exmls_folder_dir = self.controller.get_biom_exmls_folder_dir()
            biomes_folder = os.path.abspath(os.path.join(biom_exmls_folder_dir, 'BIOMES'))

            # verify that the '_BIOMES Exmls Folder Goes Here' directory exists
            if not os.path.exists(biom_exmls_folder_dir):
                messagebox.showerror("Error", f"The import directory does not exist: \n\n{biom_exmls_folder_dir}"
                                    "\n\nPlease do not delete or rename this directory.", parent=self.window)
                return
            else:
                if not os.listdir(biom_exmls_folder_dir):
                    messagebox.showerror("Error", f"The import directory is empty: \n\n{biom_exmls_folder_dir}"
                                        "\n\nDecompile MBINs to EXML, then move one or more 'BIOMES' folder to this directory."
                                        "\nSee: '_Biome Templates/__template README.txt' for more info.", parent=self.window)
                    return
                else:
                    if not os.path.exists(biomes_folder): # check if 'BIOMES' folder in directory
                        response = messagebox.askyesnocancel("Question", f"No 'BIOMES' folder found in directory: \n\n{biom_exmls_folder_dir}"
                                        "\n\nThis folder contains all necessary EXML files for biome conversion into a biome template (CSV). "
                                        "Without it, data WILL be missing."
                                        "\n\n*I do not recommend importing folders other than 'BIOMES'."
                                        "\n*Renaming the 'BIOMES' folder may cause LUA script errors "
                                        "(ignore this if importing a renamed/modded 'BIOMES' folder)."
                                        "\n\nContinue anyway?", parent=self.window)
                        if not response:
                            return

            after_next_update = messagebox.askyesnocancel("Question", "Was the 'BIOMES' folder in the directory '_BIOMES Exmls Folder Goes Here' "
                                                        "created after NMS 'NEXT' update?\n(Update 1.5-July, 2018)"
                                                        "\n\nYes = After\nNo = Before"
                                                        "\n\n--- Answering this incorrectly WILL cause issues. ---", parent=self.window)
            
            if after_next_update is not None:
                # create pop-up window to enter filename
                template_filename = simpledialog.askstring("Enter template filename", "What do you want to name this biome template?"
                                                        "\n\nUse a unique filename to prevent overwriting any .csv file with the same name in your '_Biome Templates' folder."
                                                        "\n\nEnter only numbers, letters, or underscores. Do not add .csv at the end.\n", parent=self.window)
                # verify filename contains numbers, letters, or underscores
                if template_filename and re.match("^[a-zA-Z0-9_]+$", template_filename):
                    template_filename = f"{template_filename}-unsorted.csv" # add '-unsorted.csv'
                else:
                    messagebox.showerror("Invalid Filename", "Invalid filename. Enter only numbers, letters, or underscores.", parent=self.window)
                    return
            
            self.filemenu.entryconfig('Make Biome Template from EXML', state='disabled') # disable make biome template
            # show loading screen
            loading_screen = self.show_loading_screen()
            self.window.update_idletasks()  # all pending events processed to show loading screen
            
            if after_next_update is not None:  # check if user clicked Yes or No
                
                import_thread = threading.Thread(target=self.make_template_from_exml_threaded, args=(after_next_update, template_filename, loading_screen))
                import_thread.start()

            else:
                self.reenable_buttons()
                self.filemenu.entryconfig('Make Biome Template from EXML', state='normal')
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
        all_biome_tile_types = data["all_biome_tile_types"]

        return bfn_all_biome_files_weights, bfn_all_tile_types, bfn_all_valid_start_planets, all_biome_tile_types



    # export
    def export_script(self):
        try:
                
            biomes_objs = self.controller.get_biome_objs()

            # get any imported data
            bfn_all_biome_files_weights = self.controller.get_bfn_all_biome_files_weights()
            bfn_all_tile_types = self.controller.get_bfn_all_tile_types()
            bfn_all_valid_start_planets = self.controller.get_bfn_all_valid_start_planets()
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

                    response = messagebox.askyesnocancel("Import Vanilla JSON?", f"Some spawner data is not configured. Details: \n{missing_variables_str}"
                            "\n\nImport default data to create a new spawner canvas?"
                            "\nNote: This will not replace your Biome Objects List."
                            "\n\nYes = Replace MISSING spawner data."
                            "\nNo = Replace *ALL* spawner data.", parent=self.window)

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

                # verify that the '_BIOMES Exmls Folder Goes Here' directory exists
                if not os.path.exists(default_bfn_folder_dir):
                    messagebox.showerror("Error", f"The default import directory does not exist: \n\n{default_bfn_folder_dir}"
                                        "\n\nPlease do not delete or rename this directory.", parent=self.window)
                    return

                if not os.path.isfile(json_file_path):
                    messagebox.showerror("Error", f"JSON filepath does not exist: \n\n{json_file_path}"
                                            "\n\nPlease do not rename or delete this JSON file.", parent=self.window)
                    return

                # import data from JSON file
                bfn_all_biome_files_weights_c, bfn_all_tile_types_c, bfn_all_valid_start_planets_c, all_biome_tile_types_c = self.import_from_json(json_file_path)
                # set default values
                if replace_missing_vars_w_json: # True
                    if missing_var_a:
                        self.controller.set_bfn_all_biome_files_weights(bfn_all_biome_files_weights_c)
                    if missing_var_b:
                        self.controller.set_bfn_all_tile_types(bfn_all_tile_types_c)
                    if missing_var_c:
                        self.controller.set_all_biome_tile_types(all_biome_tile_types_c)
                    self.controller.set_bfn_all_valid_start_planets(bfn_all_valid_start_planets_c) # replace regardless

                else: # False - replace ALL
                    self.controller.set_bfn_all_biome_files_weights(bfn_all_biome_files_weights_c)
                    self.controller.set_bfn_all_tile_types(bfn_all_tile_types_c)
                    self.controller.set_bfn_all_valid_start_planets(bfn_all_valid_start_planets_c)
                    self.controller.set_all_biome_tile_types(all_biome_tile_types_c)

                # refresh for any recently modified imported data
                bfn_all_biome_files_weights = self.controller.get_bfn_all_biome_files_weights()
                bfn_all_tile_types = self.controller.get_bfn_all_tile_types()
                bfn_all_valid_start_planets = self.controller.get_bfn_all_valid_start_planets()
                all_biome_tile_types = self.controller.get_all_biome_tile_types() # **each** biome file


            # check if user ignored error message when importing
            if len(bfn_all_biome_files_weights) < 16:
                response = messagebox.askyesno("Issues Exporting - Import Vanilla JSON?", f"The imported biome files list contains less than 16 entries! "
                                            "\n\nYou should've gotten an error message saying to re-import the EXML files. "
                                            "\n\nOne alternative solution is to import vanilla JSON data to create "
                                            "a basic canvas (or you can go back and import EXML files)."
                                            "\n\nI do not recommend this if you don't know what you're doing..."
                                            "\n\nContinue with replacing export data with a vanilla canvas?"
                                            "\n\nFYI: This will replace any/all of your current biome spawner data."
                                            "\nThis will not replace your current Biome Objects List.", parent=self.window)
                if not response:
                    return
                else:
                    default_bfn_folder_dir = self.controller.get_default_bfn_folder_dir()
                    json_file_path = os.path.abspath(os.path.join(default_bfn_folder_dir, 'default_bfn_and_biomes.json'))

                    # verify that the '_BIOMES Exmls Folder Goes Here' directory exists
                    if not os.path.exists(default_bfn_folder_dir):
                        messagebox.showerror("Error", f"The default import directory does not exist: \n\n{default_bfn_folder_dir}"
                                            "\n\nPlease do not delete or rename this directory.", parent=self.window)
                        return

                    if not os.path.isfile(json_file_path):
                        messagebox.showerror("Error", f"JSON filepath does not exist: \n\n{json_file_path}"
                                                "\n\nPlease do not rename or delete this JSON file.", parent=self.window)
                        return

                    # import data from JSON file
                    bfn_all_biome_files_weights, bfn_all_tile_types, bfn_all_valid_start_planets, all_biome_tile_types = self.import_from_json(json_file_path)
                    # set default values
                    self.controller.set_bfn_all_biome_files_weights(bfn_all_biome_files_weights)
                    self.controller.set_bfn_all_tile_types(bfn_all_tile_types)
                    self.controller.set_bfn_all_valid_start_planets(bfn_all_valid_start_planets)
                    self.controller.set_all_biome_tile_types(all_biome_tile_types)
                    messagebox.showinfo("Export Window", "Any changes made in the next window will be saved automatically.", parent=self.window)

            else:
                messagebox.showinfo("Export Window", "Any changes made in the next window will be saved automatically.", parent=self.window)

            #self.root.withdraw()
            plumgen_view_gen_export = PlumgenViewGenExport(
                self.root,
                self.window,
                biomes_objs,
                bfn_all_biome_files_weights,
                bfn_all_valid_start_planets,
                bfn_all_tile_types,
                all_biome_tile_types,
                self.icon_path,
                self.apply_export_settings
            )

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            

    def apply_export_settings(self, bfn_all_biome_files_weights_c, bfn_all_valid_start_planets_c, bfn_all_tile_types_c, all_biome_tile_types_c):
        try:
            self.controller.set_bfn_all_biome_files_weights(bfn_all_biome_files_weights_c)
            self.controller.set_bfn_all_tile_types(bfn_all_tile_types_c)
            self.controller.set_bfn_all_valid_start_planets(bfn_all_valid_start_planets_c)
            self.controller.set_all_biome_tile_types(all_biome_tile_types_c)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
            


    # called when the Toplevel window is closed
    def on_close(self):
        try:
            #self.root.deiconify() # show the root window again
            #self.window.destroy() # destroy the Toplevel window
            if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"
                                "\n\nAny changes will be lost unless you exported to LUA.", parent=self.window):


                self.root.destroy()
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
'''
File: PLUMGEN_view_gen_export.py
'''

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, Scale, Label, Button, IntVar, Listbox, Entry, Frame, Text, Label, INSERT, simpledialog
import logging
import re
import json
import webbrowser
import ctypes
from datetime import datetime   # timestamping
from view.ScrollableNotebook import ScrollableNotebook
from model.PLUMGEN_export_lua_class import PlumgenExportLuaClass
from model.PLUMGEN_export_exml_class import PlumgenExportExmlClass
from view.PLUMGEN_view_menu import MenuBar


class PlumgenViewGenExport:

    def __init__(self, grandparent, parent, 
                biomes_objs, 
                bfn_all_biome_files_weights, 
                bfn_all_valid_start_planets,
                bfn_all_tile_types,
                all_biome_tile_types,
                icon_path,
                lngs,
                ln,
                apply_callback):
        
        self.logger = logging.getLogger(__name__)  #set up logging

        try:
                
            self.grandparent = grandparent
            self.parent = parent

            self.apply_callback = apply_callback

            # all lists
            self.biomes_objs = biomes_objs

            self.bfn_all_biome_files_weights = bfn_all_biome_files_weights
            self.bfn_all_valid_start_planets = bfn_all_valid_start_planets
            self.bfn_all_tile_types = bfn_all_tile_types

            self.all_biome_tile_types = all_biome_tile_types  # **each** biome file

            self.icon_path = icon_path
            self.langs = lngs
            self.lan = ln

            #if not self.bfn_all_valid_start_planets: # check that valid_start_planets is not empty -- happens with pre-next NMS
            #    self.bfn_all_valid_start_planets.append("!! Don't leave blank [ADD THEN DELETE ME]")

            # new variables
            self.current_planet_type_idx = None
            self.current_planet_tt_idx = None
            self.current_planet_type_listbox = None
            self.bfn_tile_selected_tab_idx = None
            self.bfn_weight_selected_tab_index = None
            self.bfn_weight_selected_tab_text = None
            self.bfn_wts_selected_idx = None
            self.valid_start_selected_idx = None
            self.selected_biome_file = None
            self.populate_planet_type_lbs = []

            self.parent.withdraw()
            
            self.window = tk.Toplevel(self.grandparent)
            self.window.title(f"1.1 - {self.langs[self.lan]["view_gen_export_init"]["main_title"]}")
            

            # retrieve parent window's position & size
            parent_width = self.parent.winfo_width()
            parent_height = self.parent.winfo_height()
            parent_x = self.parent.winfo_rootx()
            parent_y = self.parent.winfo_rooty()

            self.window.attributes("-alpha", 0.0) # remove flash
            self.window.update() # explicitly update loading screen
            self.fade_in(self.window)

            # set new window's position & size
            self.window.geometry(f"{parent_width}x{parent_height}+{parent_x}+{parent_y}")

            # check if the code is frozen (compiled to exe) or running as a script
            if getattr(sys, 'frozen', False):
                # if frozen (and running as exe), use this path
                self.parent_path = tk.StringVar(value=os.path.dirname(os.path.dirname(sys.executable)))
            else:
                # if running as script, use this path
                # one level up from the current script's directory
                self.parent_path = tk.StringVar(value=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

            #self.window.iconbitmap(os.path.join(self.parent_path.get(), 'images', 'plum_icon_cc0.ico'))
            self.window.iconbitmap(self.icon_path)

            self.style = ttk.Style(self.window)
            self.style.theme_use('clam')

            self.background_c = '#555555'
            self.highlight_c = '#0078d7'
            self.white_c = '#FFFFFF'

            self.subfolder = '_BIOMES Exmls Folder Goes Here'

            self.style_current()

            self.create_widgets()
            self.layout_widgets()


            # populate biome objects listbox
            self.biome_list_lb.delete(0, tk.END) # empty listbox
            for biome in self.biomes_objs:
                self.biome_list_lb.insert(tk.END, biome.get_filename())

            # populate valid starting planets
            self.valid_start_planet_lb.delete(0, tk.END)
            for valid_planet in self.bfn_all_valid_start_planets:
                self.valid_start_planet_lb.insert(tk.END, valid_planet)

            # populate notebooks with tabs and corresponding data
            self.populate_planet_type_notebook()
            self.populate_tile_type_notebook()
            self.populate_biome_files_list_weights_notebook()

            #---------------------------------------------------------------------

            # set closing event handler for the Toplevel window
            self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    def show_error_message(self, message, max_length=200):
        if len(message) > max_length:
            truncated_message = message[:max_length] + "..."
        else:
            truncated_message = message
        messagebox.showerror("Error", f"{truncated_message}\n\nIf you're struggling to resolve this error, please share the 'plumgen.log' file with the dev.", parent=self.window)


    def customize_style(self):
        hover_bg_color = '#555555'
        hover_bg_prpl_color = '#0078d7'  
        hover_fg_prpl_color = '#2b1c4a'
        red_bg_color = '#473d5c'
        
        self.style.configure('.', background='#333333', foreground=self.white_c, font=('TkDefaultFont', 10))
        self.style.configure('TitleLabel.TLabel', background='#333333', foreground=self.white_c, font=('TkDefaultFont', 14, 'bold'))
        self.style.configure('Title2Label.TLabel', background='#333333', foreground=self.white_c, font=('TkDefaultFont', 12, 'bold'))
        self.style.configure('Title3Label.TLabel', background='#333333', foreground=self.white_c, font=('TkDefaultFont', 12))
        self.style.configure('SmallLabel.TLabel', background='#333333', foreground=self.white_c, font=('TkDefaultFont', 8))
        self.style.configure('TLabel', background='#333333', foreground=self.white_c, font=('TkDefaultFont', 10))
        self.style.configure('TButton', background='#666666', foreground=self.white_c, font=('TkDefaultFont', 10))
        self.style.configure('Start.TButton', background=hover_bg_prpl_color, foreground=self.white_c, font=('TkDefaultFont', 10))
        self.style.configure('Gen.TButton', background='#404040', foreground=self.white_c, font=('TkDefaultFont', 10))
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
        fieldbackground=[('!disabled', '#404040')])

        # notebook styles
        self.style.configure('TNotebook', background='#333333')
        self.style.configure('TNotebook.Tab', background='#473d5c', foreground='#FFFFFF', padding=[5, 5])
        self.style.map('TNotebook.Tab', background=[('selected', hover_fg_prpl_color), ('active', '#241c30')])
        self.style.configure('TFrame', background='#333333')

        # checkbox hover colors
        self.style.map('TCheckbutton',
              background=[('active', hover_bg_color)])
        

    def style_current(self):
        # reuse the existing style instance
        self.customize_style()

        # set background color
        self.window.configure(bg='#333333')
        

    def create_widgets(self):
        # modified menubar
        mb = MenuBar(self.window, bg='#473d5c', fg='#FFFFFF', overbackground='#2b1c4a')
        mb.grid(row=0, column=0, columnspan=10, sticky="ew")

        filemenu = tk.Menu(mb)
        filemenu.add_command(label=self.langs[self.lan]["filemenu_view_gen_export"]["Auto_Add_To_Tiles"], command=self.auto_add_all_biomes)
        filemenu.add_separator()
        filemenu.add_command(label=self.langs[self.lan]["filemenu_view_gen_export"]["Select_All"], command=self.select_all)
        filemenu.add_command(label=self.langs[self.lan]["filemenu_view_gen_export"]["Deselect_All"], command=self.deselect_all)
        filemenu.add_separator()
        filemenu.add_command(label=self.langs[self.lan]["filemenu_view_gen_export"]["Exit"], command=self.on_close)

        self.toolmenu = tk.Menu(mb)
        self.toolmenu.add_command(label=self.langs[self.lan]["filemenu_view_gen_export"]["Replace_Spawner_Json"], command=self.replace_spawner_data)

        editmenu = tk.Menu(mb)
        editmenu.add_command(label=self.langs[self.lan]["filemenu_view_gen_export"]["Help_2"], command=self.open_help)
        editmenu.add_command(label=self.langs[self.lan]["filemenu_view_gen_export"]["About"], command=self.open_about)

        donatemenu = tk.Menu(mb)
        donatemenu.add_command(label=self.langs[self.lan]["filemenu_view_gen_export"]["Donate_3"], command=lambda: webbrowser.open_new("https://www.buymeacoffee.com/sunnysummit"))

        mb.add_menu(self.langs[self.lan]["filemenu_view_gen_export"]["File"], filemenu)
        mb.add_menu(self.langs[self.lan]["filemenu_view_gen_export"]["Tools"], self.toolmenu)
        mb.add_menu(self.langs[self.lan]["filemenu_view_gen_export"]["Help"], editmenu)
        mb.add_menu(self.langs[self.lan]["filemenu_view_gen_export"]["Donate_4"], donatemenu)
        
        # listboxes
        self.biome_list_lb = Listbox(self.window, selectmode=tk.MULTIPLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=42, height=10)
        self.indiv_planet_type_lb = Listbox(self.window, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=42)
        self.valid_start_planet_lb = Listbox(self.window, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=42)

        self.valid_start_planet_lb.bind("<Button-1>", self.on_valid_start_planet_click)

        # scrollbars
        self.biome_scroll_x = ttk.Scrollbar(self.window, orient=tk.HORIZONTAL, command=self.biome_list_lb.xview)
        self.biome_scroll_y = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.biome_list_lb.yview)
        self.biome_list_lb.configure(xscrollcommand=self.biome_scroll_x.set, yscrollcommand=self.biome_scroll_y.set)

        self.indiv_scroll_x = ttk.Scrollbar(self.window, orient=tk.HORIZONTAL, command=self.indiv_planet_type_lb.xview)
        self.indiv_scroll_y = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.indiv_planet_type_lb.yview)
        self.indiv_planet_type_lb.configure(xscrollcommand=self.indiv_scroll_x.set, yscrollcommand=self.indiv_scroll_y.set)

        # buttons
        self.go_back_button = ttk.Button(self.window, text=f"<< {self.langs[self.lan]["buttons_2"]["Go_Back"]}", style='Start.TButton', command=self.on_close, width=20)
        
        #self.select_all_button = ttk.Button(self.window, text="Select All", style='TButton', command=self.select_all)
        #self.deselect_all_button = ttk.Button(self.window, text="Deselect All", style='TButton', command=self.deselect_all)
        
        #self.auto_add_all_biomes_button = ttk.Button(self.window, text="Auto Add ALL Biomes", style='Start.TButton', command=self.auto_add_all_biomes)
        self.add_each_biome_button = ttk.Button(self.window, text=f">> {self.langs[self.lan]["buttons_2"]["Add_Biomes"]} >>", style='Gen.TButton', command=self.add_each_biome, width=20)
        self.delete_each_biome_button = ttk.Button(self.window, text=f"{self.langs[self.lan]["buttons_2"]["Remove_Biome"]} >>", style='Delete.TButton', command=self.delete_each_biome, width=20)

        self.add_tile_type_button = ttk.Button(self.window, text=f">> {self.langs[self.lan]["buttons_2"]["Add_Biomes"]} >>", style='Gen.TButton', command=self.add_tile_type, width=20)
        self.delete_tile_type_button = ttk.Button(self.window, text=f"{self.langs[self.lan]["buttons_2"]["Remove_Biome"]} >>", style='Delete.TButton', command=self.delete_tile_type, width=20)

        self.add_tiletype_set_button = ttk.Button(self.window, text=f"<< {self.langs[self.lan]["buttons_2"]["Add_Tile_Type"]}", style='Gen.TButton', command=self.add_tile_type_set, width=20)
        self.delete_tiletype_set_button = ttk.Button(self.window, text=f"<< {self.langs[self.lan]["buttons_2"]["Delete_Tile_Type"]}", style='Delete.TButton', command=self.delete_tile_type_set, width=20)

        self.add_validp_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons_2"]["Add_Valid_Start"], style='Gen.TButton', command=self.add_valid_start_planet, width=20)
        self.delete_validp_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons_2"]["Remove_Valid_Start"], style='Delete.TButton', command=self.delete_valid_start_planet, width=20)

        self.export_button = ttk.Button(self.window, text=f"{self.langs[self.lan]["buttons_2"]["Export"]} >>", style='Start.TButton', command=self.apply_export_settings)
        
        self.save_weight_button = ttk.Button(self.window, text=self.langs[self.lan]["buttons_2"]["Save Weight"], style='Gen.TButton', command=self.save_weight, width=20)

        # entry
        self.weight_entry = ttk.Entry(self.window, style='TEntry', font=('TkDefaultFont', 12))

        # separators
        self.separator1 = ttk.Separator(self.window, orient="horizontal")
        self.separator2 = ttk.Separator(self.window, orient="horizontal")
        self.separator3 = ttk.Separator(self.window, orient="horizontal")
        self.separator4 = ttk.Separator(self.window, orient="vertical")

        # create labels
        self.biome_list_label = ttk.Label(self.window, text=self.langs[self.lan]["labels"]["title_1"], style='TitleLabel.TLabel', justify=tk.CENTER)
        self.planet_type_label = ttk.Label(self.window, text=self.langs[self.lan]["labels_2"]["sub_tile_types"], style='TitleLabel.TLabel', justify=tk.CENTER)
        self.planet_type_info1_label = ttk.Label(self.window, text=f"      {self.langs[self.lan]["labels_2"]["tips"]}      ", style='SmallLabel.TLabel')
        #self.planet_type_info2_label = ttk.Label(self.window, text="each biome .MBIN", style='SmallLabel.TLabel', justify=tk.LEFT)
        self.tile_type_label = ttk.Label(self.window, text=self.langs[self.lan]["labels_2"]["universal_tile_types"], style='TitleLabel.TLabel', justify=tk.CENTER)
        #self.tile_type_info_label = ttk.Label(self.window, text="(BIOMEFILENAMES.MBIN)", style='SmallLabel.TLabel', justify=tk.CENTER)
        self.biome_file_list_weights_label = ttk.Label(self.window, text=self.langs[self.lan]["labels_2"]["bfl_weights"], style='TitleLabel.TLabel', justify=tk.CENTER)
        #self.biome_file_list_weights_info_label = ttk.Label(self.window, text="(BIOMEFILENAMES.MBIN)", style='SmallLabel.TLabel', justify=tk.CENTER)
        self.valid_start_planet_label = ttk.Label(self.window, text=self.langs[self.lan]["labels_2"]["valid_start"], style='TitleLabel.TLabel', justify=tk.CENTER)
        #self.valid_start_planet_info_label = ttk.Label(self.window, text="(BIOMEFILENAMES.MBIN)", style='SmallLabel.TLabel', justify=tk.CENTER)

        # tooltip
        self.tooltip_label = ttk.Label(self.window, text="", style=".TLabel", wraplength=425)

        # checkbox
        self.hide_tooltip_var = tk.BooleanVar(value=False)
        self.hide_tooltip_cb = ttk.Checkbutton(self.window, text=self.langs[self.lan]["checkboxes"]["hide_tooltip"], variable=self.hide_tooltip_var, command=self.toggle_tooltip)

        # Notebook widgets
        self.planet_type_notebook = ScrollableNotebook(self.window, self.langs, self.lan, wheelscroll=True, tabmenu=True, ind_listbox=self.indiv_planet_type_lb)
        self.tile_type_notebook = ttk.Notebook(self.window)
        self.biome_files_list_weights_notebook = ttk.Notebook(self.window)


    def layout_widgets(self):
        # configure grid weights - expand listboxes/other elements
        for i in range(2, 12):  # rows 2 to 12
            if i != 9 and i != 4 and i != 8:  # exclude rows (e.g. button rows)
                self.window.grid_rowconfigure(i, weight=1)

        for j in range(6):  # columns
            self.window.grid_columnconfigure(j, weight=1)
       
        # listboxes
        self.biome_list_lb.grid(row=2, column=0, columnspan=2, rowspan=10, padx=15, pady=(0, 20), sticky=tk.NSEW)
        self.indiv_planet_type_lb.grid(row=4, column=3, columnspan=3, rowspan=2, padx=(15, 30), pady=(5, 40), sticky=tk.NSEW)
        self.valid_start_planet_lb.grid(row=2, column=6, columnspan=2, rowspan=2,  padx=15, sticky=tk.NSEW)

        # scrollbars
        self.biome_scroll_x.grid(row=11, column=0, columnspan=2, padx=15, pady=(5, 5), sticky=tk.EW + tk.S)
        self.biome_scroll_y.grid(row=2, column=1, rowspan=10, pady=(0, 15), sticky=tk.NS + tk.E)

        self.indiv_scroll_x.grid(row=5, column=3, columnspan=3, padx=(15,30), pady=(5, 25), sticky=tk.EW + tk.S)
        self.indiv_scroll_y.grid(row=4, column=5, rowspan=2, padx=(15,15), pady=(5, 40), sticky=tk.NS + tk.E)

        # buttons
        self.go_back_button.grid(row=12, column=0, padx=20, pady=5, sticky=tk.W)

        #self.select_all_button.grid(row=12, column=0, columnspan=2, padx=15, pady=5, sticky=tk.NS)
        #self.deselect_all_button.grid(row=12, column=1, padx=15, pady=5, sticky=tk.E)

        self.add_each_biome_button.grid(row=4, column=2, padx=15, pady=5, sticky=tk.S)
        self.delete_each_biome_button.grid(row=5, column=2, padx=15, pady=5, sticky=tk.N)
        #self.auto_add_all_biomes_button.grid(row=5, column=2, padx=15, pady=5, sticky=tk.N)

        self.add_tile_type_button.grid(row=6, column=2, padx=15, pady=5, sticky=tk.S)
        self.delete_tile_type_button.grid(row=7, column=2, padx=15, pady=5, sticky=tk.N)

        self.add_tiletype_set_button.grid(row=6, column=6, columnspan=2, padx=15, pady=5, sticky=tk.S)
        self.delete_tiletype_set_button.grid(row=7, column=6, columnspan=2, rowspan=2, padx=15, pady=5, sticky=tk.N)

        self.add_validp_button.grid(row=4, column=6, columnspan=2, padx=15, pady=5, sticky=tk.S)
        self.delete_validp_button.grid(row=5, column=6, columnspan=2, padx=15, pady=5, sticky=tk.N)

        self.export_button.grid(row=12, column=6, columnspan=2, padx=20, pady=5, sticky=tk.E)

        self.save_weight_button.grid(row=12, column=2, padx=15, pady=5, sticky=tk.E)

        # entry
        self.weight_entry.grid(row=12, column=3, padx=15, pady=5, sticky=tk.W)

        # separators
        self.separator1.grid(row=1, column=0, columnspan=8, padx=(5, 5), pady=(5,0), sticky=tk.EW)
        self.separator2.grid(row=5, column=2,  columnspan=6, padx=(5, 5), pady=(5,10), sticky=tk.EW + tk.S)
        self.separator3.grid(row=9, column=2, columnspan=6, padx=(5, 5), pady=(5,0), sticky=tk.EW)
        self.separator4.grid(row=1, column=6, rowspan=5, padx=(0, 0), pady=(20,12), sticky=tk.NS + tk.W)

        # labels
        self.biome_list_label.grid(row=1, column=0, columnspan=2, pady=(5,0), padx=5, sticky=tk.S)
        self.planet_type_label.grid(row=1, column=2, columnspan=4, pady=(5,0), padx=(30, 0), sticky=tk.SW)
        self.planet_type_info1_label.grid(row=1, column=5, padx=5, pady=(5,0), sticky=tk.SE)
        #self.planet_type_info2_label.grid(row=1, column=3, padx=15, pady=5, sticky=tk.S)
        self.tile_type_label.grid(row=5, column=2, columnspan=3, padx=(30, 0), pady=(5,0), sticky=tk.SW)
        #self.tile_type_info_label.grid(row=5, column=2, columnspan=3, padx=15, pady=5, sticky=tk.SW)
        self.biome_file_list_weights_label.grid(row=9, column=2, columnspan=3, padx=(30, 0), pady=(5,0), sticky=tk.SW)
        #self.biome_file_list_weights_info_label.grid(row=9, column=2, columnspan=3, padx=15, pady=5, sticky=tk.SW)
        self.valid_start_planet_label.grid(row=1, column=6, columnspan=2, padx=15, pady=(5,0), sticky=tk.S)
        #self.valid_start_planet_info_label.grid(row=2, column=6, columnspan=2, padx=(15,5), pady=(20, 5))
        
        # tooltip
        self.tooltip_label.grid(row=8, column=5, columnspan=5, rowspan=4, sticky=tk.NSEW)

        # UI element descriptions
        self.listbox_descriptions = {
            self.biome_list_lb: f"> {self.langs[self.lan]["tooltip_2"]["biome_list_lb"]}",
            #self.indiv_planet_type_lb: "Select any biomes you want to add from the Biome Objects List, then click 'Add Biome(s)' button. Now, when you visit planets of this type, there's a chance you'll encounter your newly added biome.",
            self.tile_type_notebook: f"> {self.langs[self.lan]["tooltip_2"]["tile_type_notebook"]}",
            self.biome_files_list_weights_notebook: f"> {self.langs[self.lan]["tooltip_2"]["biome_files_list_weights_notebook"]}",
            self.valid_start_planet_lb: f"> {self.langs[self.lan]["tooltip_2"]["valid_start_planet_lb"]}",
            self.planet_type_info1_label: self.langs[self.lan]["tooltip_2"]["planet_type_info1_label"]
        }
        # *bind motion later when making listboxes in notebook

        # checkbox
        self.hide_tooltip_cb.grid(row=12, column=5)

        # layout notebooks
        self.planet_type_notebook.grid(row=2, column=2, columnspan=4, rowspan=2, padx=15, sticky=tk.NSEW)
        self.tile_type_notebook.grid(row=6, column=3, columnspan=3, rowspan=2, padx=15, sticky=tk.NSEW)
        self.biome_files_list_weights_notebook.grid(row=10, column=2, columnspan=3, rowspan=2, padx=15, sticky=tk.NSEW)

        self.tile_type_notebook.bind("<<NotebookTabChanged>>", self.on_bfn_tiletype_tab_changed)
        self.biome_files_list_weights_notebook.bind("<<NotebookTabChanged>>", self.on_bfn_weights_tab_changed)



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


    def handle_listbox_selection(self, listbox, selected_index):
        if selected_index: 
            for index in range(listbox.size()):
                listbox.itemconfig(index, {'bg': self.background_c})
            listbox.itemconfig(selected_index[0], {'bg': self.highlight_c})

    def on_planet_type_selected(self, event, listbox):
        try:
            selected_index = listbox.curselection()
            self.handle_listbox_selection(listbox, selected_index)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    # mouse move/leave listboxes
    def on_listbox_mouse_move(self, event, listbox):

        # Display tooltip with description
        description = self.listbox_descriptions.get(listbox, "")
        self.tooltip_label.config(text=description)

    def on_listbox_mouse_leave(self, event):
        self.tooltip_label.config(text="")

    def toggle_tooltip(self):
        try:
            if self.hide_tooltip_var.get():
                self.tooltip_label.grid_remove() # hide tooltip label
            else:
                self.tooltip_label.grid() # show
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



    def on_planet_type_clicked(self, event, idx, listbox):
        try:
            
            self.current_planet_type_idx = idx # set the index of what tab/sub-biome was clicked
            
            self.current_planet_type_listbox = listbox

            self.current_planet_tt_idx = self.current_planet_type_listbox.nearest(event.y) # index of clicked item
            
            current_biome_tile_type = self.all_biome_tile_types[self.current_planet_type_idx]
            key = list(current_biome_tile_type.keys())[self.current_planet_tt_idx] # tile type name, string
            values = current_biome_tile_type[key] # MBIN filenames, list

            self.indiv_planet_type_lb.delete(0, tk.END) # empty listbox
            for value in values: # insert each file path into the listbox
                self.indiv_planet_type_lb.insert(tk.END, value)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))





    def on_bfn_tiletype_tab_changed(self, event):
        try:
            selected_tab = self.tile_type_notebook.select()
            
            if selected_tab: self.bfn_tile_selected_tab_idx = self.tile_type_notebook.index(selected_tab)
            else: self.bfn_tile_selected_tab_idx = None
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    def on_bfn_weights_tab_changed(self, event):
        try:
            #self.bfn_weight_selected_tab_idx = self.biome_files_list_weights_notebook.index(self.biome_files_list_weights_notebook.select())
            self.bfn_weight_selected_tab_index = self.biome_files_list_weights_notebook.index(self.biome_files_list_weights_notebook.select())
            selected_tab_string = self.biome_files_list_weights_notebook.tab(self.bfn_weight_selected_tab_index, "text")
            #self.bfn_weight_selected_tab_text = selected_tab_string
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



    def on_bfn_weights_clicked(self, event, listbox):
        try:
            
            if self.bfn_weight_selected_tab_index is not None:

                bfn_weights = self.bfn_all_biome_files_weights
                selected_bfn_weight_values = bfn_weights[self.bfn_weight_selected_tab_index]
                key_name = list(selected_bfn_weight_values.keys())[0]
                selected_biome_files = selected_bfn_weight_values[key_name]
                #first_values = [list(item.keys())[0] for item in selected_bfn_weight_values]

                self.bfn_wts_selected_idx = listbox.nearest(event.y)
                if self.bfn_wts_selected_idx is not None and self.bfn_wts_selected_idx != -1:

                    clicked_fn_wt_value = listbox.get(self.bfn_wts_selected_idx)

                    clicked_fn = clicked_fn_wt_value.split(',')[0].split(': ')[1].strip()

                    self.selected_biome_file = None
                    for item in selected_biome_files:
                        if clicked_fn in item:
                            self.selected_biome_file = item
                            break

                    selected_biome_file_key, selected_biome_file_value = list(self.selected_biome_file.items())[0]
                    weight = selected_biome_file_value.split()[0]

                    self.weight_entry.delete(0, tk.END)
                    self.weight_entry.insert(0, str(weight))  # insert weight for clicked item

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))




    def populate_planet_type_notebook(self):
        
        for idx, biome_tile_types in enumerate(self.all_biome_tile_types):
            tab = ttk.Frame(self.planet_type_notebook)
            filename = biome_tile_types['Filename']

            filepath_parts = filename.split(self.subfolder) # format filename, so it's shorter
            if len(filepath_parts) > 1:
                filename = filepath_parts[-1].replace('.exml', '').replace('.EXML', '').replace('\\', '/')
                filename = ' / '.join([word.title() for word in filename.split('/')])
                filename = re.sub(r'[\\/]+', '/', filename) # Remove consecutive slashes or backslashes
                if filename.startswith('/'): # Remove the first slash if present
                    filename = filename[1:]
                final_filename = filename.split('/')[-1]
                final_filename = final_filename.replace("biome", "").replace("Biome", "").replace("BIOME", "")

            label = ttk.Label(tab, text=f"{filename}", style='Title3Label.TLabel')
            label.grid(row=0, column=0, pady=5, sticky=tk.W)
            listbox = tk.Listbox(tab, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=100)
            scroll_x = ttk.Scrollbar(tab, orient=tk.HORIZONTAL, command=listbox.xview)
            scroll_y = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=listbox.yview)
            listbox.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

            for key, value in biome_tile_types.items(): # populate listbox with data
                if key != 'Filename':
                    listbox.insert(tk.END, f"{key}: {value}")
            # Add the listbox to the tab
            listbox.grid(row=1, column=0, sticky=tk.NSEW)
            scroll_x.grid(row=2, column=0, sticky=tk.EW)
            scroll_y.grid(row=1, column=1, sticky=tk.NS)
            tab.rowconfigure(1, weight=1)  # Make listbox expandable vertically
            tab.columnconfigure(0, weight=1)  # Make listbox expandable horizontally
            self.planet_type_notebook.add(tab, text=str(final_filename))

            listbox.bind("<Button-1>", lambda event, idx=idx, lb=listbox: self.on_planet_type_clicked(event, idx, lb))
            listbox.bind("<<ListboxSelect>>", lambda event, lb=listbox: self.on_planet_type_selected(event, lb))

            self.listbox_descriptions.update({
                listbox: f"> {self.langs[self.lan]["tooltip_2"]["inside_notebook_lb"]}",
            })

            self.populate_planet_type_lbs.append(listbox)
        
        for listbox in self.listbox_descriptions.keys():
            listbox.bind("<Motion>", lambda event, listbox=listbox: self.on_listbox_mouse_move(event, listbox))
            listbox.bind("<Leave>", self.on_listbox_mouse_leave)


    def populate_tile_type_notebook(self):
        
        for tile_type, values in self.bfn_all_tile_types.items():
            tab = ttk.Frame(self.tile_type_notebook)
            listbox = tk.Listbox(tab, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=100)
            scroll_x = ttk.Scrollbar(tab, orient=tk.HORIZONTAL, command=listbox.xview)
            scroll_y = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=listbox.yview)
            listbox.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
            # Populate the listbox with data
            for value in values:
                listbox.insert(tk.END, value)
            # Add the listbox to the tab
            listbox.grid(row=0, column=0, sticky=tk.NSEW)
            scroll_x.grid(row=1, column=0, sticky=tk.EW)
            scroll_y.grid(row=0, column=1, sticky=tk.NS)
            tab.rowconfigure(0, weight=1)  # Make listbox expandable vertically
            tab.columnconfigure(0, weight=1)  # Make listbox expandable horizontally
            self.tile_type_notebook.add(tab, text=tile_type)


    def populate_biome_files_list_weights_notebook(self):
        
        for biome_files_weights in self.bfn_all_biome_files_weights:
            for biome_name, biome_data in biome_files_weights.items():
                tab = ttk.Frame(self.biome_files_list_weights_notebook)
                listbox = tk.Listbox(tab, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=100)
                scroll_x = ttk.Scrollbar(tab, orient=tk.HORIZONTAL, command=listbox.xview)
                scroll_y = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=listbox.yview)
                listbox.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
                # Populate the listbox with data
                for data in biome_data:
                    filename = list(data.keys())[0]
                    weight = data[filename]
                    listbox.insert(tk.END, f"{self.langs[self.lan]["misc"]["Filename"]}: {filename}, {self.langs[self.lan]["misc"]["Weight"]}: {weight}")
                # Add the listbox to the tab
                listbox.grid(row=0, column=0, sticky=tk.NSEW)
                scroll_x.grid(row=1, column=0, sticky=tk.EW)
                scroll_y.grid(row=0, column=1, sticky=tk.NS)
                tab.rowconfigure(0, weight=1)  # Make listbox expandable vertically
                tab.columnconfigure(0, weight=1)  # Make listbox expandable horizontally
                self.biome_files_list_weights_notebook.add(tab, text=biome_name)
                
                listbox.bind("<Button-1>", lambda event, lb=listbox: self.on_bfn_weights_clicked(event, lb))
        

    # handle buttons
        
    def select_all(self):
        try:
            num_items = self.biome_list_lb.size() # num items in the listbox
            for i in range(num_items): 
                self.biome_list_lb.selection_set(i) # select all items
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    def deselect_all(self):
        try:
            self.biome_list_lb.selection_clear(0, tk.END)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



    def auto_add_all_biomes(self):
        try:
            
            confirmed = messagebox.askyesno(self.langs[self.lan]["auto_add_all_biomes"]["add_all_title"], self.langs[self.lan]["auto_add_all_biomes"]["add_all_desc"], parent=self.window)
            if not confirmed:
                return # user clicked no or closed

            for biome in self.biomes_objs:
                biome_name = biome.get_filename()
                if '/' in biome_name:
                    parts = biome_name.split('/')
                    last_part = parts[-1]
                else:
                    last_part = biome_name
                type_parts = last_part.split('_')
                biome_types = []
                biome_types.extend(type_parts[1:])

                for idx, biome_tile_types in enumerate(self.all_biome_tile_types):
                    filename = biome_tile_types['Filename']

                    # split filename to get the path after '_BIOMES Exmls Folder Goes Here'
                    filepath_parts = filename.split(self.subfolder)
                    if len(filepath_parts) > 1:
                        final_filename = filepath_parts[1]
                    
                        # check if any string in biome_types is a substring of file_filename
                        for biome_type in biome_types:
                            if biome_type.lower() in final_filename.lower():
                                
                                biome_name = biome_name.upper()
                                new_biome_name = "METADATA/SIMULATION/SOLARSYSTEM/" + biome_name + ".MBIN"

                                # append biome_name to the first list in biome_tile_types
                                biome_tile_types[list(biome_tile_types.keys())[0]].append(new_biome_name)
                                break  # break if found to avoid adding multiple times

            # update each listbox in the notebook with the new info
            for listbox in self.populate_planet_type_lbs:
                listbox.delete(0, tk.END) # clear

                idx = self.populate_planet_type_lbs.index(listbox) # get index of listbox
                biome_tile_types = self.all_biome_tile_types[idx] # get updated biome_tile_types

                for key, value in biome_tile_types.items(): # populate the listbox with updated data
                    if key != 'Filename':
                        listbox.insert(tk.END, f"{key}: {value}")

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



    def add_each_biome(self):
        try:
            
            first_value = self.indiv_planet_type_lb.get(0)  # get value at index 0
            if first_value != self.langs[self.lan]["tabChanger"]["None_selected"]: # means user selected an item in lb and didn't just change tabs

                selected_indices = self.biome_list_lb.curselection() # get selected items from biome objects listbox
                selected_items = [self.biome_list_lb.get(idx) for idx in selected_indices]

                # format biome name
                modified_items = [f"METADATA/SIMULATION/SOLARSYSTEM/{item.upper().replace(' ', '_')}.MBIN" for item in selected_items]

                current_biome_tile_type = self.all_biome_tile_types[self.current_planet_type_idx]
                key = list(current_biome_tile_type.keys())[self.current_planet_tt_idx] # tile type name, string
                values = current_biome_tile_type[key] # MBIN filenames, list
            
                values.extend(modified_items) # add selected biome MBIN filenames to selected Sub-Biome's tile type

                self.indiv_planet_type_lb.delete(0, tk.END) # empty listbox
                for value in values: # insert each file path into the listbox
                    self.indiv_planet_type_lb.insert(tk.END, value)

                # repopulate listbox in notebook tab
                self.current_planet_type_listbox.delete(0, tk.END) # empty listbox
                for key, value in current_biome_tile_type.items(): # populate listbox with data
                    if key != 'Filename':
                        self.current_planet_type_listbox.insert(tk.END, f"{key}: {value}")

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))






    def delete_each_biome(self):
        try:
            
            first_value = self.indiv_planet_type_lb.get(0)  # get value at index 0
            if first_value != self.langs[self.lan]["tabChanger"]["None_selected"]: # means user selected an item in lb and didn't just change tabs

                confirmed = messagebox.askyesno(self.langs[self.lan]["delete_add_stuff"]["delete_biome_title"], self.langs[self.lan]["delete_add_stuff"]["delete_biome_desc"], parent=self.window)
                if not confirmed:
                    return # user clicked no or closed

                selected_index_tuple = self.indiv_planet_type_lb.curselection()  # get selected index tuple / items from biome objects listbox
                
                if selected_index_tuple:
                    selected_index = selected_index_tuple[0]

                    current_biome_tile_type = self.all_biome_tile_types[self.current_planet_type_idx]
                    key = list(current_biome_tile_type.keys())[self.current_planet_tt_idx] # tile type name, string
                    values = current_biome_tile_type[key] # MBIN filenames, list
                
                    values.pop(selected_index) # delete selected MBIN filename in selected Sub-Biome's tile type

                    self.indiv_planet_type_lb.delete(0, tk.END) # empty listbox
                    for value in values: # insert each file path into the listbox
                        self.indiv_planet_type_lb.insert(tk.END, value)

                    # repopulate listbox in notebook tab
                    self.current_planet_type_listbox.delete(0, tk.END) # empty listbox
                    for key, value in current_biome_tile_type.items(): # populate listbox with data
                        if key != 'Filename':
                            self.current_planet_type_listbox.insert(tk.END, f"{key}: {value}")

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



    def add_tile_type(self):
        try:
            
            selected_indices = self.biome_list_lb.curselection() # get selected items from biome listbox
            selected_items = [self.biome_list_lb.get(idx) for idx in selected_indices]

            # format biome name
            modified_items = [f"METADATA/SIMULATION/SOLARSYSTEM/{item.upper().replace(' ', '_')}.MBIN" for item in selected_items]

            target_item = self.bfn_all_tile_types

            target_item_values = list(target_item.values())[self.bfn_tile_selected_tab_idx]  # dict with one key-value pair
            target_item_values.extend(modified_items)

            # get frame (tab) corresponding to the selected tab index
            selected_tab_frame = self.tile_type_notebook.winfo_children()[self.bfn_tile_selected_tab_idx]

            listbox = selected_tab_frame.winfo_children()[0] # find listbox widget within the selected tab frame
            
            listbox.delete(0, tk.END) # clear listbox
            for value in target_item_values: # insert each file path into the listbox
                listbox.insert(tk.END, value)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



    def delete_tile_type(self):
        try:
            
            confirmed = messagebox.askyesno(self.langs[self.lan]["delete_add_stuff"]["delete_tile_type_title"], self.langs[self.lan]["delete_add_stuff"]["delete_tile_type_desc"], parent=self.window)
            if not confirmed:
                return # user clicked no or closed
            
            # get frame (tab) corresponding to the selected tab index
            selected_tab_frame = self.tile_type_notebook.winfo_children()[self.bfn_tile_selected_tab_idx]

            listbox = selected_tab_frame.winfo_children()[0] # find listbox widget within the selected tab frame

            selected_index_tuple = listbox.curselection()  # get selected index tuple / items from lb in notebook
            if selected_index_tuple:
                selected_index = selected_index_tuple[0]

                target_item = self.bfn_all_tile_types

                target_item_values = list(target_item.values())[self.bfn_tile_selected_tab_idx]  # dict with one key-value pair
                target_item_values.pop(selected_index)

                listbox.delete(0, tk.END) # clear listbox
                for value in target_item_values: # insert each file path into the listbox
                    listbox.insert(tk.END, value)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



    def add_tile_type_set(self):
        try:
            
            # pop-up window to enter tile type and weight
            tile_type = simpledialog.askstring(self.langs[self.lan]["delete_add_stuff"]["add_tile_type_title"], self.langs[self.lan]["delete_add_stuff"]["add_tile_type_desc"], parent=self.window)

            if tile_type is None: # check if user canceled the dialog
                return

            # validate input using regular expression
            if not re.match(r'^[a-zA-Z]+\d+ \d+(\.\d+)?$', tile_type):
                # show error message if invalid
                messagebox.showerror(self.langs[self.lan]["delete_add_stuff"]["invalid_input_title"], self.langs[self.lan]["delete_add_stuff"]["invalid_input_desc"], parent=self.window)
                return
            
            target_item = self.bfn_all_tile_types
            target_item[tile_type] = []

            # Create a new tab and listbox
            tab = ttk.Frame(self.tile_type_notebook)
            listbox = tk.Listbox(tab, selectmode=tk.SINGLE, bg=self.background_c, fg=self.white_c, font=('TkDefaultFont', 10), width=100)
            
            # Add the listbox to the tab
            listbox.grid(row=0, column=0, sticky=tk.NSEW)
            tab.rowconfigure(0, weight=1)  # Make listbox expandable vertically
            tab.columnconfigure(0, weight=1)  # Make listbox expandable horizontally
            
            # Add the tab to the notebook
            self.tile_type_notebook.add(tab, text=tile_type)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



    def delete_tile_type_set(self):
        try:
            
            confirmed = messagebox.askyesno(self.langs[self.lan]["delete_add_stuff"]["delete_tile_type_set_title"], self.langs[self.lan]["delete_add_stuff"]["delete_tile_type_set_desc"], parent=self.window)
            if not confirmed:
                return # user clicked no or closed
            
            self.tile_type_notebook.forget(self.bfn_tile_selected_tab_idx)

            target_item = self.bfn_all_tile_types

            # Get the keys of the target_item dictionary
            keys = list(target_item.keys())

            # Get the key corresponding to the selected tab index
            selected_key = keys[self.bfn_tile_selected_tab_idx]

            # Remove the key from the target_item dictionary
            target_item.pop(selected_key, None)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))




    def save_weight(self):
        try:
            
            if self.bfn_weight_selected_tab_index is not None and self.selected_biome_file is not None:

                new_weight_value = self.weight_entry.get() # get value from entry

                # validate new_weight_value is number
                if not re.match(r'^\d+(\.\d+)?$', new_weight_value):
                    messagebox.showerror(self.langs[self.lan]["delete_add_stuff"]["invalid_input_wt_title"], self.langs[self.lan]["delete_add_stuff"]["invalid_input_wt_desc"], parent=self.window)
                    return

                if "." in new_weight_value:
                    new_weight_value = re.sub(r'(?<=\d)0+$', '', new_weight_value)

                bfn_weights = self.bfn_all_biome_files_weights
                selected_bfn_weight_values = bfn_weights[self.bfn_weight_selected_tab_index]
                key_name = list(selected_bfn_weight_values.keys())[0]
                selected_biome_files = selected_bfn_weight_values[key_name]

                if self.bfn_wts_selected_idx is not None and self.bfn_wts_selected_idx != -1:

                    selected_biome_file_key, selected_biome_file_value = list(self.selected_biome_file.items())[0]
                    # split existing value by whitespace to separate weight from rest of string
                    existing_weight, existing_standard = self.selected_biome_file[selected_biome_file_key].split(' ', 1)
                    # replace weight part with the new new_weight_value
                    self.selected_biome_file[selected_biome_file_key] = f"{new_weight_value} {existing_standard}"


                # get frame (tab) corresponding to the selected tab index
                selected_tab_frame = self.biome_files_list_weights_notebook.winfo_children()[self.bfn_weight_selected_tab_index]

                listbox = selected_tab_frame.winfo_children()[0] # find listbox widget within the selected tab frame

                # repopulate listbox
                listbox.delete(0, tk.END) # clear listbox
                for data in selected_biome_files:
                    filename = list(data.keys())[0]
                    weight = data[filename]
                    listbox.insert(tk.END, f"{self.langs[self.lan]["misc"]["Filename"]}: {filename}, {self.langs[self.lan]["misc"]["Weight"]}: {weight}")

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))






    def on_valid_start_planet_click(self, event):
        try:
            # get index of clicked item
            self.valid_start_selected_idx = self.valid_start_planet_lb.nearest(event.y)
        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



    def add_valid_start_planet(self):
        try:
            
            starting_planet = simpledialog.askstring(self.langs[self.lan]["delete_add_stuff"]["add_start_plan_title"], self.langs[self.lan]["delete_add_stuff"]["add_start_plan_desc"], parent=self.window)

            if starting_planet is None: # check if user canceled the dialog
                return

            if not re.match(r'^[a-zA-Z]+$', starting_planet):
                messagebox.showerror(self.langs[self.lan]["delete_add_stuff"]["invalid_start_input_title"], self.langs[self.lan]["delete_add_stuff"]["invalid_start_input_desc"], parent=self.window)
                return
            
            #valid_start_planet_list = self.bfn_all_valid_start_planets[0]
            self.bfn_all_valid_start_planets.append(starting_planet)

            self.valid_start_planet_lb.delete(0, tk.END)
            for valid_planet in self.bfn_all_valid_start_planets:
                self.valid_start_planet_lb.insert(tk.END, valid_planet)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))




    def delete_valid_start_planet(self):
        try:
            
            if self.valid_start_selected_idx is not None:

                confirmed = messagebox.askyesno(self.langs[self.lan]["delete_add_stuff"]["delete_start_plan_title"], self.langs[self.lan]["delete_add_stuff"]["delete_start_plan_desc"], parent=self.window)
                if not confirmed:
                    return # user clicked no or closed
                
                #valid_start_planet_list = self.bfn_all_valid_start_planets[0]
                self.bfn_all_valid_start_planets.pop(self.valid_start_selected_idx)

                self.valid_start_planet_lb.delete(0, tk.END)
                for valid_planet in self.bfn_all_valid_start_planets:
                    self.valid_start_planet_lb.insert(tk.END, valid_planet)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



    def import_from_json(self, filename):
        with open(filename, "r") as json_file:
            data = json.load(json_file)
        
        bfn_all_biome_files_weights = data["bfn_all_biome_files_weights"]
        bfn_all_tile_types = data["bfn_all_tile_types"]
        bfn_all_valid_start_planets = data["bfn_all_valid_start_planets"]
        all_biome_tile_types = data["all_biome_tile_types"]

        return bfn_all_biome_files_weights, bfn_all_tile_types, bfn_all_valid_start_planets, all_biome_tile_types

    def replace_spawner_data(self):
        try:
            
            result = messagebox.askyesno(self.langs[self.lan]["replace_spawner_data"]["replace_spawn_json_title"], self.langs[self.lan]["replace_spawner_data"]["replace_spawn_json_desc"], parent=self.window)
            if not result:
                return

            # check if the code is frozen (compiled to exe) or running as a script
            if getattr(sys, 'frozen', False):
                # if frozen (and running as exe), use this path
                current_directory = os.path.dirname(sys.executable)
                default_subfolder = 'Defaults Json'
                default_bfn_folder_dir = os.path.abspath(os.path.join(current_directory, default_subfolder))
                json_file_path = os.path.abspath(os.path.join(default_bfn_folder_dir, 'default_bfn_and_biomes.json'))
            else:
                # if running as script, use this path
                current_directory = os.path.dirname(os.path.realpath(__file__))
                default_subfolder = 'Defaults Json'
                default_bfn_folder_dir = os.path.abspath(os.path.join(current_directory, '..', default_subfolder))
                json_file_path = os.path.abspath(os.path.join(default_bfn_folder_dir, 'default_bfn_and_biomes.json'))


            # verify that the '_BIOMES Exmls Folder Goes Here' directory exists
            if not os.path.exists(default_bfn_folder_dir):
                messagebox.showerror(self.langs[self.lan]["replace_spawner_data"]["Error"], f"{self.langs[self.lan]["replace_spawner_data"]["error_1_desc_pt1"]}{default_bfn_folder_dir}{self.langs[self.lan]["replace_spawner_data"]["error_1_desc_pt2"]}", parent=self.window)
                return

            if not os.path.isfile(json_file_path):
                messagebox.showerror(self.langs[self.lan]["replace_spawner_data"]["Error"], f"{self.langs[self.lan]["replace_spawner_data"]["error_3_desc_pt1"]}{json_file_path}{self.langs[self.lan]["replace_spawner_data"]["error_3_desc_pt2"]}", parent=self.window)
                return

            # import data from JSON file
            self.bfn_all_biome_files_weights, self.bfn_all_tile_types, self.bfn_all_valid_start_planets, self.all_biome_tile_types = self.import_from_json(json_file_path)

            messagebox.showinfo(self.langs[self.lan]["replace_spawner_data"]["import_json_complete_title"], self.langs[self.lan]["replace_spawner_data"]["import_json_complete_desc"], parent=self.window)

            self.on_close()

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    # function to validate input
    def validate_input(self, input_string):
        return re.match(r'^[a-zA-Z0-9_.-]+$', input_string) is not None


    def create_export_settings_window(self):
        # draw distance dialog

        self.export_settings_window = tk.Toplevel(self.window)
        self.export_settings_window.title(self.langs[self.lan]["export_settings_window"]["main_title"])
        #export_settings_window.configure(bg="#333333")
        self.export_settings_window.iconbitmap(self.icon_path)

        # set DPI awareness, handle scaling better
        try: ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except: pass  # DPI awareness not available

        parent_x = self.window.winfo_rootx()
        parent_y = self.window.winfo_rooty()
        self.export_settings_window.geometry(f"+{parent_x}+{parent_y}")
        self.export_settings_window.grab_set()  # prevent this window from going behind main window

        dr_label = tk.Label(self.export_settings_window, text=self.langs[self.lan]["export_settings_window"]["dr_label"], justify=tk.LEFT, font=("TkDefaultFont", 8))
        dr_label.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(0, 20), sticky=tk.W)

        self.prop_dist_var = tk.BooleanVar()
        dr_checkbox = tk.Checkbutton(self.export_settings_window, text=self.langs[self.lan]["export_settings_window"]["dr_checkbox"], variable=self.prop_dist_var)
        dr_checkbox.grid(row=1, column=0, columnspan=2, padx=(20, 20), sticky=tk.W)

        # global lod/draw distance dialog
        #global_label = tk.Label(export_settings_window, text="Global LOD/draw distance limit/fade time [+]")
        #global_label.grid(row=2, column=0, columnspan=2, padx=(10, 10))

        self.global_dist_var = tk.BooleanVar()
        global_checkbox = tk.Checkbutton(self.export_settings_window, text=self.langs[self.lan]["export_settings_window"]["global_checkbox"], variable=self.global_dist_var)
        global_checkbox.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(0, 20), sticky=tk.W)

        # mod author entry
        self.mod_author_entry = tk.Entry(self.export_settings_window)
        mod_author_label = tk.Label(self.export_settings_window, text=self.langs[self.lan]["export_settings_window"]["Mod_Author"])
        mod_author_label.grid(row=4, column=0, padx=(0, 0), sticky=tk.E)
        self.mod_author_entry.grid(row=4, column=1, padx=(0, 10), sticky=tk.W)

        # biomes filename entry
        self.biomes_filename_entry = tk.Entry(self.export_settings_window)
        biomes_filename_label = tk.Label(self.export_settings_window, text=self.langs[self.lan]["export_settings_window"]["Biomes_Filename"])
        biomes_filename_label.grid(row=5, column=0, padx=(0, 0), sticky=tk.E)
        self.biomes_filename_entry.grid(row=5, column=1, padx=(0, 10), sticky=tk.W)

        # spawner filename entry
        self.spawner_filename_entry = tk.Entry(self.export_settings_window)
        spawner_filename_label = tk.Label(self.export_settings_window, text=self.langs[self.lan]["export_settings_window"]["Spawner_Filename"])
        spawner_filename_label.grid(row=6, column=0, padx=(0, 0), sticky=tk.E)
        self.spawner_filename_entry.grid(row=6, column=1, padx=(0, 10), sticky=tk.W)

        # export button
        export_button = tk.Button(self.export_settings_window, text=self.langs[self.lan]["export_settings_window"]["Export"], command=self.export_all_the_files, width=10, background='#473d5c', foreground=self.white_c)

        export_button.grid(row=7, column=0, columnspan=2, padx=(10, 10), pady=(30, 10))



    def export_all_the_files(self):
        # get values from export settings window
        self.prop_dist = self.prop_dist_var.get()
        self.global_dist = self.global_dist_var.get()
        mod_author = self.mod_author_entry.get()
        biomes_filename = self.biomes_filename_entry.get()
        spawner_filename = self.spawner_filename_entry.get()

        timestamp = datetime.now().strftime('%Y-%m-%d %H%M%S')

        # validate user input
        if not mod_author:
            messagebox.showerror(self.langs[self.lan]["export_all_files"]["Error"], self.langs[self.lan]["export_all_files"]["Error_Desc_1"], parent=self.window)
            return
        if not self.validate_input(mod_author):
            messagebox.showerror(self.langs[self.lan]["export_all_files"]["Error"], self.langs[self.lan]["export_all_files"]["Error_Desc_2"], parent=self.window)
            return

        if not biomes_filename:
            messagebox.showerror(self.langs[self.lan]["export_all_files"]["Error"], self.langs[self.lan]["export_all_files"]["Error_Desc_3"], parent=self.window)
            return
        if not self.validate_input(biomes_filename):
            messagebox.showerror(self.langs[self.lan]["export_all_files"]["Error"], self.langs[self.lan]["export_all_files"]["Error_Desc_4"], parent=self.window)
            return

        if not spawner_filename:
            messagebox.showerror(self.langs[self.lan]["export_all_files"]["Error"], self.langs[self.lan]["export_all_files"]["Error_Desc_5"], parent=self.window)
            return
        if not self.validate_input(spawner_filename):
            messagebox.showerror(self.langs[self.lan]["export_all_files"]["Error"], self.langs[self.lan]["export_all_files"]["Error_Desc_6"], parent=self.window)
            return
        

        self.export_button.config(state="disabled") # disable export button
        self.go_back_button.config(state="disabled")
        self.toolmenu.entryconfig(self.langs[self.lan]["filemenu_view_gen_export"]["Replace_Spawner_Json"], state='disabled')

        # destroy export settings window
        self.export_settings_window.destroy()

        # initialize export lua class, pass arguments
        self.export_class = PlumgenExportLuaClass(
            self.prop_dist,
            self.global_dist,
            self.biomes_objs,
            self.bfn_all_biome_files_weights,
            self.bfn_all_valid_start_planets,
            self.bfn_all_tile_types,
            self.all_biome_tile_types,
            timestamp
        )

        # write PlumgenBiomes.lua
        self.export_class.export_biome_objects(mod_author, biomes_filename)

        # write PlumgenSpawner.lua
        self.export_class.export_biome_spawner(mod_author, spawner_filename)
        '''
        messagebox.showinfo("All Done!", "LUAs created:"
                        "\n\n1. PlumgenBiomes.lua - Contains biome objects" \
                        "\n2. PlumgenSpawner.lua - Spawns biomes"
                        "\n\nTo make future changes, extract and import EXML to PLUMGEN.\nTo get EXML: "
                        "\n\n[1][Recommended] Place any PAK(s) in ModScript folder, run BUILDMOD.bat, navigate to AMUMSS folder: "
                        "TOOLS\\UNPACKED_DECOMPILED_PAKs\\[your mod]\\EXMLFILES_PAK (look for BIOMES folder & copy to PLUMGEN's BEFGH folder)."
                        "\n\nOR"
                        "\n\n[2] Place 1 LUA in ModScript folder, run BUILDMOD.bat, navigate to AMUMSS folder: "
                        "TOOLS\\EXML_Helper\\MODDED (look for BIOMES folder & copy to PLUMGEN's BEFGH folder)."
                        "\n\nNote: File structure may vary with AMUMSS updates.", parent=self.window)
        '''

        # initialize export exml class, pass arguments
        self.export_exml_class = PlumgenExportExmlClass(
            self.prop_dist,
            self.global_dist,
            self.biomes_objs,
            self.bfn_all_biome_files_weights,
            self.bfn_all_valid_start_planets,
            self.bfn_all_tile_types,
            self.all_biome_tile_types,
            timestamp,
            self.langs,
            self.lan,
            self.window
        )


        # begin exporting directly to pak

        connected_to_internet = self.export_exml_class.update_mbc_move_files() #
        #print("\n1")
        if connected_to_internet:
            self.export_exml_class.modify_prop_scenes()
            #print("\n2")
            self.export_exml_class.modify_each_subbiome()
            #print("\n3")
            self.export_exml_class.make_initial_bio_objs_file()
            #print("\n4")
            self.export_exml_class.modify_biome_objects() 
            #print("\n5")
            self.export_exml_class.modify_biomefilenames()
            #print("\n6")
            self.export_exml_class.modify_globals() #
            #print("\n7")
            self.export_exml_class.make_move_mbins_pak_and_validate(biomes_filename, spawner_filename)
            #print("\n8")

        self.export_button.config(state="normal") # reenable export button
        self.go_back_button.config(state="normal")
        self.toolmenu.entryconfig(self.langs[self.lan]["filemenu_view_gen_export"]["Replace_Spawner_Json"], state="normal")


    def apply_export_settings(self):
        try:

            # validate imported 16 sub-biomes
            if len(self.bfn_all_biome_files_weights) < 16:
                confirmed = messagebox.askyesno(self.langs[self.lan]["apply_export_settings"]["spawner_crash_title"], self.langs[self.lan]["apply_export_settings"]["spawner_crash_desc"], parent=self.window)
                if not confirmed:
                    return # user clicked no or closed

            # validate no empty lists in each sub-biome tiletype
            empty_list_found = False
            for item in self.all_biome_tile_types:
                for key, value in item.items():
                    if isinstance(value, list) and not value:
                        empty_list_found = True
                        break
                
            if empty_list_found:
                confirmed = messagebox.askyesno(self.langs[self.lan]["apply_export_settings"]["spawner_crash_2_title"], self.langs[self.lan]["apply_export_settings"]["spawner_crash_2_desc"], parent=self.window)
                if not confirmed:
                    return

            # validate no missing data
            missing_variables = []

            if not self.biomes_objs:
                missing_variables.append("A. Biome objects")
            if not self.bfn_all_valid_start_planets:
                missing_variables.append("B. Valid start planets")
            if not self.bfn_all_tile_types:
                missing_variables.append("C. Tile types")
            if not self.all_biome_tile_types:
                missing_variables.append("D. Biome tile types")

            if missing_variables:
                missing_variables_str = ", ".join(missing_variables)
                confirmed = messagebox.askyesno(self.langs[self.lan]["apply_export_settings"]["missing_data_title"], f"{self.langs[self.lan]["apply_export_settings"]["missing_data_desc_pt1"]}{missing_variables_str}{self.langs[self.lan]["apply_export_settings"]["missing_data_desc_pt2"]}", parent=self.window)
                if not confirmed:
                    return

            # new window to for export settings
            self.create_export_settings_window()


        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))




    def fade_out(self, window_type, alpha=1.0):
        try:
            
            if alpha > 0:
                window_type.attributes("-alpha", alpha)
                window_type.after(1, lambda a=alpha: self.fade_out(window_type, a - 0.01))
                window_type.update() # explicitly update window
            else:
                window_type.attributes("-alpha", 0.0)
                self.fade_in(self.parent)
                window_type.destroy()

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))



    def fade_in(self, window_type, alpha=0.0):
        try:
            
            if alpha < 1:
                window_type.attributes("-alpha", alpha)
                window_type.after(1, lambda a=alpha: self.fade_in(window_type, a + 0.01))
                window_type.update() # explicitly update window
            else:
                window_type.attributes("-alpha", 1.0)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))


    # called when the Toplevel window is closed
    def on_close(self):
        try:

            messagebox.showinfo(self.langs[self.lan]["on_close_2"]["biome_notice_title"], self.langs[self.lan]["on_close_2"]["biome_notice_desc"], parent=self.window)
            
            self.apply_callback(self.bfn_all_biome_files_weights, self.bfn_all_valid_start_planets, self.bfn_all_tile_types, self.all_biome_tile_types)

            self.parent.attributes("-alpha", 0.0) # remove flash
            self.parent.deiconify() # show the root window again
            self.fade_out(self.window)

        except Exception as e:
            self.logger.exception("Error: %s", e) # log the exception
            self.show_error_message("An error occurred: {}".format(str(e)))
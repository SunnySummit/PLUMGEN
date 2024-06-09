'''
File: PLUMGEN_view_gen_bulk.py
'''

import os
import tkinter as tk
from tkinter import ttk, messagebox, Scale, Label, Button, IntVar, Listbox, Entry
import sys
import ctypes

# no file imports

class PlumgenViewGenBulk:
    def __init__(self, parent, bulk_new_val, selected_biome, property_labels_edited, asset_proper_index, icon_path, languages, langu, apply_callback, multiply=False):
        self.parent = parent

        self.apply_callback = apply_callback

        self.selected_biome = selected_biome
        self.property_labels_edited = property_labels_edited
        self.asset_proper_index = asset_proper_index
        self.icon_path = icon_path
        self.langs = languages
        self.lan = langu

        self.multiply = multiply

        self.window = tk.Toplevel(self.parent)
        self.window.title(self.langs[self.lan]["view_gen_bulk_init"]["Main_Title"])

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

        self.style_parent()

        self.level_choice = tk.StringVar(value='1')
        
        self.prop_distant = tk.BooleanVar(value=True)
        self.prop_landmark = tk.BooleanVar(value=False)
        self.prop_object = tk.BooleanVar(value=False)
        self.prop_detail = tk.BooleanVar(value=False)

        self.create_widgets()
        self.layout_widgets()

        self.bulk_new_val = bulk_new_val
        self.value_label.configure(text=self.property_labels_edited[self.asset_proper_index] + ": ")
        
        if self.multiply:
            self.entered_value_label.configure(text=f"* {self.bulk_new_val} {self.langs[self.lan]["view_gen_bulk_init"]["multiply_each_label"]}")
        else:
            self.entered_value_label.configure(text=self.bulk_new_val)

        # set DPI awareness, handle scaling better
        try: ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except: pass  # DPI awareness not available

        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        self.window.geometry(f"+{parent_x}+{parent_y}")

        self.window.grab_set() # prevent this window from going behind main window


    def customize_style(self):
        hover_bg_color = '#555555'  
        hover_fg_color = '#FFFFFF'
        
        self.style.configure('.', background='#333333', foreground=hover_fg_color, font=('TkDefaultFont', 10))
        self.style.configure('TitleLabel.TLabel', background='#333333', foreground=hover_fg_color, font=('TkDefaultFont', 14, 'bold'))
        self.style.configure('TLabel', background='#333333', foreground=hover_fg_color, font=('TkDefaultFont', 10))
        self.style.configure('TButton', background='#666666', foreground=hover_fg_color, font=('TkDefaultFont', 10))
        self.style.configure('Bulk.TButton', background='#5a28a5', foreground=hover_fg_color, font=('TkDefaultFont', 10))
        self.style.configure('TEntry', fieldbackground='#444444', foreground=hover_fg_color, font=('TkDefaultFont', 10))
        self.style.configure('TText', background='#444444', foreground=hover_fg_color, font=('TkDefaultFont', 10))

        # button hover colors
        self.style.map('TButton',
                  background=[('active', hover_bg_color), ('pressed', hover_bg_color)],
                  foreground=[('active', hover_fg_color), ('pressed', hover_fg_color)])
        
        


    def style_parent(self):
        # reuse the existing style instance
        self.customize_style()

        # set background color
        self.window.configure(bg='#333333')
        

    def create_widgets(self):
        # Left column widgets
        self.choose_level_label = ttk.Label(self.window, text=self.langs[self.lan]["left_col_widg"]["choose_level_label"], style='TitleLabel.TLabel')
        self.current_biome_radio = ttk.Radiobutton(self.window, text=self.langs[self.lan]["left_col_widg"]["current_biome_radio"], variable=self.level_choice, value='1')
        self.all_biomes_radio = ttk.Radiobutton(self.window, text=self.langs[self.lan]["left_col_widg"]["all_biomes_radio"], variable=self.level_choice, value='2')

        # Right column widgets
        self.choose_category_label = ttk.Label(self.window, text=self.langs[self.lan]["right_col_widg"]["choose_category_label"], style='TitleLabel.TLabel')
        self.all_distant_objects_check = ttk.Checkbutton(self.window, text=self.langs[self.lan]["right_col_widg"]["all_distant_objects_check"], variable=self.prop_distant, onvalue=True, offvalue=False)
        self.all_landmarks_check = ttk.Checkbutton(self.window, text=self.langs[self.lan]["right_col_widg"]["all_landmarks_check"], variable=self.prop_landmark, onvalue=True, offvalue=False)
        self.all_objects_check = ttk.Checkbutton(self.window, text=self.langs[self.lan]["right_col_widg"]["all_objects_check"], variable=self.prop_object, onvalue=True, offvalue=False)
        self.all_detail_objects_check = ttk.Checkbutton(self.window, text=self.langs[self.lan]["right_col_widg"]["all_detail_objects_check"], variable=self.prop_detail, onvalue=True, offvalue=False)

        # Labels for entered value
        self.value_label = ttk.Label(self.window, text=self.langs[self.lan]["labels_button"]["value_label"], style='TitleLabel.TLabel')
        self.entered_value_label = ttk.Label(self.window, text=self.langs[self.lan]["labels_button"]["entered_value_label"], style='TLabel')

        # Apply button
        self.apply_button = ttk.Button(self.window, text=self.langs[self.lan]["labels_button"]["apply_button"], command=self.apply_bulk_settings, style='Bulk.TButton')


    def layout_widgets(self):
        # set row and column weights for this frame - expanding widgets/elements
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(4, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        # Left column layout
        self.choose_level_label.grid(row=1, column=0, columnspan=2, padx = 40, pady=(10, 0))

        self.current_biome_radio.grid(row=2, column=0, sticky=tk.W, padx=(50, 0))
        self.all_biomes_radio.grid(row=3, column=0, sticky=tk.W, padx=(50, 0))

        # Right column layout
        self.choose_category_label.grid(row=0, column=2, columnspan=2, padx = 40, pady=(10, 0))

        self.all_distant_objects_check.grid(row=1, column=2, sticky=tk.W, padx=(50, 0))
        self.all_landmarks_check.grid(row=2, column=2, sticky=tk.W, padx=(50, 0))
        self.all_objects_check.grid(row=3, column=2, sticky=tk.W, padx=(50, 0))
        self.all_detail_objects_check.grid(row=4, column=2, sticky=tk.W, padx=(50, 0))

        # Value labels layout
        self.value_label.grid(row=5, column=0, padx=(10, 0), pady=30, sticky=tk.E)
        self.entered_value_label.grid(row=5, column=1, columnspan=3, padx=(0, 10), pady=30, sticky=tk.EW)

        # Apply button layout
        self.apply_button.grid(row=6, column=2, padx=20, pady=(0, 10), sticky=tk.E)


    def apply_bulk_settings(self):

        # checkboxes
        distant = self.prop_distant.get()
        landmark = self.prop_landmark.get()
        object = self.prop_object.get()
        detail = self.prop_detail.get()

        # radio buttons
        level = self.level_choice.get() # '1' if "Selected Biome Only", '2' if "ALL Biomes"

        # create a summary message
        summary_message = self.langs[self.lan]["apply_bulk_settings"]["confirm_desc"]

        response = messagebox.askyesno(self.langs[self.lan]["apply_bulk_settings"]["confirm_title"], summary_message, parent=self.window)
            
        if response: # if yes
            self.apply_callback(self.bulk_new_val, self.selected_biome, distant, landmark, object, detail, level, self.multiply)
            self.window.destroy()
'''
File: PASTA_view_menu.py
'''

import tkinter as tk

# no file imports

class MenuBar(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        kw = tk._cnfmerge((cnf, kw))
        kw['relief'] = kw.get('relief', 'raised')
        self._fg = kw.pop('fg', kw.pop('foreground', 'black'))
        self._over_bg = kw.pop('overbackground', 'blue')
        super().__init__(master=master, **kw)
        self._lb_list = []
    
    def _on_press(self, label, command=None):
        """Internal function. This is called when a user clicks on a menubar."""
        label.menu.post(label.winfo_rootx(), 
            label.winfo_rooty() + label.winfo_height() + 0) # 5 padding (set accordingly)
        if command: command()  # Calls the function passed to `add_menu` method.
    
    def add_menu(self, title, menu, command=None):
        """Add menu labels."""
        l = tk.Label(self, text=title, fg=self._fg, bg=self['bg'], padx=2, pady=2)
        l.grid(row=0, column=len(self._lb_list))
        l.bind('<Enter>', lambda e: l.config(bg=self._over_bg))
        l.bind('<Leave>', lambda e: l.config(bg=self['bg']))
        l.menu = menu  # Easy to access menu with the instance 
                       #   of the label saved in the `self._lb_list`
        l.bind('<1>', lambda e: self._on_press(l, command))
        self._lb_list.append(l)
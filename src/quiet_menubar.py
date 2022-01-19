import tkinter as tk

from quiet_config import Configurations
from quiet_loaders import ConfigLoader


class Menubar():
    # initialising the menu bar of editor
    def __init__(self, parent):
        self._parent = parent
        self.ptrn = r'[^\/]+$'

        #TODO Control Textformat
        font_specs = ('Droid Sans Fallback', 12)

        # setting up basic features in menubar
        menubar = tk.Menu(
            parent.master,
            font=font_specs)
        parent.master.config(menu=menubar)
        self._menubar = menubar

        #file dropdown menu
        file_dropdown = tk.Menu(
            menubar, 
            font=font_specs, 
            tearoff=0)
        file_dropdown.add_command(
            label='Save',
            accelerator='Ctrl+S',
            command=parent.manager.save)
        file_dropdown.add_command(
            label='Reopen (Overrides)',
            accelerator='Ctrl+O',
            command=parent.manager.load)
        file_dropdown.add_separator()
        file_dropdown.add_command(
            label='Exit',
            command=parent.manager.on_closing)
        file_dropdown.add_command(
            label='Update',
            command=parent.manager.update)

        #view dropdown menu
        view_dropdown = tk.Menu(
            menubar, 
            font=font_specs,
            tearoff=0)
        view_dropdown.add_command(
            label='Toggle Menu Bar',
            accelerator='Alt',
            command=self.hide_menu)
        view_dropdown.add_command(
            label='Toggle Line Numbers',
            accelerator='Ctrl+Shift+L',
            command=parent.toggle_linenumbers)

        # menubar add buttons
        menubar.add_cascade(label='File', menu=file_dropdown)
        menubar.add_cascade(label='View', menu=view_dropdown)
        self.menu_fields = [field for field in (
            file_dropdown, view_dropdown)]
        
        self.reload_settings()
        self.hide_menu()

    # Settings reconfiguration function
    def reload_settings(self):
        theme = Configurations.Theme
        ConfigLoader.add_font_attr(self)
        for field in self.menu_fields:
            ConfigLoader.add_font_attr(field)
            field.configure(
                bg=theme.menu_bg,
                fg=theme.menu_fg,
                activeforeground=theme.menubar_fg_active,
                activebackground=theme.menubar_bg_active,
                background = theme.bg_color,
            )
        self._menubar.configure(
            bg=theme.menu_bg,
            fg=theme.menu_fg,
            background = theme.bg_color,
            activeforeground= theme.menubar_fg_active,
            activebackground = theme.menubar_bg_active,
            activeborderwidth=0,
            bd=0)

    # quiet mode is defined here
    def enter_quiet_mode(self):
        self._parent.enter_quiet_mode()

    # hiding the menubar
    def hide_menu(self):
        self._parent.master.config(menu='')

    # display the menubar
    def show_menu(self):
        self._parent.master.config(menu=self._menubar)


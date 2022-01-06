import tkinter as tk
import os
import re
from tkinter.colorchooser import askcolor
from quiet_syntax_highlighting import SyntaxHighlighting
from time import sleep


class Menubar():
    # initialising the menu bar of editor
    def __init__(self, parent):
        self._parent = parent
        self.syntax = parent.syntax_highlighter
        self.ptrn = r'[^\/]+$'
        font_specs = ('Droid Sans Fallback', 12)

        # setting up basic features in menubar
        menubar = tk.Menu(
          parent.master,
          font=font_specs,
          fg=parent.menu_fg,
          bg=parent.menu_bg,
          activeforeground= parent.menubar_fg_active,
          activebackground= parent.menubar_bg_active,
          activeborderwidth=0,
          bd=0)

        parent.master.config(menu=menubar)
        self._menubar = menubar
        # adding features file dropdown in menubar
        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(
          label='Load Previous File',
          accelerator='Ctrl+P',
          command=parent.load_previous_file)
        # new file creation feature
        file_dropdown.add_command(
          label='New File',
            accelerator='Ctrl+N',
            command=parent.new_file)
        # open file feature
        file_dropdown.add_command(
          label='Open File',
            accelerator='Ctrl+O',
            command=parent.open_file)
        file_dropdown.add_command(
          label='Open Directory',
          command=parent.open_dir)
        # save file feature
        file_dropdown.add_command(
          label='Save',
            accelerator='Ctrl+S',
            command=parent.save)
        # Save as feature
        file_dropdown.add_command(
          label='Save As',
            accelerator='Ctrl+Shift+S',
            command=parent.save_as)
        # exit feature
        file_dropdown.add_separator()
        file_dropdown.add_command(
          label='Exit',
          command=parent.on_closing)

        #view dropdown menu
        view_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        view_dropdown.add_command(
          label='Toggle Menu Bar',
          accelerator='Alt',
          command=self.hide_menu)
        view_dropdown.add_command(
          label='Hide Status Bar',
          command=parent.hide_status_bar)
        view_dropdown.add_command(
          label='Toggle Line Numbers',
          accelerator='Ctrl+Shift+L',
          command=parent.toggle_linenumbers)
        view_dropdown.add_command(
          label='Toggle Text Border',
          command=self.toggle_text_border)
        view_dropdown.add_command(
          label='Enter Quiet Mode',
          accelerator='Ctrl+Q',
          command=self.enter_quiet_mode)

        #theme dropdown menu
        theme_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        theme_dropdown.add_command(
          label='Dracula',
          command=self.syntax.syntax_and_themes.load_dracula)
        theme_dropdown.add_command(
          label='Githubly',
          command=self.syntax.syntax_and_themes.load_githubly)

        # menubar add buttons
        menubar.add_cascade(label='File', menu=file_dropdown)
        menubar.add_cascade(label='View', menu=view_dropdown)
        menubar.add_cascade(label='Themes', menu=theme_dropdown)
        #menubar.add_command(label='Undo')
        #menubar.add_command(label='Redo')
        
        self.menu_fields = [field for field in (
            file_dropdown, view_dropdown, theme_dropdown)]

        self.hide_menu()

    # Settings reconfiguration function
    def reconfigure_settings(self):
        settings = self._parent.loader.load_settings_data()
        for field in self.menu_fields:
            field.configure(
                bg=self._parent.menu_bg,
                fg=self._parent.menu_fg,
                activeforeground=self._parent.menubar_fg_active,
                activebackground=self._parent.menubar_bg_active,
                background = self._parent.bg_color,
            )

        self._menubar.configure(
            bg=self._parent.menu_bg,
            fg=self._parent.menu_fg,
            background = self._parent.bg_color,
            activeforeground= self._parent.menubar_fg_active,
            activebackground = self._parent.menubar_bg_active,
          )

    # color to different text tye can be set here
    def open_color_picker(self):
        return askcolor(title='Color Menu', initialcolor='#d5c4a1')[1]

    def toggle_text_border(self):
        settings = self._parent.loader.load_settings_data()
        border_status = settings['textarea_border']
        if border_status == 0:
          self._parent.textarea.configure(bd=0.5)
          settings['textarea_border'] = 0.5
        elif border_status > 0:
          self._parent.textarea.configure(bd=0)
          settings['textarea_border'] = 0
        self._parent.loader.store_settings_data(settings)

    # quiet mode is defined here
    def enter_quiet_mode(self):
        self._parent.enter_quiet_mode()

    # hiding the menubar
    def hide_menu(self):
        self._parent.master.config(menu='')

    # display the menubar
    def show_menu(self):
        self._parent.master.config(menu=self._menubar)


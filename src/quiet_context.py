import tkinter as tk

from quiet_config import Configurations
from quiet_loaders import ConfigLoader


class ContextMenu(tk.Listbox):

    def __init__(self, parent, *args, **kwargs):
        tk.Listbox.__init__(self, parent, *args, **kwargs)

        self.changes = [""]
        self.steps = int()
        self.parent = parent

        # setting tk.RIGHT click menu bar
        self.right_click_menu = tk.Menu(
            parent,
            font='DroidSansFallback')
        self.reload_settings()

        self.right_click_menu.add_command(
            label='Cut',
            command=self.parent.textarea.event_generate('<<Cut>>'))

        self.right_click_menu.add_command(
            label='Copy',
            command=self.parent.textarea.event_generate('<<Copy>>'))

        self.right_click_menu.add_command(
            label='Paste',
            command=self.parent.textarea.event_generate('<<Paste>>'))

    def popup(self, event):
        try:
            self.right_click_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.right_click_menu.grab_release()

    def undo(self, event=None):
        if self.steps != 0:
            self.steps -= 1
            self.parent.textarea.delete(0, tk.END)
            self.parent.textarea.insert(tk.END, self.changes[self.steps])

    def redo(self, event=None):
        if self.steps < len(self.changes):
            self.parent.textarea.delete(0, tk.END)
            self.parent.textarea.insert(tk.END, self.changes[self.steps])
            self.steps += 1

    def add_changes(self, event=None):
        if self.parent.textarea.get() != self.changes[-1]:
            self.changes.append(self.parent.textarea.get())
            self.steps += 1

    def reload_settings(self):
        #TODO: Change Theme handeling
        theme = Configurations.Theme
        conf = Configurations.Settings
        ConfigLoader.add_font_attr(self)
        self.right_click_menu.configure(
            font=conf.font_family,
            fg=theme.menu_fg,
            bg=theme.bg_color,
            activebackground=theme.menubar_bg_active,
            activeforeground=theme.menubar_fg_active,
            bd=0,
            tearoff=0)

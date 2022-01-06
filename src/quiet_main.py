import os
import re
import tkinter as tk
import tkinter.font as tk_font
from platform import system
from tkinter import TclError

from quiet_config import Configurations
from quiet_loaders import ConfigLoader, SyncManager
from quiet_context import ContextMenu
from quiet_linenumbers import TextLineNumbers
from quiet_menubar import Menubar
from quiet_statusbar import Statusbar
from quiet_syntax_highlighting import SyntaxHighlighting
from quiet_textarea import CustomText


class QuietText(tk.Frame):
    def __init__(self, *args, **kwargs):
        """The main class for bringing the whole shebang together"""
        tk.Frame.__init__(self, *args, **kwargs)
        master.title('QuietToDo')
        # defined size of the editer window
        master.geometry('600x500')
        self.operating_system = system()

        self.conf = Configurations.Settings
        self.theme = Configurations.Theme

        # editor metadata 
        self.master = master
        self.filename = os.getcwd()
        self.dirname = os.getcwd()

        # configuration of the file dialog text colors.
        ConfigLoader.add_font_attr(self)
        self.configure(bg='black')

        # Init other
        self.manager = SyncManager(self)
        self.textarea = CustomText(self)
        self.linenumbers = TextLineNumbers(self)
        self.initial_content = self.textarea.get("1.0", tk.END)

        # retrieving the font from the text area and setting a tab width
        self._font = tk_font.Font(font=self.textarea['font'])
        self._tab_width = self._font.measure(' ' * self.conf.tab_size)
        self.textarea.config(tabs=(self._tab_width,))

        self.context_menu = ContextMenu(self)
        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)
        self.syntax_highlighter = SyntaxHighlighting(self, self.textarea, self.initial_content)

        self.linenumbers.attach(self.textarea)
        self.linenumbers.pack(side=tk.LEFT, fill=tk.Y)
        self.textarea.pack(side=tk.RIGHT, fill='both', expand=True)
        
        self.textarea.find_match_index = None
        self.textarea.find_search_starting_index = 1.0

        self.reconfigure_settings()

        #calling function to bind hotkeys.
        self.bind_shortcuts()
        self.control_key = False
        self.menu_hidden = False
        self.first_word = True

        self.sync_stats = True

    def clear_and_replace_textarea(self, text):
        self.textarea.delete(1.0, tk.END)
        self.textarea.insert(1.0, text)
        self.syntax_highlighter.initial_highlight()

    #reconfigure the tab_width depending on changes.
    def set_new_tab_width(self, tab_spaces = 'default'):
        if tab_spaces == 'default':
            space_count = self.conf.tab_size
        else:
            space_count = tab_spaces
        _font = tk_font.Font(font=self.textarea['font'])
        _tab_width = _font.measure(' ' * int(space_count))
        self.textarea.config(tabs=(_tab_width,))

    # editor basic settings can be altered here
    #function used to reload settings after the user changes in settings.yaml
    def reconfigure_settings(self):
        self.conf = Configurations.Settings
        ConfigLoader.add_font_attr(self)
        
        self.context_menu.reload_settings()
        self.linenumbers.reload_settings()
        self.menubar.reload_settings()
        self.textarea.reload_settings()
        self.set_new_tab_width(self.conf.tab_size)

    #hide status bar for text class so it can be used in menu class
    def hide_status_bar(self, *args):
        self.statusbar.hide_status_bar()

    # toggle the visibility of line numbers
    def toggle_linenumbers(self, *args):
        self.linenumbers.visible = not self.linenumbers.visible

    # setting up the editor title
    #Renames the window title bar to the name of the current file.
    def set_window_title(self, name=None):
        if name:
            self.master.title(f'{name} - Quiet Text')
        else:
            self.master.title('untitled - Quiet Text')

    # select all written text in the editor
    def select_all_text(self, *args):
        self.textarea.tag_add(tk.SEL, '1.0', tk.END)
        self.textarea.mark_set(tk.INSERT, '1.0')
        self.textarea.see(tk.INSERT)
        return 'break'

    # give hex colors to the file content for better understanding
    def apply_hex_color(self, key_event):
        new_color = self.menubar.open_color_picker()
        try:
            sel_start = self.textarea.index(tk.SEL_FIRST)
            sel_end = self.textarea.index(tk.SEL_LAST)
            self.textarea.delete(sel_start, sel_end)
            self.textarea.insert(sel_start, new_color)
        except tk.TclError:
            pass

    def _on_change(self, key_event):
        self.linenumbers.redraw()

    def _on_mousewheel(self, event):
        if self.control_key:
            self.change_font_size(1 if event.delta > 0 else -1)

    def _on_linux_scroll_up(self, _):
        if self.control_key:
            self.change_font_size(1)
            if self.filename == self.loader.settings_path:
                self.syntax_highlighter.initial_highlight()

    def _on_linux_scroll_down(self, _):
        if self.control_key:
            self.change_font_size(-1)
            if self.filename == self.loader.settings_path:
                self.syntax_highlighter.initial_highlight()

    def change_font_size(self, delta):
        self.font_size = self.font_size + delta
        min_font_size = 6
        self.font_size = min_font_size if self.font_size < min_font_size else self.font_size
        ConfigLoader.add_font_attr(self, set_size=False)
        self.textarea.configure(font=self.font_style)
        self.set_new_tab_width()
        self.conf.font_size = self.font_size

    # control_l = 37
    # control_r = 109
    # mac_control = 262401 #control key in mac keyboard
    # mac_control_l = 270336 #tk.LEFT control key in mac os with normal keyboard
    # mac_control_r = 262145 #tk.RIGHT control key in mac os with normal keyboard
    def _on_keydown(self, event):
        if event.keycode in [17, 37, 109, 262401, 270336, 262145]:
            self.control_key = True
            self.textarea.isControlPressed = True
        else:
            self.statusbar.update_status('hide')

    def syntax_highlight(self, *args):
        if self.first_word:
            self.syntax_highlighter.initial_highlight()
            self.first_word = not self.first_word
        self.syntax_highlighter.default_highlight()
        self.control_key = False
        self.textarea.isControlPressed = False

    def show_find_window(self, event=None):
        self.textarea.tag_configure('find_match', background=self.theme.text_selection_bg_clr)
        self.textarea.bg_color = self.theme.bg_color
        self.textarea.fg_color = self.theme.menu_fg
        self.textarea.active_fg = self.theme.menubar_fg_active
        self.textarea.active_bg = self.theme.menubar_bg_active
        #FindWindow(self.textarea)
        self.control_key = False
        self.textarea.isControlPressed = False

    def select_all(self):
        self.selection_set(0, 'end')

    def autoclose_base(self, symbol):
        index = self.textarea.index(tk.INSERT)
        self.textarea.insert(index, symbol)
        self.textarea.mark_set(tk.INSERT, index)

    def autoclose_parens(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.conf.autoclose_parentheses and not second_char.isalnum():
            self.autoclose_base(')')

    def autoclose_curly_brackets(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.conf.autoclose_curlybraces and not second_char.isalnum():
            self.autoclose_base('}')

    def autoclose_square_brackets(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.conf.autoclose_squarebrackets and not second_char.isalnum():
            self.autoclose_base(']')

    def autoclose_double_quotes(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.conf.autoclose_doublequotes and not second_char.isalnum():
            self.autoclose_base('"')

    def autoclose_single_quotes(self, event):
        _, second_char, _, _ = self.get_chars_in_front_and_back()
        if self.conf.autoclose_singlequotes and not second_char.isalnum():
            self.autoclose_base("'")

    def get_indent_level(self):
        text = self.textarea
        line = text.get('insert linestart', 'insert lineend')
        match = re.match(r'^(\s+)', line)
        current_indent = len(match.group(0)) if match else 0
        return current_indent

    def auto_indentation(self):
        text = self.textarea
        new_indent = self.get_indent_level()
        text.insert('insert', '\n' + '\t' * new_indent)

    def auto_block_indentation(self, event):
        prev_char, second_char, _, _ = self.get_chars_in_front_and_back()
        text = self.textarea
        if prev_char == ':':
            current_indent = self.get_indent_level()
            new_indent = current_indent + 1
            text.insert('insert', '\n' + '\t' * new_indent)
            return 'break'
        elif prev_char in '{[(' and second_char in '}])':
            current_indent = self.get_indent_level()
            new_indent = current_indent + 1
            text.insert('insert', '\n\n')
            text.insert('insert', '\t' * current_indent)
            index = text.index(tk.INSERT)
            text.mark_set('insert', str(round(float(index) - 1, 1)))
            text.insert('insert', '\t' * new_indent)
            return 'break'
        else:
            self.auto_indentation()
            return 'break'

    def get_chars_in_front_and_back(self):
        index = self.textarea.index(tk.INSERT)
        first_pos = f'{str(index)}-1c'
        end_second_pos = f'{str(index)}+1c'
        first_char = self.textarea.get(first_pos, index)
        second_char = self.textarea.get(index, end_second_pos)
        return (first_char, second_char, index, end_second_pos)
        
    def backspace_situations(self, event):
        first_char, second_char, index, end_second_pos = self.get_chars_in_front_and_back()

        if first_char == "'" and second_char == "'":
            self.textarea.delete(index, end_second_pos)
        elif first_char == '"' and second_char == '"':
            self.textarea.delete(index, end_second_pos)
        elif first_char == '(' and second_char == ')':
            self.textarea.delete(index, end_second_pos)
        elif first_char == '{' and second_char == '}':
            self.textarea.delete(index, end_second_pos)
        elif first_char == '[' and second_char == ']':
            self.textarea.delete(index, end_second_pos)

    def hide_and_unhide_menubar(self, key_event):
        if self.menu_hidden:
            self.menubar.show_menu()
        else:
            self.menubar.hide_menu()
        self.menu_hidden = not self.menu_hidden

    def tab_text(self, event):
        try:
            index = self.textarea.index("sel.first linestart")
            last = self.textarea.index("sel.last linestart")

            if last != index:
                if event.state == 0:
                    while self.textarea.compare(index,"<=", last):
                        if len(self.textarea.get(index, 'end')) != 0:
                            self.textarea.insert(index, '\t')
                        index = self.textarea.index("%s + 1 line" % index)
                else:
                    while self.textarea.compare(index,"<=", last):
                        if self.textarea.get(index, 'end')[:1] == "\t":
                            self.textarea.delete(index)
                        index = self.textarea.index("%s + 1 line" % index)
            else:
                if event.state == 0:
                    index = self.textarea.index(tk.INSERT)
                    self.textarea.insert(index, '\t')
                else:
                    index = self.textarea.index("insert linestart")
                    if self.textarea.get(index, 'end')[:1] == "\t":
                        self.textarea.delete(index)
        except TclError:
            print("TabError")
        return "break"

    def bind_shortcuts(self, *args):
        text = self.textarea
        text.bind('<Control-s>', self.manager.save)
        text.bind('<Control-a>', self.select_all_text)
        text.bind('<Control-m>', self.apply_hex_color)
        text.bind('<Control-f>', self.show_find_window)
        text.bind('<Control-z>', self.syntax_highlighter.initial_highlight)
        text.bind('<Control-y>', self.syntax_highlighter.initial_highlight)
        text.bind('<<Change>>', self._on_change)
        text.bind('<Configure>', self._on_change)
        text.bind('<Button-3>', self.context_menu.popup)
        text.bind('<MouseWheel>', self._on_mousewheel)
        text.bind('<Key>', self._on_keydown)
        text.bind('<KeyRelease>', self.syntax_highlight)
        text.bind('<Shift-asciitilde>', self.syntax_highlighter.initial_highlight)
        text.bind('<Shift-parenleft>', self.autoclose_parens)
        text.bind('<bracketleft>', self.autoclose_square_brackets)
        text.bind('<quoteright>', self.autoclose_single_quotes)
        text.bind('<quotedbl>', self.autoclose_double_quotes)
        text.bind('<braceleft>', self.autoclose_curly_brackets)
        text.bind('<Return>', self.auto_block_indentation)
        text.bind('<BackSpace>', self.backspace_situations)
        text.bind('<Alt_L>', self.hide_and_unhide_menubar)
        text.bind('<Control-L>', self.toggle_linenumbers)
        text.bind('<KeyPress-Tab>', self.tab_text)
        if self.operating_system == 'Windows':
            text.bind('<Shift-Tab>', self.tab_text)
        else:
            text.bind('<Shift-ISO_Left_Tab>', self.tab_text)

if __name__ == '__main__':
    master = tk.Tk()
    master.update()
    qt = QuietText(master)
    qt.pack(side='top', fill='both', expand=True)
    qt.manager.load()
    master.protocol("WM_DELETE_WINDOW", qt.manager.on_closing)
    
    master.mainloop()


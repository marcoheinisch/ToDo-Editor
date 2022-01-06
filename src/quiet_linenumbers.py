import re
import tkinter as tk

from quiet_config import Configurations
from quiet_loaders import ConfigLoader


class TextLineNumbers(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self._parent = parent
        self._textarea = parent.textarea
        self.reload_settings()

    def reload_settings(self):
        self.conf = Configurations.Settings
        self.theme = Configurations.Theme
        ConfigLoader.add_font_attr(self)
        self.redraw()

    def attach(self, text_widget):
        self._textarea = text_widget

    def redraw(self, *args):
        def drawthisline(line_index, lines):
            if len(lines)>line_index and len(lines[line_index])>0:
                print(lines[line_index][0])
                tmp = (lines[line_index][0] == 'o')
                return tmp
            else:
                return False

        if not self.visible:
            return
        self.delete('all')
        self.config(width=(self._parent.font_size * 3), 
                    bd=0, bg=self.theme.bg_color, highlightthickness=0)
        i = self._textarea.index('@0,0')
        i_str = 0
        lines = self._textarea.get(0.0, tk.END).split("\n")
        while True:
            dline= self._textarea.dlineinfo(i)
            if dline is None:break

            y = dline[1]
            index = self._textarea.index(tk.INSERT)
            i_int = int(str(i).split('.')[0])
            pos = index.split('.')[0]
            if not drawthisline(i_int-1,lines):
                linenum = '~ '
            else:
                i_str += 1
                if float(i_str) >= 10:
                    linenum = str(i_str)
                else:
                    linenum = '~' + str(i_str)
            if pos == str(i).split('.')[0] and self.conf.current_line_indicator:
                linenum += self.conf.current_line_indicator_symbol
            self.create_text(2, y, anchor='nw',
                             text=linenum,
                             font=(self.conf.font_family, self._parent.font_size),
                             fill=self.theme.font_color_linenumbers)
            i = self._textarea.index('%s+1line' % i)

    @property
    def visible(self):
        return self.cget('state') == 'normal'

    @visible.setter
    def visible(self, visible):
        self.config(state='normal' if visible else 'disabled')
        if visible:
            self.redraw()
        else:
            self.delete('all')
            self.config(width=0)

import tkinter as tk

class TextLineNumbers(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self._text_font = parent.settings['font_family']
        self._parent = parent
        self.textwidget = parent.textarea

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        font_color = self._parent.menu_fg
        bg_color = self._parent.bg_color
        indicator_on = self._parent.current_line_indicator
        current_line_symbol = self._parent.current_line_symbol
        if not self.visible:
            return

        self.delete('all')
        self.config(width=(self._parent.font_size * 3), 
                    bd=0, bg=bg_color, highlightthickness=0)

        i = self.textwidget.index('@0,0')
        i_str = 0
        while True:
            dline= self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            index = self.textwidget.index(tk.INSERT)
            pos = index.split('.')[0]
            if dline[2] < 30:
                linenum = '~ '
            else:
                i_str += 1
                if float(i_str) >= 10:
                    linenum = str(i_str)
                else:
                    linenum = '~' + str(i_str)
            if pos == str(i).split('.')[0] and indicator_on:
                linenum += current_line_symbol
            self.create_text(2, y, anchor='nw',
                             text=linenum,
                             font=(self._text_font, self._parent.font_size),
                             fill=font_color)
            i = self.textwidget.index('%s+1line' % i)

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

from textwrap import indent
import tkinter as tk

from quiet_config import Configurations
from quiet_loaders import ConfigLoader


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self.isControlPressed = False
        self._orig = self._w + '_orig'
        self.tk.call('rename', self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        self.persistance_tags = [tk.SEL]

        self.reload_settings()

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        try:
            cmd = (self._orig,) + args
            result = ''
            if not self.isControlPressed:
                # if command is not present, execute the event
                result = self.tk.call(cmd)
            else:
                # Suppress y-scroll and x-scroll when control is pressed
                if args[0:2] not in [('yview', 'scroll'), ('xview', 'scroll')]:
                    result = self.tk.call(cmd)
        except tk.TclError:
            result = ''

        # generate an event if something was added or deleted,
        # or the cursor position changed https://regex101.com/
        if (args[0] in ('insert', 'replace', 'delete') or 
            args[0:3] == ('mark', 'set', 'insert') or
            args[0:2] == ('xview', 'moveto') or
            args[0:2] == ('xview', 'scroll') or
            args[0:2] == ('yview', 'moveto') or
            args[0:2] == ('yview', 'scroll')
        ):
            self.event_generate('<<Change>>', when='tail')

        # return what the actual widget returned
        return result   

    def find(self, text_to_find):
        length = tk.IntVar()
        index = self.search(
            text_to_find,
            self.find_search_starting_index,
            stopindex=tk.END, count=length)
        if index:
            self.tag_remove('find_match', 1.0, tk.END)
            end = f'{index}+{length.get()}c'
            self.tag_add('find_match', index, end)
            self.see(index)
            self.find_search_starting_index = end
            self.find_match_index = index
        else:
            if self.find_match_index != 1.0:
                if tk.messagebox.askyesno("No more results", "No further matches. Repeat from the beginning?"):
                    self.find_search_starting_index = 1.0
                    self.find_match_index = None
                    return self.find(text_to_find)
            else:
                tk.messagebox.showinfo("No Matches", "No matching text found")

    def replace_text(self, target, replacement):
        if self.find_match_index:
            current_found_index_line = str(self.find_match_index).split('.')[0]

            end = f"{self.find_match_index}+{len(target)}c"
            self.replace(self.find_match_index, end, replacement)

            self.find_search_starting_index = current_found_index_line + '.0'

    def cancel_find(self):
        self.find_search_starting_index = 1.0
        self.find_match_index = None
        self.tag_remove('find_match', 1.0, tk.END)

    def reload_settings(self):
        self.bg_color = '#eb4034'
        self.bg_color = '#eb4034'
        self.fg_color = '#eb4034'
        self.active_fg = '#eb4034'
        self.active_bg = '#eb4034'
        conf = Configurations.Settings
        theme = Configurations.Theme

        ConfigLoader.add_font_attr(self)
        self.configure(
            bg=theme.bg_color,
            pady=conf.padding_y,
            padx=conf.padding_x,
            fg=theme.font_color,
            spacing1=conf.text_top_lineheight,
            spacing3=conf.text_bottom_lineheight,
            insertbackground=theme.insertion_color,
            selectbackground= theme.text_selection_bg_clr,
            insertofftime=conf.insertion_blink,
            bd=conf.border,
            highlightthickness=conf.border,
            wrap=conf.text_wrap)

    def pattern_highlight(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''
        
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchlimit_mark", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchlimit_mark",
                                count=count, regexp=regexp, exact=True)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")


    def pattern_move(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        
        self.update_search_limit()

        count = tk.IntVar()
        found = 0
        while True:
            self.update_search_limit()
            index = self.search(pattern, "matchEnd","searchlimit_mark",
                                count=count, regexp=regexp, exact=True, )
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
                      
            text = self.get(index,"%s+%sc" % (index, count.get()))
            self.delete(index,"%s+%sc" % (index, count.get()))
            
            self.update_search_limit()
            self.insert(self.index('insert_mark'), text)
            
            #print(f"index: {index} searchlimit_mark: { self.index('searchlimit_mark') } insert_mark: { self.index('insert_mark') } < {end}")
            
            found+=1
            
    def update_search_limit(self):
        index_limit = self.search_limit()
        if not index_limit:
            index_limit = self.index(tk.END)
            self.insert(tk.END, "x= Done \n")
            index_insert = self.index(tk.END)
        else:
            index_insert = f"{int(index_limit.split('.')[0])+1}.0"
        
        self.mark_set("searchlimit_mark", index_limit)  
        self.mark_set("insert_mark", index_insert)  
        
    def search_limit(self):
        count_s = tk.IntVar()
        index = self.search(Configurations.Patterns.pattern_split.regex, "1.0","end",
                                   count=count_s, regexp=True, exact=True, )
        return index
        
    def clear_highlight(self):
        for tag in self.tag_names():
            if tag not in self.persistance_tags:
                self.tag_remove(tag, 1.0, tk.END)
import os
import sys
from tkinter import messagebox
import tkinter.font as tk_font
import tkinter as tk

from quiet_config import Configurations

class ConfigLoader:
    
    @staticmethod
    def copy_attr(from_obj, to_obj):
        attributes = [attr for attr in dir(from_obj) if not callable(getattr(from_obj, attr)) and not attr.startswith("__")]
        # copy attributes from one object to another
        for a in attributes:
            setattr(to_obj,a, getattr(from_obj, a)) 
    
    @staticmethod
    def add_font_attr(to_obj, set_size=True):
        class FontStyle:
            if set_size: 
                font_size = Configurations.Settings.font_size

            font_style = tk_font.Font(
                family=Configurations.Settings.font_family,
                size=Configurations.Settings.font_size)
            italics = tk_font.Font(
                family=Configurations.Settings.font_family, 
                slant='italic', 
                size=Configurations.Settings.font_size)
            bold = tk_font.Font(
                family=Configurations.Settings.font_family, 
                weight='bold',
                size= Configurations.Settings.font_size)

        ConfigLoader.copy_attr(FontStyle, to_obj)

class SyncManager:

    def __init__(self, parent) -> None:
        self.qt = parent
        self.conf = Configurations.Settings
        self.fb_config = self.conf.sync_fb_key
    
    def save_local(self):
        textarea_content = self.qt.textarea.get(1.0, tk.END)
        with open(self.qt.conf.filename, 'w+') as f:
            f.write(textarea_content)
        self.qt.statusbar.update_status('saved')
        
    # saving changes made in the file
    def save(self, *args):
        if self.conf.sync_remote:
            try:
                self.push_remote_text()
            except Exception:
                messagebox.showinfo("Warning", f"No remote save possible!")

        if self.conf.filename:    
            try:
                self.save_local()
            except Exception as e:
                messagebox.showinfo("Warning", f"No local save possible: {e.args}")

    #On exiting the Program
    def quit_save(self, *args):
        try:
            os.path.isfile(self.conf.filename)
            self.save()
        except Exception:
            self.save_as()
        sys.exit()

    def on_closing(self, *args):
        self.quit_save()

    
    def load(self, *args):
        text = False
        if self.conf.sync_remote:
            try:
                text = self.pull_remote_text()
            except Exception:
                self.qt.statusbar.update_status('cant sync')

        if self.conf.filename:
            with open(self.conf.filename, 'r+') as f:
                text_local = f.read()
                if text:
                    if text != text_local:
                        text += "\n>>>>>>>>>>> remote /\ | \/ local <<<<<<<<<<<<<\n" + text_local
                        self.qt.statusbar.update_status('cant sync')
                else:
                    text = text_local
            
        self.qt.clear_and_replace_textarea(text)
    
    def pull_remote_text(self) -> str:
        
        from firebase import Firebase
        db = Firebase(self.fb_config).database()
        return db.get().val()
        

    def push_remote_text(self):
        
        from firebase import Firebase
        db = Firebase(self.fb_config).database()
        textarea_content = self.qt.textarea.get(1.0, tk.END)
        db.set(textarea_content)
        
        
    def update(self): 
        
        self.save()
        
        # TODO: implement auto updating
        
        if not Configurations.Settings.update:
            return
        
        import subprocess
        src_dir = os.path.dirname(os.path.realpath(__file__))
        from pathlib import Path
        path = Path(src_dir)
        src_dir=path.parent.parent.absolute()
        branch = ["main","feature"][Configurations.Settings.update_feature]
        egg =path.parent.name
        
        
        UPDATE_CMD = 'pip install --upgrade --src="%s" -e git+https://github.com/marcoheinisch/ToDo-Editor@%s#egg=%s'
        cmd = UPDATE_CMD % (src_dir, branch, egg) 
        print(f"start {cmd}")
        subprocess.call(f"cmd /k start cmd /k {cmd}", shell=True)
        exit()
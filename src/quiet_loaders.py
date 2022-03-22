import os
import sys
from tkinter import messagebox
import tkinter.font as tk_font
import tkinter as tk

from quiet_config import Configurations
import logger

log = logger.get_logger(__name__)

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
        log.debug("save_local")
        textarea_content = self.qt.textarea.get(1.0, tk.END)
        with open(self.qt.conf.filename, 'w+') as f:
            f.write(textarea_content)
        self.qt.statusbar.update_status('saved')
        
    # saving changes made in the file
    def save(self, *args):
        log.debug("save")
        if self.conf.sync_remote:
            try:
                self.push_remote_text()
            except Exception:
                messagebox.showinfo("Warning", f"No remote save possible!")

        if self.conf.filename and os.path.isfile(self.conf.filename):    
            try:
                self.save_local()
            except Exception as e:
                messagebox.showinfo("Warning", f"No local save possible: {e.args}")

    #On exiting the Program
    def quit_save(self, *args):
        log.debug("quit_save")
        try:            
            self.save()
        except Exception as e:
            log.critical(f"quit_save save failed: {str(e)}.")
            messagebox.showerror("Fehler", "Speichern fehlgeschlagen")
        sys.exit()

    def on_closing(self, *args):
        self.quit_save()

    
    def load(self, *args):
        log.debug("load")
        text = False
        if self.conf.sync_remote:
            try:
                text = self.pull_remote_text()
            except Exception:
                log.warning("sync_remote faild")
                self.qt.statusbar.update_status('cant sync')

        if self.conf.filename:
            with open(self.conf.filename, 'r+') as f:
                text_local = f.read()

                if text:
                    if text != text_local:
                        log.warning("diffrences in remote: /local:")
                        log.info(text)
                        log.info(text_local)

                        text += "\n>>>>>>>>>>> remote /\ | \/ local <<<<<<<<<<<<<\n" + text_local
                        self.qt.statusbar.update_status('cant sync')
                else:
                    log.info("load local")
                    text = text_local
            
        self.qt.clear_and_replace_textarea(text)
    
    def pull_remote_text(self) -> str:
        log.debug("pull_remote_text")
        from firebase import Firebase
        db = Firebase(self.fb_config).database()
        return db.get().val()
        

    def push_remote_text(self):
        log.debug("push_remote_text")
        from firebase import Firebase
        db = Firebase(self.fb_config).database()
        textarea_content = self.qt.textarea.get(1.0, tk.END)
        db.set(textarea_content)
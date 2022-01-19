from quiet_config import Configurations


class SyntaxHighlighting():

    def __init__(self, parent, text_widget, initial_content):
        self.parent = parent
        self.text = text_widget
        self.previous_content = initial_content

        self.theme = Configurations.Theme
        self.pattern = Configurations.Patterns

    def default_highlight(self):
        content = self.text.get("1.0", "end-1c")

        if (self.previous_content != content):
           self.highlight()
    
    def highlight(self):    
        self.text.clear_highlight()
        
        for p in self.pattern.patternmovelist:
            self.text.pattern_move(
                p.regex, 
                p.token, 
                regexp=True)

        for p in self.pattern.patternlist:
            self.text.pattern_highlight(
                p.regex, 
                p.token, 
                regexp=True)

    def initial_highlight(self, *args):
        self.clear_existing_tags()

        for p in self.pattern.patternlist:
            self.text.tag_configure(p.token, **p.styledict)

        self.highlight()

    def clear_existing_tags(self):
        for tag in self.text.tag_names():
            self.text.tag_delete(tag)



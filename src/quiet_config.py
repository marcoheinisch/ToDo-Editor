class Configurations:
    class Settings:
        autoclose_squarebrackets= True
        autoclose_parentheses= True
        autoclose_curlybraces= True
        autoclose_doublequotes= True
        autoclose_singlequotes= True
        current_line_indicator= True
        current_line_indicator_symbol= ':'
        font_family= "consolas"
        font_size= 11
        horizontal_scrollbar_show= 'false'
        insertion_blink= 300 #or 0
        tab_size= 3
        text_bottom_lineheight= '6'
        text_top_lineheight= '0'
        text_wrap= None
        border= 0
        padding_x= '5'
        padding_y= '5'
        theme= "data\theme_configs/theme.yaml"
        vertical_scrollbar_show= True
        web_browser= "chromium"
        filename= "quiet_note.txt"
        sync_remote= False
        #TODO: change key handeling
        sync_fb_key={
            'apiKey': "",
            'authDomain': "",
            'databaseURL': "",
            'projectId': "",
            'storageBucket': "",
            'messagingSenderId': "",
            'appId': "",
            'measurementId': ""
        }

    class Theme:
        comment_color= '#6A737D'
        string_color= '#032F62'
        number_color= '#005CC5'
        type_color= '#005CC5'
        keyword_color= '#D73A49'
        operator_color= '#D73A49'
        bultin_function_color= '#D73A49'
        class_self_color= '#24292E'
        namespace_color= '#D73A49'
        class_name_color= '#E36209'
        function_name_color= '#E36209'
        font_color= '#24292E'
        font_color_linenumbers= '#a4a9aE'
        bg_color= '#FFFFFF'
        menu_fg_active= '#24292E'
        menu_bg_active= '#c1d9e3'
        selection_color= '#c1d9e3'
        
        insertion_color = '#eb4034'
        s_bg_color = '#eb4034'
        s_font_color = '#eb4034'
        text_selection_bg_clr = '#eb4034'
        troughx_clr = '#242222'
        troughy_clr = '#242222'
        menubar_bg_active = '#eb4034'
        menubar_fg_active = '#eb4034'
        menu_fg = '#eb4034'
        menu_bg = '#eb4034'
   
    class Patterns:
        class _Pattern:
            def __init__(self, regex, token, styledict) -> None:
                self.regex = regex
                self.token = token
                self.styledict = styledict
        patternlist = [
            _Pattern(r"(\d\d\:\d\d)", 
                'Token.Time', 
                {'foreground':'#0055c2'}),
            _Pattern(r"(\d\d\.\d\d\.(\d\d(\d\d)?)?)", 
                'Token.Date', 
                {'foreground':'#0055c2'}),
            _Pattern(r"(==.*)",
                'Token.Headers',
                {'foreground':'#D73A49'}),
            _Pattern(r"(>.*)", 
                'Token.Fade.Waiting', 
                {'foreground':'#c0c0c0'}),
            _Pattern(r"(<.*)", 
                'Token.Fade.Next', 
                {'foreground':'#808080'}),
            _Pattern(r"(\t?x  [^\n]*?\n)", 
                'Token.Done', 
                {'foreground':'#e0e0e0', 'overstrike':'True'})]




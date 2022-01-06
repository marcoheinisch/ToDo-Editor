import os
from pygments.lexers import (PythonLexer, RustLexer, CLexer, CppLexer, JavaLexer, MarkdownLexer, CssLexer,
         GoLexer, DockerLexer, YamlLexer, JavascriptLexer, HtmlDjangoLexer, SqlLexer, SwiftLexer,
         CoffeeScriptLexer, DartLexer, HaskellLexer, NimrodLexer, BatchLexer, CSharpLexer)

class SyntaxAndThemes:

		def __init__(self, master):

			self.master = master
			self.githubly_theme_path = master.parent.loader.resource_path(
				os.path.join('data', 'theme_configs/githubly.yaml'))
			self.dracula_theme_path = master.parent.loader.resource_path(
				os.path.join('data', 'theme_configs/dracula.yaml'))

			self.default_theme_path = self.githubly_theme_path

		def load_default(self):
			self.master.load_new_theme(self.default_theme_path)

		def load_githubly(self):
			self.master.load_new_theme(self.githubly_theme_path)

		def load_dracula(self):
			self.master.load_new_theme(self.dracula_theme_path)

		def load(self):
			self.master.lexer = MarkdownLexer()
			self.master.initial_highlight()

		def save_theme_to_config(self, path):
			loader = self.master.parent.loader
			data = loader.load_settings_data()
			data["theme"] = path

			#loader.store_settings_data(data)

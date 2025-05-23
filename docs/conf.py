# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Path extension
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))
print(sys.path[0])
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = 'CatMatcher'
copyright = '2025, A. Rottensteiner'
author = 'A. Rottensteiner'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'nbsphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


autodoc_typehints = "description"

def skip_dataclass_fields(app, what, name, obj, skip, options):
    # Skip dataclass fields to avoid duplicate docs
    dataclass_fields = {
        "file_list", "file_path", "match_radius", "match_values", "output_mode",
        "output_file_name", "command_file_name", "cwd", "matcher", "multimode",
        "join_mode", "runner", "progress", "fixcols", "reference_file",
        "suffix_list", "iref", "input_command", "output_command", "ifmt", "ofmt"
    }
    if name in dataclass_fields:
        return True
    return skip

def setup(app):
    app.connect("autodoc-skip-member", skip_dataclass_fields)


from sphinx.highlighting import lexers
from pygments.lexers import PythonLexer

# Map unknown 'ipython2' lexer to PythonLexer (or IPythonLexer if installed)
lexers['ipython2'] = PythonLexer()

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'The JuanBook of Machine Learning'
copyright = '2026, Juan Maroñas Molano'
author = 'Juan Maroñas Molano'


# =========================
# EXTENSIONS
# =========================
extensions = [
    "myst_nb", # markdown plus notebooks
    "sphinx_togglebutton",
    "sphinx.ext.autodoc",
    "sphinxcontrib.bibtex",
    "sphinx.ext.napoleon",      # Google / NumPy docstrings
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",      # source code linke
    "sphinx.ext.todo",          # todo notes
    "sphinx.ext.doctest",     
    "sphinx.ext.duration",
]

myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "colon_fence",
]

togglebutton_hint = "Mostrar código"
togglebutton_hint_hide = "Ocultar código"

togglebutton_selector = ".cell_input"

nitpicky = True
warning_is_error = True

bibtex_bibfiles = ["publications.bib"]

bibtex_default_style = "unsrt"
bibtex_reference_style = "author_year"

# =========================
# FORMATO DE ARCHIVOS
# =========================

# =========================
# MYST-NB (NOTEBOOKS)
# =========================
nb_execution_mode = "auto" #"off"   #off importante: evita ejecutar notebooks al build
nb_merge_streams = True
nb_execution_allow_errors = True
nb_kernel_name = "temario_ml"
nb_execution_excludepatterns = []
nb_render_markdown_format = "myst"  # so display(Markdown(...)) outputs (e.g. _macros.md) get $$...$$ math processed, not left as literal text
nb_execution_timeout = 120

# =========================
# HTML THEME (recomendado)
# =========================
html_theme = "sphinx_book_theme"
html_sidebars = {
    "index": []
}
html_static_path = ["_static"]
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css",
]

html_theme_options = {
    "home_page_in_toc": True,
    "show_toc_level": 10
}

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
templates_path = ['_templates']
exclude_patterns = [
    "book_content/_macros.md",
    "book_content/linear_models/theory/notes_normalization_conditioning.md",
    "book_content/linear_models/theory/notes_ols_consistency.md",
    "book_content/clustering/**",
    "book_content/notes_video_animation_optimization.md",
    "book_content/math/optimization/OPTIMIZATION_SESSION_NOTES.md",
    "book_content/AUDIT_INSTRUCTIONS.md",
    # --- TEMPORARY: first minimal deploy test, index page only, remove once book_content is ready ---
    "book_content/**",
    # --- END TEMPORARY ---
]

# =========================
# API DOC
# =========================
'''
autodoc_default_options = {
    'members': True,
    #'undoc-members': True,  # Non documented members
    'private-members': True,  # private members
    'special-members': True,  # special methods like __init__
}
'''


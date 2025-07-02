# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------
project = "Data Profiling CLI"
author = "Roy Kensmil"
release = "0.1.4"  # match your pyproject.toml

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",  # API generation from docstrings
    "sphinx.ext.napoleon",  # Google/NumPy style docstrings
    "sphinx.ext.viewcode",  # add links to highlighted source
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"

# Theme-specific options
html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "logo_only": False,
}

# Static files (e.g., style sheets) path
html_static_path = ["_static"]

# Optional: Add a logo and favicon if available
# html_logo = "_static/logo.png"
# html_favicon = "_static/favicon.ico"

# Show GitHub link in the theme
html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": "rkendev",  # Username
    "github_repo": "dataprof",  # Repo name
    "github_version": "main/docs/source",  # Path in the repo
    "conf_py_path": "/docs/source/",  # Path to docs root
}

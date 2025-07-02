import sphinx_rtd_theme

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
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ["_static"]

# Show "Edit on GitHub" links in the sidebar
html_context = {
    "display_github": True,
    "github_user": "rkendev",
    "github_repo": "dataprof",
    "github_version": "main/docs/source/",
    "conf_py_path": "/docs/source/",
}

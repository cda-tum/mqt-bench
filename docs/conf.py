"""Sphinx configuration file."""

from __future__ import annotations

import warnings
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()


try:
    version = metadata.version("mqt.bench")
except ModuleNotFoundError:
    msg = (
        "Package should be installed to produce documentation! "
        "Assuming a modern git archive was used for version discovery."
    )
    warnings.warn(msg, stacklevel=1)

    from setuptools_scm import get_version

    version = get_version(root=str(ROOT), fallback_root=ROOT)

# Filter git details from version
release = version.split("+")[0]

project = "MQT Bench"
author = "Chair for Design Automation, Technical University of Munich"
language = "en"
project_copyright = "2023, Chair for Design Automation, Technical University of Munich"

extensions = [
    "myst_parser",
    "sphinx.ext.intersphinx",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinxext.opengraph",
]

source_suffix = [".rst", ".md"]

exclude_patterns = [
    "_build",
    "**.ipynb_checkpoints",
    "Thumbs.db",
    ".DS_Store",
    ".env",
    ".venv",
]

pygments_style = "colorful"

add_module_names = False

modindex_common_prefix = ["mqt.bench."]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "qiskit": ("https://qiskit.org/documentation/", None),
    "mqt": ("https://mqt.readthedocs.io/en/latest/", None),
}
intersphinx_disabled_reftypes = ["*"]

myst_enable_extensions = [
    "colon_fence",
    "substitution",
    "deflist",
]

myst_substitutions = {
    "version": version,
}

copybutton_prompt_text = r"(?:\(venv\) )?(?:\[.*\] )?\$ "
copybutton_prompt_is_regexp = True
copybutton_line_continuation_character = "\\"

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]
html_theme_options = {
    "light_logo": "mqt_dark.png",
    "dark_logo": "mqt_light.png",
    "source_repository": "https://github.com/cda-tum/mqt-bench/",
    "source_branch": "main",
    "source_directory": "docs/",
    "navigation_with_keys": True,
}

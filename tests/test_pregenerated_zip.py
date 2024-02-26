from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from mqt.benchviewer import Backend, BenchmarkConfiguration, Server
from mqt.benchviewer.main import app
from mqt.bench import utils

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):  # pragma: no cover
    from importlib import resources
else:
    import importlib_resources as resources



def test_flask_server_with_pregenerated_zip() -> None:
    benchviewer = resources.files("mqt.benchviewer")
    with resources.as_file(benchviewer) as benchviewer_path:
        benchviewer_location = benchviewer_path

    Server(
        skip_question=True,
        activate_logging=False,
        target_location=str(utils.get_zip_file_path()),
    )

    paths_to_check = [
        "static/files/MQTBench_all.zip",
        "templates/benchmark_description.html",
        "templates/index.html",
        "templates/legal.html",
        "templates/description.html",
    ]
    for path in paths_to_check:
        assert (benchviewer_location / path).is_file()

    with app.test_client() as c:
        success_code = 200
        links_to_check = [
            "/mqtbench/index",
            "/mqtbench/download",
            "/mqtbench/legal",
            "/mqtbench/description",
            "/mqtbench/benchmark_description",
        ]
        for link in links_to_check:
            assert c.get(link).status_code == success_code

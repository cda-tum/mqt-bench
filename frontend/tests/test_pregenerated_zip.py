"""Test the Flask server with the pregenerated zip file."""

from __future__ import annotations

import os
from importlib import resources

import pytest

from mqt.bench import utils
from mqt.bench.viewer import Server
from mqt.bench.viewer.main import app

# only run test when executed on GitHub runner
IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.mark.skipif(not IN_GITHUB_ACTIONS, reason="Only run this test on GitHub runner")
def test_flask_server_with_pregenerated_zip() -> None:
    """Test the Flask server with the pregenerated zip file."""
    benchviewer = resources.files("mqt.bench.viewer")
    with resources.as_file(benchviewer) as benchviewer_path:
        benchviewer_location = benchviewer_path

    Server(
        skip_question=True,
        activate_logging=False,
        target_location=str(utils.get_zip_folder_path()),
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

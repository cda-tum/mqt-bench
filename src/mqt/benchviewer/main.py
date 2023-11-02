from __future__ import annotations

import logging
import os
import sys
from datetime import datetime
from typing import TYPE_CHECKING

from flask import Flask, cli, jsonify, render_template, request, send_from_directory

from mqt.benchviewer.backend import Backend

if TYPE_CHECKING or sys.version_info < (3, 10, 0):  # pragma: no cover
    import importlib_resources as resources
else:
    from importlib import resources

if TYPE_CHECKING:  # pragma: no cover
    from flask import Response


class Server:
    def __init__(
        self,
        target_location: str,
        skip_question: bool = False,
        activate_logging: bool = False,
    ):
        self.backend = Backend()

        self.target_location = target_location
        if not os.access(self.target_location, os.W_OK):
            msg = "target_location is not writable. Please specify a different path."
            raise RuntimeError(msg)

        res_zip = self.backend.read_mqtbench_all_zip(self.target_location, skip_question)
        if not res_zip:
            msg = "Error while reading the MQTBench_all.zip file."
            raise RuntimeError(msg)
        self.backend.init_database()
        if self.backend.database is None:
            msg = "Error while initializing the database."
            raise RuntimeError(msg)

        self.activate_logging = activate_logging

        if self.activate_logging:
            logging.basicConfig(filename="/local/mqtbench/downloads.log", level=logging.INFO)
        global SERVER  # noqa: PLW0603
        SERVER = self


app = Flask(__name__, static_url_path="/mqtbench")
SERVER: Server = None  # type: ignore[assignment]
PREFIX = "/mqtbench/"


@app.route(f"{PREFIX}/", methods=["POST", "GET"])
@app.route(f"{PREFIX}/index", methods=["POST", "GET"])
def index() -> str:
    """Return the index.html file together with the benchmarks and nonscalable benchmarks."""
    return render_template(
        "index.html",
        benchmarks=SERVER.backend.benchmarks,
        nonscalable_benchmarks=SERVER.backend.nonscalable_benchmarks,
    )


@app.route(f"{PREFIX}/get_pre_gen", methods=["POST", "GET"])
def download_pre_gen_zip() -> Response:
    filename = "MQTBench_all.zip"

    if SERVER.activate_logging:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        app.logger.info("###### Start ######")
        app.logger.info("Timestamp: %s", timestamp)
        headers = str(request.headers)
        headers = headers.replace("\r\n", "").replace("\n", "")
        app.logger.info("Headers: %s", headers)
        app.logger.info("Download of pre-generated zip")
        app.logger.info("###### End ######")

    return send_from_directory(
        SERVER.target_location,
        filename,
        as_attachment=True,
        mimetype="application/zip",
        download_name="MQTBench_all.zip",
    )


@app.route(f"{PREFIX}/download", methods=["POST", "GET"])
def download_data() -> str | Response:
    """Triggers the downloading process of all benchmarks according to the user's input."""
    if request.method == "POST":
        data = request.form
        prepared_data = SERVER.backend.prepare_form_input(data)
        file_paths = SERVER.backend.get_selected_file_paths(prepared_data)
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        if SERVER.activate_logging:
            app.logger.info("###### Start ######")
            app.logger.info("Timestamp: %s", timestamp)
            headers = str(request.headers)
            headers = headers.replace("\r\n", "").replace("\n", "")
            app.logger.info("Headers: %s", headers)
            app.logger.info("Prepared_data: %s", prepared_data)
            app.logger.info("Download started: %s", len(file_paths))
            app.logger.info("###### End ######")

        if file_paths:
            return app.response_class(  # type: ignore[no-any-return]
                SERVER.backend.generate_zip_ephemeral_chunks(file_paths),
                mimetype="application/zip",
                headers={"Content-Disposition": f'attachment; filename="MQTBench_{timestamp}.zip"'},
                direct_passthrough=True,
            )

    return render_template(
        "index.html",
        benchmarks=SERVER.backend.benchmarks,
        nonscalable_benchmarks=SERVER.backend.nonscalable_benchmarks,
    )


@app.route(f"{PREFIX}/legal")
def legal() -> str:
    """Return the legal.html file."""

    return render_template("legal.html")


@app.route(f"{PREFIX}/description")
def description() -> str:
    """Return the description.html file in which the file formats are described."""

    return render_template("description.html")


@app.route(f"{PREFIX}/benchmark_description")
def benchmark_description() -> str:
    """Return the benchmark_description.html file together in which all benchmark algorithms
    are described in detail.
    """

    return render_template("benchmark_description.html")


@app.route(f"{PREFIX}/get_num_benchmarks", methods=["POST"])
def get_num_benchmarks() -> Response:
    if request.method == "POST":
        data = request.form
        prepared_data = SERVER.backend.prepare_form_input(data)
        file_paths = SERVER.backend.get_selected_file_paths(prepared_data)
        return jsonify({"num_selected": len(file_paths)})  # type: ignore[no-any-return]
    return jsonify({"num_selected": 0})  # type: ignore[no-any-return]


def start_server(
    skip_question: bool = False,
    activate_logging: bool = False,
    target_location: str | None = None,
    debug_flag: bool = False,
) -> None:
    if not target_location:
        target_location = str(resources.files("mqt.benchviewer") / "static" / "files")

    Server(
        target_location=target_location,
        skip_question=skip_question,
        activate_logging=activate_logging,
    )
    print(
        "Server is hosted at: http://127.0.0.1:5000" + PREFIX + ".",
        "To stop it, interrupt the process (e.g., via CTRL+C). \n",
    )

    # This line avoid the startup-message from flask
    cli.show_server_banner = lambda *_args: None

    if not activate_logging:
        log = logging.getLogger("werkzeug")
        log.disabled = True

    app.run(debug=debug_flag)


if __name__ == "__main__":
    start_server()

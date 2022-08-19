from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_from_directory,
)
from mqt.benchviewer.src.backend import *
from datetime import datetime
import logging

app = Flask(__name__)
PREFIX = "/mqtbench/"


def init(
    skip_question=False,
    activate_logging=False,
    target_location: str = "mqt/benchviewer/static/files/qasm_output",
):
    read_mqtbench_all_zip(skip_question, target_location)
    init_database()

    global ACTIVATE_LOGGING
    ACTIVATE_LOGGING = activate_logging

    if ACTIVATE_LOGGING:
        logging.basicConfig(
            filename="/local/mqtbench/downloads.log", level=logging.INFO
        )


@app.route(f"{PREFIX}/", methods=["POST", "GET"])
@app.route(f"{PREFIX}/index", methods=["POST", "GET"])
def index():
    """Return the index.html file together with the benchmarks and nonscalable benchmarks."""

    return render_template(
        "index.html",
        benchmarks=benchmarks,
        nonscalable_benchmarks=nonscalable_benchmarks,
    )


@app.route(f"{PREFIX}/get_pre_gen", methods=["POST", "GET"])
def download_pre_gen_zip():
    directory = "./static/files/qasm_output/"
    filename = "MQTBench_all.zip"

    if ACTIVATE_LOGGING:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        app.logger.info("###### Start ######")
        app.logger.info("Timestamp: %s", timestamp)
        app.logger.info("Headers: %s", request.headers)
        app.logger.info("Download of pre-generated zip")
        app.logger.info("###### End ######")

    return send_from_directory(
        directory=directory,
        path=filename,
        as_attachment=True,
        mimetype="application/zip",
        download_name="MQTBench_all.zip",
    )


@app.route(f"{PREFIX}/download", methods=["POST", "GET"])
def download_data():
    """Triggers the downloading process of all benchmarks according to the user's input."""
    if request.method == "POST":
        data = request.form
        prepared_data = prepareFormInput(data)
        print("raw data :", data)
        print("prepared input data :", prepared_data)
        file_paths = get_selected_file_paths(prepared_data)
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        if ACTIVATE_LOGGING:
            app.logger.info("###### Start ######")
            app.logger.info("Timestamp: %s", timestamp)
            app.logger.info("Headers: %s", request.headers)
            app.logger.info("Prepared_data: %s", prepared_data)
            app.logger.info("Download started: %s", len(file_paths))
            app.logger.info("###### End ######")

        if file_paths:
            return app.response_class(
                generate_zip_ephemeral_chunks(file_paths),
                mimetype="application/zip",
                headers={
                    "Content-Disposition": 'attachment; filename="MQTBench_{}.zip"'.format(
                        timestamp
                    )
                },
                direct_passthrough=True,
            )

    return render_template(
        "index.html",
        benchmarks=benchmarks,
        nonscalable_benchmarks=nonscalable_benchmarks,
    )


@app.route(f"{PREFIX}/legal")
def legal():
    """Return the legal.html file."""

    return render_template("legal.html")


@app.route(f"{PREFIX}/description")
def description():
    """Return the description.html file in which the file formats are described."""

    return render_template("description.html")


@app.route(f"{PREFIX}/benchmark_description")
def benchmark_description():
    """Return the benchmark_description.html file together in which all benchmark algorithms
    are described in detail.
    """

    return render_template("benchmark_description.html")


@app.route(f"{PREFIX}/get_num_benchmarks", methods=["POST"])
def get_num_benchmarks():

    if request.method == "POST":
        data = request.form
        prepared_data = prepareFormInput(data)
        file_paths = get_selected_file_paths(prepared_data)
        num = len(file_paths)
        print("Num benchmarks: ", num)
        data = {"num_selected": num}
        return jsonify(data)
    else:
        data = {"num_selected": 0}

        return jsonify(data)


def start_server(skip_question=False, activate_logging=False):
    init(skip_question=skip_question, activate_logging=activate_logging)
    print("Server is hosted at: ", "http://127.0.0.1:5000" + PREFIX)
    app.run(debug=False)


if __name__ == "__main__":
    start_server()

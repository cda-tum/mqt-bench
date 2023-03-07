from __future__ import annotations

import sys
import io
from typing import TYPE_CHECKING

import pytest
from pathlib import Path
from mqt.benchviewer import Backend
import zipfile

if TYPE_CHECKING or sys.version_info >= (3, 10, 0):
    from importlib import resources
else:
    import importlib_resources as resources


def test_NoSeekBytesIO():

    test_qasm_output = Path("test.qasm")
    test_qasm_output.write_bytes(b"test")
    test_qasm_output2 = Path("test2.qasm")
    test_qasm_output2.write_bytes(b"test")

    zip_path = Path("test.zip")
    with zipfile.ZipFile(str(zip_path), 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(test_qasm_output)
        zipf.write(test_qasm_output2)

    filenames = ["test2.qasm"]
    fileobj = Backend.NoSeekBytesIO(io.BytesIO())

    with zip_path.open("rb") as zf:
        zip_bytes = io.BytesIO(zf.read())
        test_zip = zipfile.ZipFile(zip_bytes, mode="r")

    with zipfile.ZipFile(fileobj, mode="w") as zf:
        for individual_file in filenames:
            individual_file_as_path = Path(individual_file)
            zf.writestr(
                individual_file_as_path.name,
                data=test_zip.read(individual_file_as_path.name),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=3,
            )
            fileobj.hidden_seek(0)
            assert fileobj.read() == b"test"
            fileobj.truncate_and_remember_offset(0)

    fileobj.hidden_seek(0)
    fileobj.read()
    fileobj.close()

    test_qasm_output.unlink()
    test_qasm_output2.unlink()
    zip_path.unlink()


def test_backend_streaming():
    backend = Backend()
    backend.read_mqtbench_all_zip()
    assert backend.generate_zip_ephemeral_chunks(filenames=["ghz_indep_qiskit_16.qasm"])
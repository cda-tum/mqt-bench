"""
Utility script to convert IBM Quantum CSV calibration data to a structured JSON format.
This script retrieves remote backend information from IBM Quantum, processes qubit properties
from a CSV file, and combines them into a comprehensive JSON file.
"""

import csv
import json
import sys
from qiskit_ibm_runtime import QiskitRuntimeService
from pathlib import Path
import os
from typing import Dict, Any


def get_remote_information(backend_name: str) -> Dict[str, Any]:
    """
    Retrieves the remote backend information from IBM Quantum.

    This includes backend details like name, number of qubits, basis gates, and connectivity.

    Args:
        backend_name (str): Name of the quantum backend to retrieve information for.

    Returns:
        Dict[str, Any]: A dictionary containing backend information (name, number of qubits, basis gates, and connectivity).
    """
    service = QiskitRuntimeService(instance="ibm-q/open/main")
    backend = service.backend(backend_name)

    # Use coupling_map directly (it is already JSON serializable)
    coupling_map = list(backend.coupling_map)

    gates = backend.basis_gates.copy()
    gates.append("measure")  # Add the 'measure' gate
    gates.append("barrier")  # Add the 'barrier' gate

    # Extract backend information
    backend_info = {
        "name": backend_name,
        "num_qubits": backend.num_qubits,
        "basis_gates": gates,
        "connectivity": coupling_map  # Already a list of lists
    }

    return backend_info


def parse_ecr_errors(ecr_str: str) -> Dict[str, float]:
    """
    Parses a string of ECR gate errors or gate time values into a dictionary.

    Each pair in the string is separated by a semicolon, with each key-value pair separated by a colon.

    Args:
        ecr_str (str): A string representing ECR error or gate time, in the format 'key:value;key:value...'.

    Returns:
        Dict[str, float]: A dictionary where the keys are the ECR error or gate time names and the values are floats.
    """
    ecr_dict = {}
    if ecr_str:
        pairs = ecr_str.split(';')
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':')
                ecr_dict[key] = float(value)
    return ecr_dict


def process_csv(input_file: str) -> Dict[str, Any]:
    """
    Processes a CSV file containing qubit properties and converts it into a structured dictionary.

    Each row in the CSV corresponds to a qubit, and the columns represent different properties.

    Args:
        input_file (str): Path to the CSV file to be processed.

    Returns:
        Dict[str, Any]: A dictionary containing qubit properties.
    """
    properties = {}

    input_path = Path(input_file)
    with input_path.open(mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            qubit_id = row["Qubit"].strip('"')

            # Extract and convert numeric values
            t1 = float(row["T1 (us)"])
            t2 = float(row["T2 (us)"])
            ero = float(row["Readout assignment error "])
            tro = float(row["Readout length (ns)"])
            eid = float(row["ID error "])
            esx = float(row["√x (sx) error "])
            ex = float(row["Pauli-X error "])

            # Parse ECR error and gate time
            eecr = parse_ecr_errors(row["ECR error "])
            tecr = parse_ecr_errors(row["Gate time (ns)"])

            # Add the qubit's properties to the dictionary
            properties[qubit_id] = {
                "T1": t1,
                "T2": t2,
                "eRO": ero,
                "tRO": tro,
                "eID": eid,
                "eSX": esx,
                "eX": ex,
                "eECR": eecr,
                "tECR": tecr
            }

    return properties


def extract_backend_name_from_filename(filename: str) -> str:
    """
    Extracts the backend name from a CSV filename.

    The backend name is assumed to be the part of the filename before the first underscore.

    Args:
        filename (str): The filename of the CSV.

    Returns:
        str: The extracted backend name.

    Raises:
        ValueError: If the filename does not contain enough underscores to extract the backend name.
    """
    base_name = os.path.basename(filename)
    parts = base_name.split('_')
    if len(parts) < 2:
        raise ValueError("Filename does not contain expected underscores to extract backend name.")
    backend_name = f"{parts[0]}_{parts[1]}"
    return backend_name


def main() -> None:
    """
    The main function of the script.

    It expects a CSV file path as a command-line argument, extracts the backend name,
    processes the file, and writes the backend information along with the qubit properties to a JSON file.
    """
    # Ensure exactly one command-line argument is provided
    if len(sys.argv) != 2:
        print("Usage: python ibm_csv_to_mqt_json.py <input_csv_file>")
        sys.exit(1)

    input_csv = sys.argv[1]

    try:
        # Automatically extract the backend name from the CSV file name
        backend_name = extract_backend_name_from_filename(input_csv)
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)

    # Fetch backend information
    try:
        backend_info = get_remote_information(backend_name)
    except Exception as e:
        print(f"Failed to retrieve backend information: {e}")
        sys.exit(1)

    # Process the CSV file to get qubit properties
    try:
        qubit_properties = process_csv(input_csv)
    except Exception as e:
        print(f"Failed to process CSV file: {e}")
        sys.exit(1)

    # Combine backend information with qubit properties
    output_data = backend_info
    output_data["properties"] = qubit_properties

    # Write the processed data to a JSON file named <backend_name>_calibration.json
    output_filename = f"{backend_name}_calibration.json"
    output_path = Path(output_filename)
    try:
        with output_path.open('w', encoding='utf-8') as json_file:
            json.dump(output_data, json_file, indent=4)
        print(f"Data successfully written to {output_filename}")
    except Exception as e:
        print(f"Failed to write JSON file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

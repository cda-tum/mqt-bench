import csv
import json
import sys

def parse_ecr_errors(ecr_str):
    """
    Parses a string of ECR gate errors or gate time values
    into a dictionary. Each pair in the string is separated by a semicolon,
    with each key-value pair separated by a colon.

    Args:
        ecr_str (str): A string representing ECR error or gate time,
                       in the format 'key:value;key:value...'.

    Returns:
        dict: A dictionary where the keys are the ECR error or gate time names
              and the values are floats representing the errors or times.
    """
    ecr_dict = {}
    if ecr_str:
        # Split the string into key-value pairs
        pairs = ecr_str.split(';')
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':')
                ecr_dict[key] = float(value)  # Convert values to float
    return ecr_dict

def process_csv(input_file):
    """
    Processes a CSV file containing qubit properties and converts it into a
    structured dictionary. Each row in the CSV corresponds to a qubit, and the
    columns represent different properties of the qubit.

    Args:
        input_file (str): Path to the CSV file to be processed.

    Returns:
        dict: A dictionary containing qubit properties. Each qubit is identified
              by a unique ID, and its associated properties (T1, T2, errors, etc.)
              are stored as key-value pairs.
    """
    properties = {}  # Dictionary to hold qubit properties

    with open(input_file, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Reads the CSV file into a dictionary format
        for row in reader:
            qubit_id = row["Qubit"].strip('"')  # Extract the qubit ID and remove quotes

            # Extract and convert numeric values
            T1 = float(row["T1 (us)"])
            T2 = float(row["T2 (us)"])
            eRO = float(row["Readout assignment error "])
            tRO = float(row["Readout length (ns)"])
            eID = float(row["ID error "])
            eSX = float(row["√x (sx) error "])
            eX = float(row["Pauli-X error "])

            # Parse ECR error and gate time (may contain multiple values)
            eecr = parse_ecr_errors(row["ECR error "])
            tecr = parse_ecr_errors(row["Gate time (ns)"])

            # Add the qubit's properties to the dictionary
            properties[qubit_id] = {
                "T1": T1,
                "T2": T2,
                "eRO": eRO,
                "tRO": tRO,
                "eID": eID,
                "eSX": eSX,
                "eX": eX,
                "eECR": eecr,
                "tECR": tecr
            }

    # Structure of the output dictionary
    output = {
        "properties": properties
    }

    return output

def main():
    """
    The main function of the script. It expects a CSV file path as a command-line
    argument, processes the file, and prints the result in JSON format. The script
    will exit if no input file is provided.

    Usage: python parse_qubits.py input.csv
    """
    # Ensure exactly one command-line argument is provided
    if len(sys.argv) != 2:
        print("Usage: python parse_qubits.py input.csv")
        sys.exit(1)

    input_csv = sys.argv[1]  # Get the input CSV file path from command-line arguments
    output_data = process_csv(input_csv)  # Process the CSV file

    # Output the processed data as pretty-printed JSON
    print(json.dumps(output_data, indent=4))

if __name__ == "__main__":
    main()

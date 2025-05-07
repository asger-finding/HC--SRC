import argparse
import array
import collections
import os
import sys
import csv
from xml.etree import ElementTree as ET
from typing import Dict, List, Tuple

def parse_cmbl(filepath: str, use_double: bool = False) -> List[Tuple[str, Dict[str, array.array]]]:
    """Parse CMBL file and return datasets, handling edge cases."""
    try:
        tree = ET.parse(filepath)
    except ET.ParseError:
        print("Error: Only text-based CMBL files are supported.")
        sys.exit(1)

    datasets = []
    for dataset_ele in tree.getroot().findall("DataSet"):
        dataset_name = dataset_ele.findtext("DataSetName", "").strip() or f"Dataset_{len(datasets)+1}"
        dataset_data = collections.OrderedDict()

        for col_ele in dataset_ele.findall("DataColumn"):
            col_name = col_ele.findtext("DataObjectName", "").strip()
            col_shortname = col_ele.findtext("DataObjectShortName", "").strip()
            col_units = col_ele.findtext("ColumnUnits", "").strip()
            col_cells = col_ele.find("ColumnCells")

            if col_cells is None or not col_cells.text:
                continue

            # Construct header
            header = f"{col_name} ({col_shortname}) [{col_units}]" if col_units else col_name
            if not header:
                header = f"Column_{len(dataset_data)+1}"

            # Parse data
            data = array.array('d' if use_double else 'f')
            for line in col_cells.text.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    data.append(float(line))
                except ValueError:
                    print(f"Warning: Skipping non-numeric value '{line}' in column '{header}'")

            if data:
                dataset_data[header] = data

        if dataset_data:
            datasets.append((dataset_name, dataset_data))

    return datasets

def write_to_csv(datasets: List[Tuple[str, Dict[str, array.array]]], output_path: str) -> None:
    """Write datasets to CSV, avoiding infinite loops."""
    for name, data in datasets:
        csv_path = f"{os.path.splitext(output_path)[0]}_{name}.csv"
        print(f"Writing {len(data)} columns to {csv_path}")

        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data.keys())
            writer.writerows(zip(*data.values()))

def main():
    parser = argparse.ArgumentParser(description="Convert Logger Pro CMBL files to CSV.")
    parser.add_argument("input", help="Input CMBL file path")
    parser.add_argument("-o", "--output", help="Output CSV base name (default: input name)")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("-D", "--double", action="store_true", help="Use double precision")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.exit(f"Error: Input file '{args.input}' not found.")

    output_base = args.output or os.path.splitext(os.path.basename(args.input))[0]
    datasets = parse_cmbl(args.input, args.double)

    if not datasets:
        sys.exit("Error: No valid datasets found in the file.")

    write_to_csv(datasets, output_base)
    print(f"Converted {len(datasets)} datasets.")

if __name__ == "__main__":
    main()


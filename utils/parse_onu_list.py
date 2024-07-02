import argparse

def parse_onu_file(filename):
    """
    Parses a text file containing ONU information and returns a dictionary
    where keys are gpon indices and values are lists of ONU serial numbers.

    Args:
        filename: The path to the text file.

    Returns:
        A dictionary containing gpon information.
    """
    onu_data = {}
    with open(filename, 'r') as file:
        for line in file:
            # Strip whitespace and remove leading/trailing pipes
            data = line.strip().split('|')

            # Skip empty lines or lines that don't have the expected format
            if len(data) < 2:
                continue

            # Extract gpon index and serial number
            gpon_index = data[0].strip().split("/")[1]
            serial_number = data[1].strip()

            # Add serial number to the corresponding gpon index list
            if gpon_index not in onu_data:
                onu_data[gpon_index] = []
            onu_data[gpon_index].append(serial_number)

    return onu_data

def main():
    parser = create_parser()
    args = parser.parse_args()
    onus=parse_onu_file(args.file)
    print(onus)

def create_parser():
    parser = argparse.ArgumentParser()
    parser.formatter_class = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=30)
    parser.add_argument('-f', '--file', help='file', required=True)
    return parser

if __name__ == "__main__":
    main()
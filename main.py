import requests
from glob import glob
import os

import find_handed_off_folders

PRODUCTION_DIR = "D:\\Production"
VSI_EXTENSION = "*.vsi"
BARCODE_LENGTH = 10

def get_barcodes_from_paths(paths):
    """Extract 10-digit barcodes from file paths."""
    return [os.path.basename(path)[-14:-4] for path in paths]

def fetch_workflow_state(barcode):
    """Fetch workflow state from LIMS for a given barcode."""
    url = 'https://lims2.corp.alleninstitute.org/slides/info/details.json'
    try:
        response = requests.get(url, params={"barcode": barcode}, timeout=10)
        response.raise_for_status()
        lims_info = response.json()
        return lims_info.get("workflow_state", "UNKNOWN")
    except Exception as e:
        print(f"Error fetching workflow state for {barcode}: {e}")
        return "ERROR"

def main():
    """Main function to find and print 'Handed off' folders in the Production directory."""
    handed_off_folders = find_handed_off_folders.find_handed_off_folders(PRODUCTION_DIR)
    barcode_status_dict = {}

    for folder in handed_off_folders:
        print(f"\nSearching {folder}")
        pattern = os.path.join(folder, VSI_EXTENSION)
        paths = glob(pattern)
        #print(f"Found VSI files: {paths}")

        barcodes_to_check = get_barcodes_from_paths(paths)
        #print(f"Barcodes to check: {barcodes_to_check}")

        for barcode in barcodes_to_check:
            workflow_state = fetch_workflow_state(barcode)
            print(f"{barcode}'s workflow state is {workflow_state}")
            barcode_status_dict[barcode] = workflow_state

if __name__ == "__main__":
    main()


import os
from pathlib import Path

def find_handed_off_folders(production_path):
    """
    Find all 'Handed off' folders at the same depth: Production > [project] > Handed off
    
    Args:
        production_path (str): Path to the Production folder
    
    Returns:
        list: List of Path objects pointing to 'Handed off' folders
    """
    production_dir = Path(production_path)
    handed_off_folders = []
    
    # Check if Production directory exists
    if not production_dir.exists() or not production_dir.is_dir():
        print(f"Production directory not found: {production_path}")
        return handed_off_folders
    
    # Iterate through project folders (direct children of Production)
    for project_folder in production_dir.iterdir():
        if project_folder.is_dir():
            # Look for 'Handed off' folder inside each project
            handed_off_path = project_folder / "Handed off"
            if handed_off_path.exists() and handed_off_path.is_dir():
                handed_off_folders.append(handed_off_path)
    
    return handed_off_folders

# Example usage
if __name__ == "__main__":
    # Replace with your actual Production folder path
    production_path = "D:\Production"
    
    #Get list of folders
    handed_off_folders = find_handed_off_folders(production_path)
    
    for folder in handed_off_folders:
        print(folder)
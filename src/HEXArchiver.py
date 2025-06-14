import os
import re
import shutil

# Root folder where organized files will be stored
ROOT_FOLDER = "DATA"

ascii_art = r"""
    __  __  ______ _  __ ___              __    _                
   / / / / / ____/| |/ //   |  __________/ /_  (_)   _____  _____
  / /_/ / / __/   |   // /| | / ___/ ___/ __ \/ / | / / _ \/ ___/
 / __  / / /____ /   |/ ___ |/ /  / /__/ / / / /| |/ /  __/ /    
/_/ /_(_)_____(_)_/|_/_/  |_/_/   \___/_/ /_/_/ |___/\___/_/                                                                       
v1.0.0 - HEXLogger File Organizer 
Created by Husamettin Eken                                                             
"""
print(ascii_art)
# Regex pattern to capture config name and date
# Allows additional suffixes after the timestamp (e.g., "-Data2-fail", "_retry", etc.)
FILENAME_PATTERN = re.compile(
    r"(?P<config>.+?)-(?P<date>\d{4}_\d{2}_\d{2})_\d{2}_\d{2}_\d{2}.*\.bin$", re.IGNORECASE
)

# List files in the current directory
for filename in os.listdir("."):
    # Skip folders
    if not os.path.isfile(filename):
        continue

    # Try matching the pattern
    match = FILENAME_PATTERN.match(filename)
    if not match:
        continue

    config_name = match.group("config")
    date_str = match.group("date")

    # Build target directory path: DATA/ConfigName/YYYY_MM_DD/
    target_dir = os.path.join(ROOT_FOLDER, config_name, date_str)
    os.makedirs(target_dir, exist_ok=True)

    # Full destination path
    target_path = os.path.join(target_dir, filename)

    try:
        shutil.move(filename, target_path)
        print(f"Moved: {filename} -> {target_path}")
    except Exception as e:
        print(f"Failed to move {filename}: {e}")
        
input("Press Enter to exit...")
from io import open
import os
import zipfile
from urllib import request

from LST_AI.config import LST_AI_DIR, ATLAS_DIR, MODELS_DIR, BINARIES_DIR

def maybe_download_data():
    """
    Downloads required model weights, binaries and atlas files for usage.
    """
    url = "https://github.com/CompImg/LST-AI/releases/download/v1.0.0/lst_data.zip"

    target_path = "lst_data.zip"
    extract_path = LST_AI_DIR  # This is the base directory.

    paths_to_check = [ATLAS_DIR, MODELS_DIR, BINARIES_DIR]

    # Check if all paths exist.
    if not all(os.path.exists(path) for path in paths_to_check):
        print("Downloading data...")
        # Download the zip file if it doesn't exist.
        if not os.path.exists(target_path):
            with request.urlopen(url) as response, open(target_path, 'wb') as out_file:
                data = response.read()
                out_file.write(data)

        # Unzip the file to the base directory.
        with zipfile.ZipFile(target_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Remove the ZIP file after extracting its contents.
        os.remove(target_path)
        print("Completed.")

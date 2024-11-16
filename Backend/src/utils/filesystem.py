from io import StringIO
import json
import pandas as pd
import os
from json import dump
import requests


def write_dataset(filename: str, df: pd.DataFrame) -> None:
    """
    Creating or overwriting a file with content.

    filename should not contain a type (.csv, .txt, etc.)
    """
    folder = "src/data"

    file_path = f"{folder}/{filename}.csv"
    df.to_csv(file_path, index=False)

    with open(file_path, "rb") as file:
        os.fsync(file.fileno())

def get_all_dataset_files() -> list:
    """
    Return a list of all dataset files in the data folder.
    """

    folder = "src/data"
    if os.path.exists(folder):
        paths = list(os.listdir(folder))
        paths.remove('.gitkeep')
        paths.remove('output')

        paths = [path.split('.')[0] for path in paths]
        return paths

    return []

def write_info(info_filename: str, metadata: dict) -> None:
    """
    Creating or overwriting a .info file with accompanying content for a dataset.

    filename should not contain type suffix (.info, .etc)
    """
    folder = "src/data/info"
    suffix = "_meta_info.info"

    with open(f"{folder}/{info_filename}{suffix}", 'w') as f:
        dump(metadata, f, indent=4) 

def read_meta_info(file_name: str) -> dict:
    """
    Extracts the JSON structure from a datasets accompanying .info file,  
    returns the parsed JSON data as a dictionary.
    """
    meta_info_suffix = "_meta_info"
    meta_info_path = f"src/data/info/{file_name}{meta_info_suffix}.info" 

    if not os.path.exists(meta_info_path):
        raise FileNotFoundError(f"The file '{meta_info_path}' does not exist.")

    with open(meta_info_path, 'r') as file:
        try:
            meta_info_data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON from file '{meta_info_path}': {e}")

    return meta_info_data

def download_qaqc_source_dataset() -> pd.DataFrame:
    """
    Downloads the qaqc data, returns the .csv file.
    """
    dataset_url = "https://svn.spraakbanken.gu.se/sb-arkiv/pub/trec/swe_qaqc_train.csv"
    response = requests.get(dataset_url)
    if response.status_code == 200:
        csv_content = StringIO(response.content.decode('utf-8'))
        df = pd.read_csv(csv_content)
        return df
    else:
        raise Exception(f"Failed to download QAQC dataset, status code: {response.status_code}")
    

def get_qaqc_info_dict() -> dict:
    """
    Helper that returns a hardcoded info dict for qaqc .info file format.
    """
    info_dict = {
        "labels": {
            "coarse": [
                "LOC",
                "HUM",
                "DESC",
                "ENTY",
                "ABBR",
                "NUM"
            ]
        },
        "description": "labels for the IsBit classifiers operation on the QAQC dataset."
    }
    return info_dict


from io import StringIO
import json
import os
import pandas as pd
import requests


def get_all_dataset_files() -> list:
    """
    Return a list of all dataset files in the data folder.
    """

    folder = "src/data"
    if os.path.exists(folder):
        paths = list(os.listdir(folder))
        paths.remove('.gitkeep')
        paths.remove('output')
        paths.remove('info')

        paths = [path.split('.')[0] for path in paths]
        return paths

    return []

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
        "labels": ["LOC", "HUM", "DESC", "ENTY", "ABBR", "NUM"],
        "description" : "labels for the IsBit classifiers operation on the QAQC dataset." 
    }
    return info_dict


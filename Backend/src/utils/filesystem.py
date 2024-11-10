import json
import os

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

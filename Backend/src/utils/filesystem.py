import pandas as pd
import os
from json import dump


def write_dataset(filename: str, df: pd.DataFrame) -> None:
    """
    Creating or overwriting a file with content.

    filename should not contain a type (.csv, .txt, etc.)
    """
    folder = "src/data"

    df.to_csv(f"{folder}/{filename}.csv", index=False)

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
    suffix = "_meta_info"

    with open(f"{folder}/{info_filename}{suffix}.info", 'w') as f:
        dump(metadata, f, indent=4) 


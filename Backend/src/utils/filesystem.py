import pandas as pd
from json import dump


def write_dataset(filename: str, df: pd.DataFrame) -> None:
    """
    Creating or overwriting a file with content.

    filename should not contain a type (.csv, .txt, etc.)
    """
    folder = "src/data"

    df.to_csv(f"{folder}/{filename}.csv", index=False)

def write_info(info_filename: str, metadata: dict) -> None:
    """
    Creating or overwriting a .info file with accompanying content for a dataset.

    filename should not contain type suffix (.info, .etc)
    """
    folder = "src/data/info"
    suffix = "_meta_info"

    with open(f"{folder}/{info_filename}{suffix}.info", 'w') as f:
        dump(metadata, f, indent=4) 


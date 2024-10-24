import json
import pandas as pd


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

    with open(f"{folder}/{info_filename}.info", 'w') as f:
        json.dump(metadata, f, indent=4) 


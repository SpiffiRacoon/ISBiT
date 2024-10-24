import pandas as pd


def write_dataset(filename: str, df: pd.DataFrame) -> None:
    """
    Creating or overwriting a file with content.

    filename should not contain a type (.csv, .txt, etc.)
    """
    folder = "src/data"

    df.to_csv(f"{folder}/{filename}.csv", index=False)

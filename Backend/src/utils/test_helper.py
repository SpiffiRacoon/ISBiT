

from io import StringIO
import pandas as pd
import requests


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
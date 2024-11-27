#own
from ..db import get_nodes_from_latest_version
from ..types import Node

#pip
import pandas as pd


def simulate_user_input(dataset_name: str, fraction:float) -> pd.DataFrame:
    """
    Simulate user labels by setting a fraction of nodes' 'input_label' to their 'truth' value.
    """
    db_nodes = get_nodes_from_latest_version(dataset_name=dataset_name)
    df = pd.DataFrame(db_nodes)

    if 'input_label' not in df.columns:
        df['input_label'] = None
    if 'truth' not in df.columns:
        print("No truth in df.columns", df.columns)
        raise ValueError("The 'truth' column is missing from the data.")

    nodes_with_null_label = df[df['input_label'].isnull()]
    sampled_nodes = nodes_with_null_label.sample(frac=fraction)
    df.loc[sampled_nodes.index, 'input_label'] = df.loc[sampled_nodes.index, 'truth']

    return df
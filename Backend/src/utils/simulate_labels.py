#own
from ..db import (
    get_all_nodes_from as db_get_all_nodes_from
)
from ..types import Node

#pip
import pandas as pd
import random

def simulate_user_input(collection: str, fraction:float=0.1) -> list[Node]:
    db_nodes = db_get_all_nodes_from(collection=collection)

    print("db_nodes:", db_nodes)

    df = pd.DataFrame(db_nodes)

    # Debugging step: Check the structure of the incoming data
    # print("db_nodes sample:", db_nodes[:5])  # Print the first few nodes

    if 'input_label' not in df.columns:
        df['input_label'] = None
    if 'truth' not in df.columns:
        print("No truth in df.columns", df.columns)
        raise ValueError("The 'truth' column is missing from the data.")

    nodes_with_null_label = df[df['input_label'].isnull()]
            
    sampled_nodes = nodes_with_null_label.sample(frac=fraction, random_state=1)
    
    #modifies the main DataFrame df with the new input_label already.
    #df.loc it the thing that updates df directly and contains all nodes
    df.loc[sampled_nodes.index, 'input_label'] = df.loc[sampled_nodes.index, 'truth']
    
    # Convert modified DataFrame back to a list of Node objects
    updated_nodes = [Node(**row) for row in df.to_dict(orient="records")]

    return updated_nodes


# newNodes = []
# for item in db_nodes: 
#     print("node item:", item)
    
#     if item.input_label == None and random.random() <= fraction:
#         item.input_label = item.truth
#         newNodes.append(item)
#     else:
#         newNodes.append(item)

# print("oldNodes:", db_nodes)
# print("newNodes:", newNodes)
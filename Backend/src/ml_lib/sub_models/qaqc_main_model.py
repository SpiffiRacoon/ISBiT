import pandas as pd
import csv
import re
import os
import torch

import random

from sentence_transformers import SentenceTransformer
from ..shared import IsbitClassifierModel

class QaqcMainModel(IsbitClassifierModel):

    def _format_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Formats the input data
        """
        df["truth"] = df["verbose label"].str.split(":").str[0]

        df = df[['text', 'truth']]

        return df

    def get_embeddings(self,text_lst: list) -> torch.Tensor:
        """
        Function to get the embeddings from the sentences
        """
        model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        embeddings = model.encode(text_lst, convert_to_tensor=True)
        return embeddings
    
    def first_run(self, df: pd.DataFrame, dim: str | None) -> pd.DataFrame:
        """
        Combines the input question data with the calculated 2D point data
        """
        questions = df["text"].tolist()
        ids = [self.get_id(question) for question in questions]
        df["id"] = pd.Series(ids)
        embeddings = self.get_embeddings(questions)

        point_data_df = self.dim_red(embeddings=embeddings, dim=dim)
        combined_df = pd.concat([df, point_data_df], axis=1)
        return combined_df

    
    def get_more_user_input(df: pd.DataFrame):
        """
        Generates more input_label entries for the dataframe
        """
        for i in range(len(df["input_label"])):
                    if random.randint(1,100) < 15:
                            if df["input_label"][i] == None:
                                    df.loc[i,"input_label"] = df.loc[i,"truth"] 
                    pass
        return df

    def latter_run(self,df: pd.DataFrame, dim: str | None) -> pd.DataFrame:
        print("entered latter run")
        print(df["input_label"])
        df = self.get_more_user_input(df) #no clue why this breaks
        print("got more user input")

        questions = df["text"].tolist()
        embeddings_tensor = self.get_embeddings(questions) #This is equal to the first embeddings(1.2 in our figure), the alternative
        print("got embeddings in latter run")
        #is to fetch these embeddings from the database
        user_truth = df["input_label"].tolist()
        #Calls the classifier to generate the predicted labels
        predictedLabels, new_embeddings = self.random_forest_classifier(embeddings=embeddings_tensor, user_truth=user_truth)
        #Something goes wrong while calling randomforest, probably because no assigned input_labels are given.
        
        print("got predicted labels in latter run")
        predLabels_df = pd.DataFrame(predictedLabels.tolist(), columns=["predicted_labels"])
        
        x_and_y = self.dim_red(embeddings=new_embeddings, dim=dim) #generates coordinates x and y for plotting in frontend
        print("got reduced embeddings in latter run")
        #Combines all of the dataframes together in order to form the final dataframe
        combined_df = pd.concat([df["text"], x_and_y, df["truth"], df["id"] , df["input_label"], predLabels_df], axis=1)
        print("concatinated dataframes in latter run")
        return combined_df
    

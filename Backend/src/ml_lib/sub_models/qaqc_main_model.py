import pandas as pd
import csv
import re
import os
import torch

from sentence_transformers import SentenceTransformer
from ..shared import IsbitClassifierModel

class QaqcMainModel(IsbitClassifierModel):

    def _format_data(self, file_name: str) -> None:
        """
        Function to format the QAQC data set, replaces comma signs iniside the question data with pipe sign |
        and removes outer qutation marks from the questions, also adds escape characters where its needed.
        """
        source_data_path = f"src/data/{file_name}.csv"
        output_data_path = f"src/data/output/{file_name}_prep.csv"
        with open(source_data_path, "r", encoding="utf-8") as infile:
            modified_lines = [
                [x for x in self.replace_commas(line.strip()).split(",")]
                for line in infile
            ]

        temp_data = pd.DataFrame(modified_lines[1:], columns=modified_lines[0])
        questions = temp_data["text"].tolist()
        no_comma_questions = [self.strip_outer_quotationmarks(q) for q in questions]

        coarse_labels = list(
            map(lambda x: x.split(":")[0], temp_data["verbose label"].tolist())
        )
        zipped = list(zip(no_comma_questions, coarse_labels))

        os.makedirs(os.path.dirname(output_data_path), exist_ok=True)
        with open(output_data_path, "w", encoding="utf-8", newline="") as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["text", "coarse label"])
            writer.writerows(zipped)

    def strip_outer_quotationmarks(self, q: str) -> str:
        """
        Helper to remove outer quotation marks, specific for qaqc data set
        """
        if q.startswith('"') and q.endswith('"'):
            q = q[1:-1]
        return q.strip()

    def replace_commas(self, line: str) -> str:
        """
        Helper to remove commas in the question text, specific for qaqc data set
        """
        pattern = r'"([^"]*?)"'

        def replace_commas(match):
            return '"' + match.group(1).replace(",", "|") + '"'
        return re.sub(pattern, replace_commas, line)

    def first_run(self, df: pd.DataFrame, dim: str | None) -> pd.DataFrame:
        """
        Combines the input question data with the calculated 2D point data
        """
        questions = df["text"].tolist()
        ids = [self.get_id(question) for question in questions]
        df["id"] = pd.Series(ids)
        model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        embeddings = model.encode(questions, convert_to_tensor=True)

        point_data_df = self.dim_red(embeddings=embeddings, dim=dim)
        combined_df = pd.concat([df, point_data_df], axis=1)
        combined_df = combined_df.rename(columns={"coarse label": "truth"})
        return combined_df
    


    def latter_run(self, df: pd.DataFrame, dim: str | None) -> pd.DataFrame:

        old_embeddings_and_input_labels_df = self.get_embeddings(df["text","input_label"].tolist()) #This is equal to the first embeddings(1.2 in our figure)
        
        #Calls the classifier to generate the predicted labels
        predictedLabels, new_embeddings = self.random_forest_classifier(old_embeddings_and_input_labels_df)
        predLabels_df = pd.DataFrame(predictedLabels.tolist(), columns=["predicted_labels"])
        
        x_and_y = self.dim_red(embeddings=new_embeddings, dim=dim) #generates coordinates x and y for plotting in frontend

        #Combines all of the dataframes together in order to form the final dataframe
        combined_df = pd.concat([df["text"], x_and_y, df["truth"], df["input_label"], predLabels_df], axis=1)
        return combined_df
    
    def get_embeddings(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Function to get the embeddings from the sentences
        """
        model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        embeddings = model.encode(df["text"].tolist(), convert_to_tensor=True)
        embedded_df = pd.DataFrame(embeddings.tolist(), columns=["embeddings"])
        returning_df = pd.concat([df["input_label"], embedded_df], axis=1)
        return returning_df
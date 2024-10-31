import json
import pandas as pd
import csv
import re
import os
import hashlib

from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from ..shared import IsbitClassifierModel


class QaqcTestModel(IsbitClassifierModel):

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

    def _read_meta_info(self, file_name: str) -> dict:
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
    
    def get_id(self, content: str) -> str:
        id = hashlib.sha256(bytes(content, 'utf-8')).hexdigest()
        return id

    def first_run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Combines the input qeustion data with the calculated 2D point data
        """
        questions = df["text"].tolist()
        ids = [self.get_id(question) for question in questions]
        d = {'id': ids}
        id_df = pd.DataFrame(data=d)
        model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        embeddings = model.encode(questions, convert_to_tensor=True)
        num_clusters = 6  # coarse lables: [LOC, HUM, DESC, ENTY, ABBR, NUM]
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(embeddings.cpu().numpy())
        clusters = kmeans.labels_
        pca = PCA(n_components=2)
        reduced_embeddings = pca.fit_transform(embeddings.cpu().numpy())
        point_data_df = pd.DataFrame(reduced_embeddings, columns=["x", "y"])
        point_data_df["cluster"] = clusters
        df = df.reset_index(drop=True)
        combined_df = pd.concat([df, point_data_df], axis=1)
        combined_df = pd.concat([combined_df, id_df], axis=1)
        combined_df = combined_df.rename(columns={"coarse label": "truth"})
        return combined_df

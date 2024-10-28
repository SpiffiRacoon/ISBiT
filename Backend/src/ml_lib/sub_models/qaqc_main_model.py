import pandas as pd
import csv
import re
import os

from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

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
        model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        embeddings = model.encode(questions, convert_to_tensor=True)
        match dim:
            case "COMBO":
                pca2 = PCA(n_components=50, whiten=False, random_state=42)
                reduced_embeddings_pca2 = pca2.fit_transform(embeddings)
                tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=300, early_exaggeration=4, learning_rate=1000)
                reduced_embeddings = tsne.fit_transform(reduced_embeddings_pca2)
                point_data_df = pd.DataFrame(reduced_embeddings, columns=["x", "y"])
            case "PCA":
                pca = PCA(n_components=2, random_state=42)
                reduced_embeddings_PCA = pca.fit_transform(embeddings)
                point_data_df = pd.DataFrame(reduced_embeddings_PCA, columns=["x", "y"])

            case "TSNE":
                pure_tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=300, early_exaggeration=4, learning_rate=1000)
                reduced_embeddings_tsne = pure_tsne.fit_transform(embeddings)
                point_data_df = pd.DataFrame(reduced_embeddings_tsne, columns=["x", "y"])
            case _: 
                raise Exception("Invalid dimension reduction method.")
            
        combined_df = pd.concat([df, point_data_df], axis=1)
        combined_df = combined_df.rename(columns={"coarse label": "truth"})
        return combined_df
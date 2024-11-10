import pandas as pd
from sentence_transformers import SentenceTransformer

from ..shared import IsbitClassifierModel


class QaqcMainModel(IsbitClassifierModel):

    def _format_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Formats the input data
        """
        df = df[['text', 'coarse label']]

        return df

    def first_run(self, df: pd.DataFrame, dim: str | None) -> pd.DataFrame:
        """
        Combines the input question data with the calculated 2D point data
        """
        questions = df["text"].tolist()
        ids = [self.get_id(question) for question in questions]
        d = {'id': ids}
        id_df = pd.DataFrame(data=d)
        model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        embeddings = model.encode(questions, convert_to_tensor=True)

        point_data_df = self.dim_red(embeddings=embeddings, dim=dim)
        combined_df = pd.concat([df, point_data_df], axis=1)
        combined_df = pd.concat([combined_df, id_df], axis=1)
        combined_df = combined_df.rename(columns={"coarse label": "truth"})
        return combined_df

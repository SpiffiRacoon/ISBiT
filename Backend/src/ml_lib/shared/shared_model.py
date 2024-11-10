import hashlib
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap
from sentence_transformers import SentenceTransformer
import torch #May be able to do this without importing entire library, only need this to define embeddings as torch.Tensor
class IsbitClassifierModel:

    def __init__(
        self, source_data_path: str | None = None, df: pd.DataFrame | None = None
    ) -> None:
        self._df = df

    def _format_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Formatting logic, overridden by child classes.
        """
        return df

    def run(self, df: pd.DataFrame, is_first: bool, dim: str | None) -> None:
        """
        Run declared in super class, initializes
        """
        data = self._format_data(df=df)

        if not is_first:
            df = self.latter_run(data)
        else:
            df = self.first_run(data, dim)

        self._df_setter(df)

    def first_run(self, df: pd.DataFrame, dim: str | None) -> pd.DataFrame:
        """
        First clustering run logic, overridden by child classes.
        """

        raise Exception("Not implemented.")

    def latter_run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        (mby not needed, but run after feedback loop) Latter clustering run logic, overridden by child classes.
        """
        raise Exception("Not implemented.")

    def _df_setter(self, df: pd.DataFrame) -> None:
        """
        Setter for the data frame attribute.
        """

        # TODO: validators
        self._df = df

    def get_id(self, content: str) -> str:
        id = hashlib.sha256(bytes(content, 'utf-8')).hexdigest()
        return id

    @property
    def df(self) -> pd.DataFrame:
        """
        Getter for the dataframe of ML models.
        """
        if self._df is None:
            raise Exception("Dataframe is None.")

        return self._df


    def dim_red(self, embeddings: torch.Tensor, dim: str | None) -> pd.DataFrame:
        """
        Reduces embeddings to 2 dimensions using PCA, TSNE, or UMAP and
        returns a dataframe with the reduced embeddings.
        """
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

            case "UMAP":
                umap_model = umap.UMAP(n_components=2, random_state=42, n_neighbors=15, min_dist=0.1, metric='euclidean')
                reduced_embeddings_umap = umap_model.fit_transform(embeddings)
                point_data_df = pd.DataFrame(reduced_embeddings_umap, columns=["x", "y"])

            case _:
                raise Exception("Invalid dimension reduction method.")

        return point_data_df

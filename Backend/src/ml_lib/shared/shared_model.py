import hashlib
import pandas as pd

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
        print(f"In run: {is_first = }")
        if not is_first:
            print("just before latter run")
            df = self.latter_run(df, dim)
        else:
            data = self._format_data(df=df)
            df = self.first_run(data, dim)

        self._df_setter(df)

    def first_run(self, df: pd.DataFrame, dim: str | None) -> pd.DataFrame:
        """
        First clustering run logic, overridden by child classes.
        """

        raise Exception("Not implemented.")

    def latter_run(self, df: pd.DataFrame, dim: str | None) -> pd.DataFrame:
        #
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

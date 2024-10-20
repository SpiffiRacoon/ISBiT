import pandas as pd


class IsbitClassifierModel:

    def __init__(
        self, source_data_path: str | None = None, df: pd.DataFrame | None = None
    ) -> None:
        self._df = df

    def _read_data_frame(self, file_name: str) -> pd.DataFrame:
        """
        Reads the CSV data and returns it as a Panda data frame.
        """
        source_path = f"src/data/output/{file_name}_prep.csv"
        data = pd.read_csv(source_path)
        return data

    def _format_data(self, file_name: str) -> None:
        """
        Formatting logic, overridden by child classes.
        """
        pass

    def run(self, file_name: str, is_first: bool) -> None:
        """
        Run declared in super class, initializes
        """
        self._format_data(file_name=file_name)
        data = self._read_data_frame(file_name)

        if not is_first:
            df = self.latter_run(data)
        else:
            df = self.first_run(data)

        self._df_setter(df)

    def first_run(self, df: pd.DataFrame) -> pd.DataFrame:
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

        df = df[["text", "x", "y", "truth", "cluster"]]

        # TODO: validators
        self._df = df

    @property
    def df(self) -> pd.DataFrame:
        """
        Getter for the dataframe of ML models.
        """
        return self._df

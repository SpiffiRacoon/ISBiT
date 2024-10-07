import pandas as pd

class IsbitClassifierModel:

    def __init__(self, source_data_path: str = None, df: pd.DataFrame = None):
        self.df = df
        self.source_data_path = source_data_path

    def _format_data(self):
        """ Formatting logic, overridden by child classes. """
        if self.df is None and self.source_data_path:
            self.df = pd.read_csv(self.source_data_path)

    def first_run(self):
        """ First clustering run logic, overridden by child classes. """
        self._format_data()
        return None
    
    def latter_run(self):
        """ (mby not needed, bu run after feedback) Latter clustering run logic, overridden by child classes. """

    def get_data(self) -> pd.DataFrame:
        return self.df

    

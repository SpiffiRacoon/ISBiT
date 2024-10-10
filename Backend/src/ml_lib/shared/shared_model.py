import pandas as pd

class IsbitClassifierModel:

    def __init__(self, source_data_path: str | None = None, df: pd.DataFrame | None = None) -> None:
        self.df = df
        self.source_data_path = source_data_path

    def _read_data_frame(file_name: str) -> pd.DataFrame:
        source_path = f"src/data/{file_name}"
        data = pd.read_csv(source_path)
        return data

    def _format_data(self, file_name: str) -> None:
        """ 
        Formatting logic, overridden by child classes. 
        """
        pass

    def run(self, file_name: str,is_first:bool) -> None:
        """ 
        Generic run frunction, shou
        """
        self._format_data(self, file_name=file_name)
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
        (mby not needed, bu run after feedback) Latter clustering run logic, overridden by child classes. 
        """
        raise Exception("Not implemented.")
    
    def _df_setter(self, df: pd.DataFrame) -> None:
        # TODO: validators
        self.df = df

    def get_data(self) -> pd.DataFrame:
        return self.df

    

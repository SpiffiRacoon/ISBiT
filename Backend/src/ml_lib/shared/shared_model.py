import hashlib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sentence_transformers import SentenceTransformer

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


    def run(self, file_name: str, is_first: bool, dim: str | None) -> None:
        """
        Run declared in super class, initializes
        """
        self._format_data(file_name=file_name)
        data = self._read_data_frame(file_name)

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

    def latter_run(self, df: pd.DataFrame, dim: str | None) -> pd.DataFrame:

        # [text,UserTruth]=getTextWhereUserTruth!=NIL();
        # UnAssignedText=getTextWhereUserTruth==NIL();
        # predictedLabels=classifier([text,UserTruth], UnAssignedLabels)
        # UpdateDataFrame(predictedLabels)
        #                                                                                                               UpdateEmbeddings
        # PingFrontEndToUpdate

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
        return self._df
    
        

    def Random_Forest_classifier(sentencesWithLabels, labels, sentencesWithoutLabels):
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        sentencesWithLabels_embeddings = model.encode(sentencesWithLabels, show_progress_bar=True)
        sentencesWithoutLabels_embeddings = model.encode(sentencesWithoutLabels, show_progress_bar=True)

      

        # Initialize the Random Forest Classifier
        clf = RandomForestClassifier(n_estimators=1024, random_state=42, max_leaf_nodes=4)

# testing?

        # test=clf.apply(X_train)
        # print(test)
        # Train the classifier
        clf.fit(sentencesWithLabels_embeddings, labels)

        # Predict the test set results
        label_pred = clf.predict(sentencesWithoutLabels_embeddings)

        return (label_pred)



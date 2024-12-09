import pandas as pd

from torch import Tensor
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.ensemble import RandomForestClassifier
import umap


from sentence_transformers import SentenceTransformer
from ..shared import IsbitClassifierModel

class QaqcMainModel(IsbitClassifierModel):

    def _format_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Formats the input data
        """
        df["truth"] = df["verbose label"].str.split(":").str[0]

        df = df[['text', 'truth']]

        return df

    def get_embeddings(self,text_lst: list) -> Tensor:
        """
        Function to get the embeddings from the sentences
        """
        model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        embeddings = model.encode(text_lst, convert_to_tensor=True)
        return embeddings
    
    def random_forest_classifier(self, embeddings: Tensor, user_truth: list):
        max_leaf = 4
        # Initialize the Random Forest Classifier
        clf = RandomForestClassifier(n_estimators=384, random_state=42, max_leaf_nodes=max_leaf)
        #n_estimators should be equal to the embedding space(i.e sentenceswithoutlabels)

        #Generating necessary input for the classifier

        all_old_embeddings_lst = embeddings.tolist()
        if len(user_truth) != len(all_old_embeddings_lst):
            raise Exception("user labeling is not equal to the number of embeddings")
        
        embeddingsWithInputFromUser = []
        embeddingsWithoutInputFromUser = [] #we dont need this anymore?
        actual_assigned_labels = []
        #Splits the sentences into labeled and unlabeled based on whether they have an input label or not
        for x in range(len(all_old_embeddings_lst)):
              if user_truth[x] == None:
                  embeddingsWithoutInputFromUser.append(all_old_embeddings_lst[x])
              else:
                  embeddingsWithInputFromUser.append(all_old_embeddings_lst[x])
                  actual_assigned_labels.append(user_truth[x])

        #Train the classifier        
        clf.fit(embeddingsWithInputFromUser, actual_assigned_labels)

        #Generates new embeddings for use in the frontend
        new_embeddings=clf.apply(all_old_embeddings_lst)

        # Predict the test set results
        # label_pred = clf.predict(embeddingsWithoutInputFromUser)
        label_pred = clf.predict(all_old_embeddings_lst)

        return (label_pred, new_embeddings)
    
    def dim_red(self, embeddings: Tensor, dim: str | None) -> pd.DataFrame:
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
    
    def first_run(self, df: pd.DataFrame, dim: str | None) -> pd.DataFrame:
        """
        Combines the input question data with the calculated 2D point data
        """
        questions = df["text"].tolist()
        ids = [self.get_id(question) for question in questions]
        df["id"] = pd.Series(ids)
        embeddings = self.get_embeddings(questions)
        df["id"] = pd.Series(ids)
        embeddings = self.get_embeddings(questions)

        point_data_df = self.dim_red(embeddings=embeddings, dim=dim)
        combined_df = pd.concat([df, point_data_df], axis=1)
        return combined_df


    def latter_run(self,df: pd.DataFrame, dim: str | None) -> pd.DataFrame:
       
        questions = df["text"].tolist()
        embeddings_tensor = self.get_embeddings(questions) #This is equal to the first embeddings(1.2 in our figure), the alternative

        #is to fetch these embeddings from the database
        user_truth = df["input_label"].tolist()
        #Calls the classifier to generate the predicted labels

        try:
            predictedLabels, new_embeddings = self.random_forest_classifier(embeddings_tensor, user_truth)
        except Exception as e:
            print(e)
            raise(e)
           
        
        predLabels_df = pd.DataFrame(predictedLabels.tolist(), columns=["predicted_labels"])
        
        x_and_y = self.dim_red(embeddings=new_embeddings, dim=dim) #generates coordinates x and y for plotting in frontend

        #Combines all of the dataframes together in order to form the final dataframe
        combined_df = pd.concat([df["text"], x_and_y, df["truth"], df["id"] , df["input_label"], predLabels_df], axis=1)
        return combined_df

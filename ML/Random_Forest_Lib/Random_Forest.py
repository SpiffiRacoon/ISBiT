
from sklearn.ensemble import RandomForestClassifier
from sentence_transformers import SentenceTransformer


# data = pd.read_csv('data\QAQC\swe_qaqc_train.csv')
# def formatData(data):
#     sentences = data['text'].tolist()
#     Coarse_labels = data['coarse label'].tolist()
#     Fine_labels = data['fine label'].tolist()
#     combined_labels = [f"{coarse}:{fine}" for coarse, fine in zip(Coarse_labels, Fine_labels)]
#     X=sentences
#     y=Coarse_labels
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.80, random_state=42)

    
#     return (X_train, y_train, X_test, sentences, Coarse_labels, Fine_labels, combined_labels)



def Random_Forest_classifier(sentencesWithLabels, labels, sentencesWithoutLabels):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    sentencesWithLabels_embeddings = model.encode(sentencesWithLabels, show_progress_bar=True)
    sentencesWithoutLabels_embeddings = model.encode(sentencesWithoutLabels, show_progress_bar=True)

    y = labels

    # Split the data into training and testing sets
    X_train = sentencesWithLabels_embeddings
    
    # Initialize the Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=1024, random_state=42, max_leaf_nodes=4)


    # test=clf.apply(X_train)
    # print(test)
    # Train the classifier
    clf.fit(X_train, y)

    # Predict the test set results
    y_pred = clf.predict(sentencesWithoutLabels_embeddings)

    return (sentencesWithoutLabels, y_pred)





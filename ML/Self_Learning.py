import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.semi_supervised import LabelSpreading
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import seaborn as sns
import sys
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier  # You can replace this with any other model

# Step 1: Load the CSV file
df = pd.read_csv('data\QAQC\swe_qaqc_train.csv')

# Step 2: Extract the text data
sentences = df['text'].tolist()
Coarse_labels = df['coarse label'].tolist()
Fine_labels = df['fine label'].tolist()
combined_labels = [f"{coarse}:{fine}" for coarse, fine in zip(Coarse_labels, Fine_labels)]

amountOfLabeledPoints=500
DatapointsWithLabels = sentences[:amountOfLabeledPoints]
CorrespondingLabels = combined_labels[:amountOfLabeledPoints] 

DatapointsWithoutLabels = sentences[500:]  # The remaining data points (without labels)
TrainingLabels = combined_labels[500:]  # The remaining labels (you won't use these for training)

model = DecisionTreeClassifier()  # Example model
model.fit(DatapointsWithLabels, CorrespondingLabels)

# Step 3: Initialize assigned labels, set -1 for unlabeled data
assigned_labels = ['-1' for _ in combined_labels]

# Manually assign real labels to some data points (let's assume first 2000 are labeled)
for i in range(2000):  # Assign real labels to 2000 data points
    assigned_labels[i] = combined_labels[i]

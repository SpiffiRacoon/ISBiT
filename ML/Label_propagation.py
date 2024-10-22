import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.semi_supervised import LabelSpreading
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import seaborn as sns
import sys

# Step 1: Load the CSV file
df = pd.read_csv('data\QAQC\swe_qaqc_train.csv')

# Step 2: Extract the text data
sentences = df['text'].tolist()
Coarse_labels = df['coarse label'].tolist()
Fine_labels = df['fine label'].tolist()
combined_labels = [f"{coarse}:{fine}" for coarse, fine in zip(Coarse_labels, Fine_labels)]

sys.setrecursionlimit(10000)

# Step 3: Initialize assigned labels, set -1 for unlabeled data
assigned_labels = ['-1' for _ in combined_labels]

# Manually assign real labels to some data points (let's assume first 2000 are labeled)
for i in range(5430):  # Assign real labels to 2000 data points
    assigned_labels[i] = combined_labels[i]

# Convert the assigned labels to a NumPy array
labels = np.array(assigned_labels)

# Step 4: Load SentenceTransformer model and compute embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
sentence_embeddings = model.encode(sentences, show_progress_bar=True)
print("Embeddings shape:", sentence_embeddings.shape)

# Step 5: Dimensionality reduction (optional)
pca = PCA(n_components=50)  # Reduce embeddings to 50 dimensions
sentence_embeddings_reduced = pca.fit_transform(sentence_embeddings)

# Step 6: Perform Label Spreading with KNN kernel and increased neighbors
label_spreading = LabelSpreading(kernel='knn', n_neighbors=30)  # Use 30 neighbors
label_spreading.fit(sentence_embeddings_reduced, labels)

# Step 7: Predict the labels for all data points
predicted_labels = label_spreading.predict(sentence_embeddings_reduced)
print("Predicted labels:", predicted_labels)

# Check how many points are still labeled as -1
unlabeled_points = np.sum(predicted_labels == '-1')
print(f"Number of points still labeled -1: {unlabeled_points}")

# Step 8: Ensure that initially labeled points maintain their labels
# Ensure that the first 2000 points (initially labeled) remain unchanged
for i in range(5430):
    if predicted_labels[i] == '-1':
        predicted_labels[i] = labels[i]  # Re-assign original label to ensure they aren't overwritten

# Step 9: Visualize the embeddings with t-SNE
tsne = TSNE(n_components=2, perplexity=30, n_iter=300, random_state=42)
sentence_embeddings_2d = tsne.fit_transform(sentence_embeddings_reduced)

# Step 10: Create a color palette for the valid predicted labels
unique_labels = np.unique(predicted_labels[predicted_labels != -1])  # Exclude -1
palette = sns.color_palette("hsv", len(unique_labels))

# Step 11: Map predicted labels to colors
label_to_color = {label: palette[i] for i, label in enumerate(unique_labels)}

# Step 12: Plot the t-SNE results, coloring points by their valid predicted labels
plt.figure(figsize=(10, 7))

# Plot each point with its corresponding color based on the predicted label
for i, label in enumerate(predicted_labels):
    if label != '-1':  # Only plot valid labels
        plt.scatter(sentence_embeddings_2d[i, 0], sentence_embeddings_2d[i, 1], 
                    color=label_to_color[label], s=100, label=f'Label {label}' if i == 0 else "")

# Add titles and labels
plt.title('t-SNE Visualization of Embeddings with Label Spreading')
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')

# Create a legend for the labels
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=label_to_color[label], markersize=10) for label in unique_labels]
plt.legend(handles, [f'Label {label}' for label in unique_labels], loc='best')

plt.grid(True)
plt.show()

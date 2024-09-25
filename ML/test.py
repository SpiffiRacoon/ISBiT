import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from scipy.sparse import hstack

# Step 1: Load the data from the CSV file
df = pd.read_csv('ML/testdata.csv')

# Step 2: Preprocess the free-text column using TF-IDF
tfidf = TfidfVectorizer(stop_words='english', max_features=100)
tfidf_matrix = tfidf.fit_transform(df['Circumstances'])

# Step 3: Preprocess the structured data (One-Hot Encode categorical columns)
df_encoded = pd.get_dummies(df, columns=['Reason for Request', 'Illness/Condition'], drop_first=True)

# Select the features for clustering (excluding 'Name' and 'Circumstances' as they aren't relevant for clustering)
features = df_encoded.drop(['Name', 'Circumstances'], axis=1)

# Step 4: Normalize the structured data
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Step 5: Combine the structured and text data (TF-IDF vectors)
combined_features = hstack([scaled_features, tfidf_matrix]).toarray()

# Step 6: Apply KMeans Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(combined_features)

# Step 7: Add the cluster labels to the original dataset
df['Cluster'] = kmeans.labels_

# Print the dataset with the cluster labels
print(df[['Name', 'Cluster', 'Circumstances']])

# Step 8: Optional: Use PCA for visualization of clusters
pca = PCA(n_components=2)
pca_components = pca.fit_transform(combined_features)

# Plot the clusters in a 2D space
plt.scatter(pca_components[:, 0], pca_components[:, 1], c=df['Cluster'], cmap='viridis')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.title('KMeans Clustering with Free-Text Circumstances')
plt.colorbar(label='Cluster')
plt.show()

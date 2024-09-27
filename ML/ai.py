

##.\envISBIT\Scripts\activate to activate my virtual environment
## "deactivate" to deactivate it

from sentence_transformers import SentenceTransformer
import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('ML/swe_qaqc_train.csv')

# Print the first 5 rows of the DataFrame to verify the contents
print(df.head())
# Load a pre-trained SBERT model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# List of sentences to encode
sentences = df['text'].tolist()

# Get sentence embeddings
embeddings = model.encode(sentences, show_progress_bar=True)

# Print the embeddings
#for sentence, embedding in zip(sentences, embeddings):
#    print(f"Sentence: {sentence}")
#    print(f"Embedding: {embedding[:1]}...")  # Print the first 5 dimensions of the embedding for brevity
#    print()
#print(f"Embedding dimensions: {len(embeddings[0])}")
for i, (sentence, embedding) in enumerate(zip(sentences, embeddings)):
    if i >= 10:
        break  # Stop after printing 10 sentences
    print(f"Sentence {i + 1}: {sentence}")
    print(f"Embedding {i + 1} (first 5 dimensions): {embedding[:5]}\n")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sentences1 = ["pippo pappo"]
sentences2 = ["zio tobia pippo"]

vectorizer = TfidfVectorizer()

# Vectorize each set of sentences separately
vectorized1 = vectorizer.fit_transform(sentences1)
vectorized2 = vectorizer.transform(sentences2)

# Compare each sentence in set 1 to each sentence in set 2
for i in range(len(sentences1)):
    for j in range(len(sentences2)):
        similarity = cosine_similarity(vectorized1[i], vectorized2[j])[0][0]
        print(f"Similarity between sentence {i+1} in set 1 and sentence {j+1} in set 2: {similarity:.2f}")
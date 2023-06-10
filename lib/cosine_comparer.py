from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def cosine_compare(lst):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(lst)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if similarity_matrix[i][j] >= 0.85:
                print(
                    f"Strings '{lst[i]}' and '{lst[j]}' are similar (cosine similarity: {similarity_matrix[i][j]:.2f}), but different DOI/Identifier.\n Consider removing one of them"
                )

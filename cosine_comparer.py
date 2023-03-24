from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def cosine_compare(list1:list, list2:list, similarity_threshold:float=0.5) -> list:
    """ Function that compares two lists of strings and returns a list of tuples with the indexes of the strings that are similar
    Args:
        list1 (list): _description_.
        list2 (list): _description_.
        similarity_threshold (float, optional): _description_. Defaults to 0.5.

    Returns:
        list: _description_.
    """
    # Create a TfidfVectorizer object to convert the sentences to vectors
    vectorizer = TfidfVectorizer()

    # Vectorize each sentence in each set separately
    vectorized1 = [vectorizer.fit_transform([s]) for s in list1]
    vectorized2 = [vectorizer.transform([s]) for s in list2]

    # Compare each sentence in set 1 to each sentence in set 2
    similar = []
    for i in range(len(list1)):
        for j in range(len(list2)):
            # Compute the cosine similarity between the vectorized form of the two sentences
            similarity = cosine_similarity(vectorized1[i], vectorized2[j])[0][0]
            # Print the similarity score for this pair of sentences
            if similarity > similarity_threshold:
                similar.append((i, j, similarity))
    print(similar)
    return similar

import numpy as np

def vectorizer(corpus, model, num_features=100):
    vocabulary = model.wv.index_to_key
    corpus_vectors = []    
    for doc in corpus:
        doc_vec = []
        for word in doc:
            if word in vocabulary:
                word_vector = model.wv[word]
            doc_vec.append(word_vector)  
        avg_vec = np.add.reduce(doc_vec)/len(doc_vec)
        corpus_vectors.append(avg_vec)
    return corpus_vectors
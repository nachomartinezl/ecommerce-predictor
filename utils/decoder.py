import numpy as np
import pickle


with open("model/mapping_dict.pkl", "rb") as f:
    mapping_dict = pickle.load(f)
    mapping_dict["other"] = "other"
    mapping_dict["Unknown"] = "Unknown"
    mapping_dict["Categories"] = "All categories"


  
def vectorizer(corpus, model, num_features=100):
    vocabulary = model.wv.index_to_key
    corpus_vectors = []
    for doc in corpus:
        doc_vec = []
        for word in doc:
            if word in vocabulary:
                word_vector = model.wv[word]
            else:
                word_vector = np.zeros((num_features), dtype="float32")
            doc_vec.append(word_vector)
        avg_vec = np.add.reduce(doc_vec) / len(doc_vec)
        corpus_vectors.append(avg_vec)
    return corpus_vectors


def decode_id(id_or_path: str or list):
    # Return product name if just one id was passed
    if type(id_or_path) == str:
        return mapping_dict[id_or_path]

    path = []
    # Return a list of names if a path was passed
    if type(id_or_path) == list:
        for id in id_or_path:
            path.append(mapping_dict[id])
        return path


with open("model/mapping_id_path_dict.pkl", "rb") as file:
      mapping_path = pickle.load(file)
      

def decode_id_path(cat_id:str):
    return mapping_path[cat_id]


decoder = np.vectorize(decode_id)

decoder_path = np.vectorize(decode_id_path)



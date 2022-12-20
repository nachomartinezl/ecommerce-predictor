import os
import yaml
import tensorflow as tf
from tensorflow import keras
import numpy as np

import numpy as np
import pickle
import os
os.chdir("/home/app/src/")

def validate_config(config):
    """
    Takes as input the experiment configuration as a dict and checks for
    minimum acceptance requirements.

    Parameters
    ----------
    config : dict
        Experiment settings as a Python dict.
    """
    if "seed" not in config:
        raise ValueError("Missing experiment seed")

    if "data" not in config:
        raise ValueError("Missing experiment data")

    if "directory" not in config["data"]:
        raise ValueError("Missing experiment training data")


def load_config(config_file_path):
    """
    Loads experiment settings from a YAML file into a Python dict.
    See: https://pyyaml.org/.

    Parameters
    ----------
    config_file_path : str
        Full path to experiment configuration file.
        E.g: `/home/app/src/experiments/exp_001/config.yml`

    Returns
    -------
    config : dict
        Experiment settings as a Python dict.
    """
    # TODO
    # Load config here and assign to `config` variable
    
    with open(config_file_path, 'r') as f:
        config = yaml.safe_load(f)

    # Don't remove this as will help you doing some basic checks on config
    # content
    validate_config(config)

    return config


def get_class_names(config):
    """
    It's not always easy to track how Keras maps our dataset classes to
    the model outputs.
    Given an image, the model output will be a 1-D vector with probability
    scores for each class. The challenge is, how to map our class names to
    each score in the output vector.
    We will use this function to provide a class order to Keras and keep
    consistency between training and evaluation.

    Parameters
    ----------
    config : dict
        Experiment settings as Python dict.

    Returns
    -------
    classes : list
        List of classes as string.
        E.g. ['AM General Hummer SUV 2000', 'Buick Verano Sedan 2012',
                'FIAT 500 Abarth 2012', 'Jeep Patriot SUV 2012',
                'Acura Integra Type R 2001', ...]
    """
    return sorted(os.listdir(os.path.join(config["data"]["directory"])))


def walkdir(folder):
    """
    Walk through all the files in a directory and its subfolders.

    Parameters
    ----------
    folder : str
        Path to the folder you want to walk.

    Returns
    -------
        For each file found, yields a tuple having the path to the file
        and the file name.
    """
    for dirpath, _, files in os.walk(folder):
        for filename in files:
            yield (dirpath, filename)


def predict_from_folder(folder, model, input_size, class_names):
    """
    Walk through all the image files in a directory, loads them, applies
    the corresponding pre-processing and sends to the model to get
    predictions.

    This function will also return the true label for each image, to do so,
    the folder must be structured in a way in which images for the same
    category are grouped into a folder with the corresponding class
    name. This is the same data structure as we used for training our model.

    Parameters
    ----------
    folder : str
        Path to the folder you want to process.

    model : keras.Model
        Loaded keras model.

    input_size : tuple
        Keras model input size, we must resize the image to math these
        dimensions.

    class_names : list
        List of classes as string. It allow us to map model output IDs to the
        corresponding class name, e.g. 'Jeep Patriot SUV 2012'.

    Returns
    -------
    predictions, labels : tuple
        It will return two lists:
            - predictions: having the list of predicted labels by the model.
            - labels: is the list of the true labels, we will use them to
                      compare against model predictions.
    """
    # Use keras.utils.load_img() to correctly load the image and
    # keras.utils.img_to_array() to convert it to the format needed
    # before sending it to our model.
    # You can use os.walk() or walkdir() to iterate over the files in the
    # folder.
    # Don't forget you must not return the raw model prediction. Model
    # prediction will be a vector assigning probability scores to each
    # class. You must take the position of the element in the vector with
    # the highest probability and use that to get the corresponding class
    # name from `class_names` list.
    # TODO
    predictions = []
    labels = []
    probs = []
    
    for dirpath, _, files in os.walk(folder):
        for file in files:
            path = os.path.join(dirpath, file)
            img = keras.utils.load_img(path, target_size = input_size)
            img = keras.utils.img_to_array(img)
            img = tf.expand_dims(img, 0)
            prob = model.predict(img)
            img_class = class_names[np.argmax(prob)]

            predictions.append(img_class)
            probs.append(prob)

            _, label = os.path.split(dirpath)
             
            labels.append(label)
        
    return predictions, labels, probs

    
with open("model/mapping_dict.pkl", "rb") as f:
    mapping_dict = pickle.load(f)

mapping_dict['other'] = 'other'


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

decoder = np.vectorize(decode_id)


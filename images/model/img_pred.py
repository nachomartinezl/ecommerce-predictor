import os
os.chdir("/home/app/src/model")

import os
os.chdir("/home/app/src/scripts")
from scripts import efficientnet

import pandas as pd
import numpy as np

from sklearn.metrics import accuracy_score, classification_report
from model import evaluation
from model import utils
from model.utils import decoder


CONFIG_YML = "/home/app/src/experiments/exp4/exp4.yml"

TEST_FOLDER = "/home/app/src/test_img/"

WEIGHTS = "/home/app/src/experiments/exp4/model.06-2.0593.h5"

config = utils.load_config(CONFIG_YML)

MODEL_CLASSES = utils.get_class_names(config)

cnn_model = efficientnet.create_model(weights=WEIGHTS)


predictions, labels, probs = utils.predict_from_folder(
    folder=TEST_FOLDER, 
    model=cnn_model, 
    input_size=config["data"]["image_size"], 
    class_names=MODEL_CLASSES,
)

def get_feat_max(cat_prob, prod_idx, max_k_feat, classes):
    """Given a array of predicted probability of classes for one product returns a dictionary with the names of the k classes with the highest probability"""
    most_prob_cat_idx = np.argsort(-cat_prob[prod_idx][0])[:max_k_feat]
    name_cat_max= []
    
    for idx in most_prob_cat_idx:
      nm_cat = classes[idx]
      name_cat_max.append(nm_cat)

    dict_max_feat = {}
    for items in range(len(name_cat_max)):
        dict_max_feat[str(items+1)] = np.array_str(decoder(name_cat_max[items]))

    return dict_max_feat


    # categories model A
dict_a = get_feat_max(cat_prob= probs,
                      prod_idx= 0,
                      max_k_feat=5,
                      classes= MODEL_CLASSES)
dict_a
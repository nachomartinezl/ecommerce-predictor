import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn.preprocessing import label_binarize
from model.utils import decoder
import os
import datetime
import anytree
from scripts import tree_utils

def get_performance(model, pred_labels, true_labels, average, tree, vectorizer=None):
    """
    model: model to evaluate 
    pred_labels: predicted labels
    true_labels: true labels 
    vectorizer: vectorized used to encode labels itfidf, w2vec, countvectorizer
    average: 'micro', 'macro', 'samples', 'weighted', 'binary' or None, default='binary'
    tree: dict generated by make tree function
    """

    
    time_exp = str(datetime.datetime.now())
    true_labels = np.array(true_labels)
    y_true = decoder(true_labels) #antes y_test
    y_pred = decoder(pred_labels) # antes predictions

    accuracy = metrics.accuracy_score(y_true, y_pred)
    precision = metrics.precision_score(y_true, y_pred, average=average)
    recall = metrics.recall_score(y_true, y_pred, average=average)
    f1_score = metrics.f1_score(y_true, y_pred, average=average)
    report = metrics.classification_report(y_true, y_pred)
    dict_report = metrics.classification_report(y_true, y_pred, output_dict=True)
    dict_report_id = metrics.classification_report(true_labels, pred_labels, output_dict=True)

    filename = f"model/experiments/exp{time_exp}/model.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=False)
    with open(filename, "w") as f:
        f.write(str(model.get_params))
        if vectorizer != None:
          f.write(str(vectorizer.get_params))

    df_id = pd.DataFrame(dict_report_id).T
    df_id.to_csv(f"model/experiments/exp{time_exp}/results.csv")

    df2 = pd.DataFrame()
    df2 = df2.assign(pred_cat= pred_labels,
                   true_cat= true_labels,
                   pred_cat_dec = y_pred,
                   true_cat_dec = y_true)
    df2['dist'] = df2.apply(lambda row: tree_utils.dist_nodes(row['pred_cat'],row['true_cat'], tree), axis=1)
    avg_dist = df2['dist'].mean()
    df2.to_csv(f"model/experiments/exp{time_exp}/labels.csv", index= False)
    

    print("Model Performance metrics:")
    print("-" * 30)
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1_score)
    print('Average distance between nodes categories:', avg_dist)
    print("\nModel Classification report:")
    print("-" * 30)
    print(report)

def store_performance_in_df(pred_labels, true_labels, average, tree, index_name):
    true_labels = np.array(true_labels)
    y_true = decoder(true_labels)
    y_pred = decoder(pred_labels)
    
    accuracy = metrics.accuracy_score(y_true, y_pred)
    precision = metrics.precision_score(y_true, y_pred, average=average)
    recall = metrics.recall_score(y_true, y_pred, average=average)
    f1_score = metrics.f1_score(y_true, y_pred, average=average)
    
    df2 = pd.DataFrame()
    df2 = df2.assign(pred_cat= pred_labels,
                   true_cat= true_labels,
                   pred_cat_dec = y_pred,
                   true_cat_dec = y_true)
    df2['dist'] = df2.apply(lambda row: tree_utils.dist_nodes(row['pred_cat'],row['true_cat'], tree), axis=1)
    avg_dist = df2['dist'].mean()
    
    dict = {
        "accuracy" : accuracy,
        "precision" : precision,
        "recall" : recall,
        "f1_score" : f1_score,
        "avg_dist" : avg_dist
    }
    
    df = pd.DataFrame(dict, index=[index_name])
    return df
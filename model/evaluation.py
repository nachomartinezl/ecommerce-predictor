import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn.preprocessing import label_binarize
from model.utils import decoder
import os


def get_performance(predictions, y_test, labels, model, average, timestamp):

    y_true = decoder(y_test)
    y_pred = decoder(predictions)

    accuracy = metrics.accuracy_score(y_true, y_pred)
    precision = metrics.precision_score(y_true, y_pred, average=average)
    recall = metrics.recall_score(y_true, y_pred, average=average)
    f1_score = metrics.f1_score(y_true, y_pred, average=average)
    report = metrics.classification_report(y_true, y_pred)
    dict_report = metrics.classification_report(y_true, y_pred, output_dict=True)
    dict_report_id = metrics.classification_report(y_test, predictions, output_dict=True)

    filename = f"model/experiments/exp{timestamp}/model.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=False)
    with open(filename, "w") as f:
        f.write(str(model.get_params))

    df_id = pd.DataFrame(dict_report_id).T
    df_id.to_csv(f"model/experiments/exp{timestamp}/results.csv")

    df2 = pd.DataFrame(labels)
    df2.to_csv(f"model/experiments/exp{timestamp}/labels.csv")

    print("Model Performance metrics:")
    print("-" * 30)
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1_score)
    print("\nModel Classification report:")
    print("-" * 30)
    print(report)


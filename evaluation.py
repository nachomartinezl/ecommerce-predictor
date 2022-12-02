import pandas as pd
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.preprocessing import label_binarize


def get_performance(predictions, y_test, labels, average):

    accuracy = metrics.accuracy_score(y_test, predictions) 
    precision = metrics.precision_score(y_test, predictions, average=average)
    recall = metrics.recall_score(y_test, predictions, average=average)
    f1_score = metrics.f1_score(y_test, predictions, average=average)
    report = metrics.classification_report(y_test, predictions)
    
    print('Model Performance metrics:')
    print('-'*30)
    print('Accuracy:', accuracy)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1 Score:', f1_score)
    print('\nModel Classification report:')
    print('-'*30)
    print(report)
    
    return accuracy, precision, recall, f1_score

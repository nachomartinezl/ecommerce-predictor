import numpy as np
from text_normalizer import normalize_corpus, stopword_list
import joblib
from utils import decoder


class Combined_Model():
   

    def predict_proba(self, X_list, estimators):
        """
        Predict probabilities of classes for samples in X.
        Parameters
        ----------
        X : list of array_like or sparse matrix of shape (n_samples, n_features)
            [X_name, X_description, X_image]
        estimators: list of pretrained models to be combined in the following order [name_model, name_description_model, image_model]
        Returns
        -------
        C : array, shape [n_samples]
            Predicted class label per sample.
        """
        # only NLP Models 
        if len(estimators) == 2:
            y_pred_model_1 = estimators[0].predict_proba(X_list[0])
            y_pred_model_2 = estimators[1].predict_proba(X_list[1])
            probs = np.array([(prob1 + prob2) * 0.5 for prob1, prob2 in zip(y_pred_model_1, y_pred_model_2)])
        
        # NLP + images    
        elif len(estimators) == 3:
            y_pred_model_1 = estimators[0].predict_proba(X_list[0])
            y_pred_model_2 = estimators[1].predict_proba(X_list[1])
            y_pred_model_3 = estimators[2].predict_proba(X_list[2])
            probs = np.array([(prob1 + prob2+ prob3) * (1/len(estimators)) for prob1, prob2, prob3 in zip(y_pred_model_1, y_pred_model_2, y_pred_model_3)])
        
        return probs

    def predict_best_five(self, X_list, estimators, max_k_feat):
        """
        Selects the k classes with highest probability for samples in X_list obtained from predict_proba() method .
        
        Parameters 
        ----------
        X_list : list of array_like or sparse matrix of shape (n_samples, n_features)
            [X_name, X_description, X_image] to pass to predict_proba()
        estimators: list of pretrained models to be combined in the following order [name_model, name_description_model, image_model]
        Returns

        estimators : list List of models to be combined

        max_k_feat : int number of classes
        
        Return
        -------
        dict_max_feat: python dict dictionary with classes with highest probability
            
        """
        
        probs = self.predict_proba(X_list, estimators)

        cat_prob = probs
        classes = estimators[0].classes_

        most_prob_cat_idx = np.argsort(-cat_prob[0])[:max_k_feat]
        name_cat_max= []
    
        for idx in most_prob_cat_idx:
            nm_cat = classes[idx]
            name_cat_max.append(nm_cat)

        dict_max_feat = {}
        for items in range(len(name_cat_max)):
          dict_max_feat[str(items)] = np.array_str(decoder(name_cat_max[items]))

        return dict_max_feat 
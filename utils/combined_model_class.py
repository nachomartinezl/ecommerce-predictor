import numpy as np
import os
import yaml

from utils.decoder import decode_id_path

class Combined_Model:

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

        if len(estimators) == 2:
            y_pred_model_1 = estimators[0].predict_proba(X_list[0])
            y_pred_model_2 = estimators[1].predict_proba(X_list[1])
            prob_cat = np.array(
                [
                    (prob1 + prob2) * (1 / len(estimators))
                    for prob1, prob2 in zip(y_pred_model_1, y_pred_model_2)
                ]
            )

        # NLP + images
        elif len(estimators) == 3:
            CONFIG_YML = "exp4.yml"
            config = utils.load_config(CONFIG_YML)

            y_pred_model_1 = estimators[0].predict_proba(X_list[0])
            y_pred_model_2 = estimators[1].predict_proba(X_list[1])

            _, _, probs = utils.predict_from_folder(
                folder=X_list[2],
                model=estimators[2],
                input_size=config["data"]["image_size"],
                class_names=estimators[0].classes_,
            )
            y_pred_model_3 = probs[0]
            prob_cat = np.array(
                [
                    (prob1 + prob2 + prob3) * (1 / len(estimators))
                    for prob1, prob2, prob3 in zip(
                        y_pred_model_1, y_pred_model_2, y_pred_model_3
                    )
                ]
            )

        return prob_cat

    def predict(self, X_list, estimators):
        pred_prob_cat = self.predict_proba(X_list, estimators)
        cat = np.argmax(pred_prob_cat, axis=1)
        
        classes = estimators[0].classes_
        name_cat_max = []
        
        for idx in cat:
            nm_cat = classes[idx]
            name_cat_max.append(nm_cat)
        return np.array(name_cat_max)

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

        cat_prob = self.predict_proba(X_list, estimators)

        classes = estimators[0].classes_

        most_prob_cat_idx = np.argsort(-cat_prob[0])[:max_k_feat]
        name_cat_max = []

        for idx in most_prob_cat_idx:
            nm_cat = classes[idx]
            name_cat_max.append(nm_cat)

        dict_max_feat = {}
        for items in range(len(name_cat_max)):
            dict_max_feat[str(items)] = decode_id_path(name_cat_max[items])

        return dict_max_feat

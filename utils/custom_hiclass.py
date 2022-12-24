from hiclass import LocalClassifierPerParentNode
from sklearn.utils.validation import check_array, check_is_fitted
import numpy as np

class CustomLocalClassifierPerParentNode(LocalClassifierPerParentNode):
    def predict_5(self, X):
        # Check if fit has been called
        check_is_fitted(self)

        # Input validation
        X = check_array(X, accept_sparse="csr")

        # Initialize array that holds predictions
        y0 = np.empty((X.shape[0], self.max_levels_), dtype=self.dtype_)
        y1 = np.empty((X.shape[0], self.max_levels_), dtype=self.dtype_)
        y2 = np.empty((X.shape[0], self.max_levels_), dtype=self.dtype_)
        y3 = np.empty((X.shape[0], self.max_levels_), dtype=self.dtype_)
        y4 = np.empty((X.shape[0], self.max_levels_), dtype=self.dtype_)

        self.logger_.info("Predicting")

        # Predict first level
        classifier = self.hierarchy_.nodes[self.root_]["classifier"]

        c0 = []
        c1 = []
        c2 = []
        c3 = []
        c4 = []
        for i in classifier.predict_proba(X):
            ind = np.flip(np.argpartition(i, range(len(i)))[-5:])
            classes = classifier.classes_[ind]
            c0.append(classes[0])
            c1.append(classes[1])
            c2.append(classes[2])
            c3.append(classes[3])
            c4.append(classes[4])
        y0[:,0] = c0
        y1[:,0] = c1
        y2[:,0] = c2
        y3[:,0] = c3
        y4[:,0] = c4
        y_all = [y0, y1, y2, y3, y4]
           
        for y in y_all:
            self._predict_remaining_levels(X, y)

            y = self._convert_to_1d(y)

            self._remove_separator(y)
                    
        return y_all
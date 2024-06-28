import string
import warnings
from math import log

import numpy as np
import pandas as pd  # type: ignore

warnings.simplefilter(action="ignore", category=FutureWarning)


class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.alpha = alpha
        self.classes_psb = None
        self.prior_psb = dict()
        self.model = pd.DataFrame()

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.classes_psb = list(set(y) - {None})
        features = self.classes_psb.copy()
        features.insert(0, "word")

        for cls in features:
            self.model[cls] = []

        for cls in list(self.classes_psb) + ["all"]:
            self.prior_psb.update(({cls: y.count(cls) / len(y)}))

        for sntcs, cls in zip(X, y):
            translator = str.maketrans("", "", string.punctuation)
            bow = sntcs.translate(translator).split()

            for word in bow:
                if word in self.model["word"].values:
                    self.model.loc[self.model["word"] == word, cls] += 1
                else:
                    new_row = {col: 0 for col in features}
                    new_row["word"] = word
                    new_row[cls] = 1
                    self.model = self.model.append(new_row, ignore_index=True)

        for cls in self.classes_psb:
            p_column = []
            nk = np.count_nonzero(self.model[cls])
            m = self.model.shape[0]

            for index, row in self.model.iterrows():
                nik = row[cls]
                p = (self.alpha + nik) / (self.alpha * m + nk)
                p_column.append(p)
                self.model[f"{cls} prb"] = p_column


    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        pred = []

        for sntcs in X:
            cls_distibution = dict()

            for cls in self.classes_psb:
                cls_distibution.update({cls: 0})

            for cls in self.classes_psb:
                translator = str.maketrans("", "", string.punctuation)
                bow = sntcs.translate(translator).split()
                rpb = log(self.prior_psb[cls])  # rpw - result per bag of words

                for word in bow:
                    try:
                        rpb += log(self.model.loc[self.model["word"] == word, f"{cls} prb"].values[0])
                    except IndexError:
                        rpb += 0

                cls_distibution.update({cls: rpb})

            max_key = max(cls_distibution, key=cls_distibution.get)
            pred.append(max_key)

        return pred

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        predictions = self.predict(X_test)
        correct_predictions = sum(y == pred for y, pred in zip(y_test, predictions))
        accuracy = correct_predictions / len(y_test)

        return accuracy


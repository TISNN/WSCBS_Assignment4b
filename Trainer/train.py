#!/usr/bin/env python3

import yaml
import sys
import os
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
#from sklearn.externals import joblib

def train_predict(source: str) -> str:
    # pd.read_csv(f"/data/train.csv")
    train = pd.read_csv(f"/data/train_traindata.csv")
    test = pd.read_csv(f"/data/test_testdata.csv")
    testid=pd.read_csv(f"/data/test.csv")
    X = train.values[:,1:]
    y = train.values[:,0]

    if source == "knn":
        knn = KNeighborsClassifier(n_neighbors = 3)
        knn.fit(X, y)
        Y_pred = knn.predict(X)
        acc_knn = round(knn.score(X, y) * 100, 2)
        #joblib.dump(knn, f"/data/knn.pkl")
        predictions = knn.predict(test)
        PassengerId=testid['PassengerId']
        prdict_test = pd.DataFrame({"PassengerId": PassengerId, "Survived": predictions.astype(np.int32)})
        prdict_test.to_csv(f"/data/{source}_results.csv")

        return "Accuracy of KNN model is "+ str(acc_knn) + " and the KNN results was saved at ./data"

    if source == "decision_tree":
        decision_tree = DecisionTreeClassifier()
        decision_tree.fit(X, y)
        Y_pred = decision_tree.predict(X)
        acc_decision_tree = round(decision_tree.score(X, y) * 100, 2)
        #joblib.dump(decision_tree, 'decision_tree.pkl')
        predictions = decision_tree.predict(test)
        PassengerId=testid['PassengerId']
        prdict_test = pd.DataFrame({"PassengerId": PassengerId, "Survived": predictions.astype(np.int32)})
        prdict_test.to_csv(f"/data/{source}_results.csv")

        return "Accuracy of decision tree model is "+ str(acc_decision_tree) + " and the decision_tree results was saved at ./data"


if __name__ == "__main__":
    # Make sure that at least one argument is given, that is either 'write' or 'read'
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} write|read")
        exit(1)

    # If it checks out, call the appropriate function
    command = sys.argv[1]
    if command == "train_predict":
        print(yaml.dump({ "contents": train_predict(os.environ["SOURCE"]) }))

import lightgbm as lgb
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, r2_score


class Regressor:

    def train_model(self):

        #read training data from csv into list
        data = np.loadtxt("training_labeled.csv", delimiter=",")

        #extract rows and output column
        x = np.delete(data, -1, axis=1)
        y = data[:, -1]
        y = np.clip(y, 20, 60) #remove outliers


        #init model
        params = {
            "objective": "regression",
            "metric": "rmse",
            "learning_rate": 0.02,
            "num_leaves": 12,
            "max_depth":4,
            "feature_fraction": 0.7,
            "bagging_fraction": 0.7,
            "bagging_freq": 1,
            "lambda_l2": 3.0,
            "lambda_l1": 1.0,
            "verbosity": -1
        }

        kf = KFold(n_splits=10) #init cross validation
        rmse =[]
        r2 = []

        for train_index, test_index in kf.split(x):

            #get iterations test / val set
            X_train = x[train_index]
            X_test = x[test_index]

            y_train = y[train_index]
            y_test = y[test_index]


            training = lgb.Dataset(X_train, label=y_train)
            testing = lgb.Dataset(X_test, label=y_test)

            #train model
            model = lgb.train(params, training, num_boost_round=1500, valid_sets=[training, testing], valid_names=["train", "test"])
        
            #predict on test
            y_pred = model.predict(X_test, num_iteration=model.best_iteration)
        
            #metrics
            rmse.append(np.sqrt(mean_squared_error(y_test, y_pred)))
            r2.append(r2_score(y_test, y_pred))

        print(np.std(y))
        return np.mean(rmse), np.mean(r2), model
    

    def predict_query(self, data):

        rsme,r2,model = self.train_model()

        query = np.array([data])

        prediction = model.predict(query)

        return round(prediction[0],1), rsme, r2


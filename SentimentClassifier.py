
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score

class SentimentClassifier:


    def train_nlp(self):
        data = pd.read_csv("sentiment_training.csv") #read training data

        label_map = {"genuine": 0, "speculative": 1}
        data["label_num"] = data["label"].map(label_map)

        
        X = data["text"].values
        y = data["label_num"].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=24, stratify=y)

        pipe = Pipeline([
            ("tfidf", TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1,2),
                max_df=0.95,
                min_df=2,

            )),
            ("clf", LogisticRegression(
                C=2.0,
                max_iter=500,
                class_weight="balanced",
                n_jobs=-1
            ))
        ])

        pipe.fit(X_train, y_train)


        y_pred = pipe.predict(X_test)

        acc =accuracy_score(y_test, y_pred)
        p = precision_score(y_test, y_pred)
        r = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)

        return pipe



    def predict_posts(self, data):

        model = self.train_nlp()

        post_pred = model.predict(data)


        genuine_counter = 0
        for pred in post_pred:
            if pred == 0:
                genuine_counter += 1

        
        p = float(genuine_counter / len(post_pred))

        label = ""

        if p > 0.9:
            label = "Extermely Genuine"

        elif p > 0.75:
            label = "Very Genuine"
        
        elif p > 0.5:
            label = "Mostly Genuine"

        elif p > 0.25:
            label = "Mostly Speculative"

        elif p > 0.1:
            label = "Very Speculative"

        else:
            label = "Extremely Speculative"


        return label





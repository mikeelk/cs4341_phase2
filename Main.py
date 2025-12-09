from DataFetcher import *
from DataParser import *
from Regressor import *
from SentimentClassifier import *
from flask import Flask, request, jsonify


def main(initdata=None):

    if initdata is None:
        ticker = input("Which stock would you like to analyze? ")

    else:
        ticker = str(initdata)

    fetcher = DataFetcher(ticker)
    
    finviz = fetcher.fetch_finviz()
    trends = fetcher.fetch_trends()
    reddit = fetcher.fetch_reddit()

    parser = DataParser()

    posts = parser.extract_posts(reddit)
    data = parser.clean_numerical_data(finviz, trends, ticker)

    regressor = Regressor()

    pop_score, shap = regressor.predict_query(data)

    print(data)
    print(pop_score)



# if __name__ == "__main__":
#     main()

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"  # dev only
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.route("/PYapp", methods=["POST"])
def PYapp():
    data = request.get_json()
    print(data)
    ticker = data.get("ticker") if data else None
    if ticker is None or len(ticker) > 4:
        return 400
    else:
        result = main(ticker)

    print(result)

    return jsonify({"score": result})


app.run(debug=True)



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

    index_map = {0: "Short Float", 1: "Short Ratio", 2: "Short Interest", 3: "Relative Volume",
                 4: "Change", 5: "Weekly Volatility", 6: "Monthly Volatility", 7: "ATR (14)",
                   8: "Recent Google Intrest", 9: "Average Google Iterest", 10: "Google Interest Momentum"}

    i = np.argsort(np.array(shap))


    drivers = [index_map[index] for index in list(i[0][:3])]

    nlp = SentimentClassifier()


    label = nlp.predict_posts(posts)

    print(f'The popularity score for {ticker} is {pop_score}/100.\nThe top popularity drivers are {", ".join(drivers)}.\nThe quality of hype surrounding this stock is {label}')

    return pop_score, drivers, label



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
        result, drivers, label = main(ticker)

    print(result)

    return jsonify({"score": result})


app.run(debug=True)



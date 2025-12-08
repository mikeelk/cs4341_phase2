from DataFetcher import *
from DataParser import *
from Regressor import *


def main():

    ticker = input("Which stock would you like to analyze? ")

    fetcher = DataFetcher(ticker)
    
    finviz = fetcher.fetch_finviz()
    trends = fetcher.fetch_trends()

    parser = DataParser()

    data = parser.clean_numerical_data(finviz, trends, ticker)

    regressor = Regressor()

    pop_score, rmse, r2 = regressor.predict_query(data)

    print(data)
    print(pop_score)




if __name__ == "__main__":
    main()

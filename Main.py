from DataFetcher import *
import DataParser

def main():

    client = DataFetcher("AAPL")

    print(client.fetch_reddit()) #test functions here


if __name__ == "__main__":
    main()

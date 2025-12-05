import DataFetcher
import DataParser

def main():

    client = DataFetcher("AAPL")

    print(client.fetch_finviz()) #test functions here


    


if __name__ == "__main__":
    main()

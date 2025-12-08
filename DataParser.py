import statistics

class DataParser:

    """
    Extracts datapoints from pytrends dataframe

    Args
        data (DataFrame): DataFrame of pytrends output
        stock (str): stock ticker symbol, needed to know column name of df

    Returns: Array of datapoitns
    """ 
    def parse_trends(self, data, stock):

        interest_column = data[stock]

        most_recent = interest_column.iloc[-1]
        mean_interest = statistics.mean(interest_column)
        interest_momentum = most_recent - mean_interest


        return [int(most_recent), mean_interest, float(interest_momentum)]


    """
    Organizes numerical data into array

    Args
        data (Array of int/float): Array of finviz output
        stock (str): stock ticker symbol, needed to call parse_trends and append trends data

    Returns: Array of datapoitns
    """ 

    def clean_numerical_data(self, finviz, trends, stock):

        finviz_clean = [float(finviz[0][:-1])/100.0, float(finviz[1]), float(finviz[2][:-1])*1000000.0, float(finviz[3]), float(finviz[4][:-1])/100.0,float(finviz[5][:-1])/100.0, float(finviz[6][:-1])/100.0, float(finviz[7])]

        return finviz_clean +self.parse_trends(trends, stock)

    """
    Extracts reddit posts from json returned by api

    Args
        data (json): json body returned by reddit api

    Returns: Array of str containing only the post contents
    """ 
    def extract_posts(self, data):
        posts = []

        for post in data["data"]["children"]:

            p = post["data"]
            posts.append(p.get("selftext", ""))

        return posts


"""
Title: Sample BoW XGBoost Model
Description: This strategy will use Bag of Words vectoriser to convert news headlines dataset into vectors.
             You will pass these vectors to the XGBoost model to train the model and predict 
             the sentiments of the news headlines. Based on the sentiments, you will place orders.

Note:
Need to place this file within the Strategies folder of the IBridgepy Installation folder. 
Place the pickle file you generated from the trained model in the IBridgepy Installation folder along with the RUN_ME.py. 

############################# DISCLAIMER #############################
This is a strategy template only and should not be
used for live trading without appropriate backtesting and tweaking of
the strategy parameters.
######################################################################
"""
# Import pickle
import pickle

# Import webhoseio
import webhoseio

# Enter your API key
webhoseio.config(token=api_key)

# Apply the filters
filter = {
    "q": "language:english site_type:news site_category:financial_news Apple or AAPL",
}
cursors = webhoseio.query("filterWebContent", filter)

# Define a function 'store_headlines' with parameters df and cursors
def store_headlines(df, cursors):

    # Run a for loop over the length of posts
    # Get the publishing date, title and text of the news headlines
    for i in range(len(cursors['posts'])):
        date = cursors['posts'][i]['published']
        title = cursors['posts'][i]['title']
        posts = cursors['posts'][i]['text']

        # Append the 'Date', 'Title' and 'New_Headlines'
        df = df.append({'Date': date, 'Title': title,
                        'News_Headlines': posts}, ignore_index=True)
    return df


def initialize(context):

    context.security = symbol('BAC')
    context.lookback = 30

def handle_data(context, data):

    # Create a dataframe with column name 'Date', 'Title' and 'New_Headlines'
    df = pd.DataFrame(columns=['Date', 'News_Headlines', 'Post'])
    df = store_headlines(df, cursors)

    # Load the model
    model = pickle.load(open('bow_xgboost.pkl', 'rb'))

    signal = model.predict(df.News_Headlines)
    score = signal.mean()

    # Fetch the data
    hist = data.history(context.security, 'close', context.lookback, '1m')

    # If the sentiment is positive then buy
    if score[-1] > 0:
        order_target_percent(context.security, 1)

    # If the sentiment is not positive then sell
    else:
        order_target_percent(context.security, -1)
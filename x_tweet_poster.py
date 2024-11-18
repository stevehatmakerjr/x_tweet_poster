import pandas as pd
import tweepy

# Replace these with your actual X (Twitter) API credentials
TWITTER_API_KEY = 'API_KEY'
TWITTER_API_SECRET = 'API_SECRET'
TWITTER_ACCESS_TOKEN = 'ACCESS_TOKEN'
TWITTER_ACCESS_SECRET = 'ACCESS_SECRET'

# Authenticate using tweepy.Client for v2 API (posting tweets)
client = tweepy.Client(
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_SECRET
)

# Read the Excel file
df = pd.read_excel('x_post_list.xlsx')

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    product_name = str(row['ProductName'])
    price = str(row['Price'])
    url = str(row['URL'])

    # Construct the tweet text
    tweet_template = "Check out {ProductName} that is currently ${Price} Click here for more details {URL}"
    tweet_text = tweet_template.format(ProductName=product_name, Price=price, URL=url)

    # Twitter character limit
    max_length = 280

    # If tweet is too long, shorten the ProductName
    if len(tweet_text) > max_length:
        # Calculate allowed length for ProductName
        extra_chars = len(tweet_text) - len(product_name)
        allowed_length = max_length - extra_chars - 3  # Subtract 3 for '...'

        # Ensure allowed_length is not negative
        allowed_length = max(allowed_length, 0)

        # Shorten ProductName and add '...'
        product_name_short = product_name[:allowed_length] + '...'
        tweet_text = tweet_template.format(ProductName=product_name_short, Price=price, URL=url)

    try:
        # Post the tweet using tweepy.Client (v2)
        tweet_response = client.create_tweet(text=tweet_text)

        print(f"Tweet posted successfully. Tweet ID: {tweet_response.data['id']}")

    except tweepy.TweepyException as e:
        print(f"An error occurred with Tweepy: {e}")

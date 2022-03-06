import sys
import pandas as pd
import requests
from datetime import datetime


filename = "defi-posts.csv"
search = "defi"
url = "https://api.pushshift.io/reddit/search/submission/?q={}&size=1000&sort=desc&before=".format(
    search
)
start_time = int(datetime.utcnow().timestamp())
new_url = url + str(start_time)

while True:
    data = requests.get(new_url).json()
    posts = data['data']
    if len(data['data']) == 0:
        sys.exit("No results found with the given search string. Try something else.")

    data_columns = ('ID', 'DATE', 'TITLE', 'TEXT', 'LIKES', 'SUBREDDIT')


    # Get all post data and combine in a Python Dictionary
    for post in posts:
        post_data = {}

        post_data['id'] = post['id']

        date = datetime.utcnow().fromtimestamp(post['created_utc'])
        post_data['date'] = date.strftime("%Y-%m-%d %H:%M:%S")

        post_data['title'] = post['title']
        post_data['likes'] = post['score']
        post_data['subreddit'] = post['subreddit']
        post_data['text'] = post['selftext']

        # Save data to a pandas DataFrame
        df = pd.DataFrame(data=post_data, index=[0])

        df.to_csv(filename, mode='a', index=False, header=False)

    # Create a new url with the last queried timestamp
    next_time = str(post['created_utc'])
    new_url = url + next_time

    print(next_time, post_data['date'])
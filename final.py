import tweepy, requests, datetime, time, json,random,os

def load_data(file_path):
    with open(file_path) as f:
        return json.load(f)
    
def load_reply_texts(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()
proxies_file = 'proxies.txt'

def load_proxies(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()
proxy_list = load_proxies(proxies_file)

def create_comment(client, tweet_id, reply_text):
    response = client.create_tweet(text=reply_text, in_reply_to_tweet_id=tweet_id)
    created_tweet_id = response.data['id']
    print(f"Replied to tweet!!! Click Here - https://twitter.com/anyuser/status/{created_tweet_id} with reply text:- {reply_text}")
    return created_tweet_id

test_url = 'http://api64.ipify.org?format=json'


def searcher_and_replier(search_query, bearer_token, reply_texts, accounts, delay, tweet_ids_list):
    search_url = 'http://api.twitter.com/2/tweets/search/recent'
    headers = {'Authorization': f'Bearer {bearer_token}'}
    yourProxy0 = random.choice(proxy_list)
    proxies = {'http': f"http://{yourProxy0}"}
    session = requests.Session()
    session.proxies = proxies
    
    current_account_index = 0

    while True:
        
        proxy_string = random.choice(proxy_list)
        server, port, username, password = proxy_string.split(':')
        os.environ['http_proxy'] = f"http://{username}:{password}@{server}:{port}"

        response = requests.get(test_url)
        print(f"Proxy used for searching tweets {response.text}")

        start_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
        params = {'query': search_query, 'start_time': start_time.strftime('%Y-%m-%dT%H:%M:%SZ'), 'max_results': 10}
        response = session.get(search_url, headers=headers, params=params)


        if response.status_code == 200:
            tweets = response.json()
            if 'data' in tweets and len(tweets['data']) > 0:
                tweet = tweets['data'][0]  # Get the first tweet
                tweet_id = tweet['id']
                if tweet_id not in tweet_ids_list:
                    tweet_ids_list.append(tweet_id)
                    tweet_url = f"http://twitter.com/anyuser/status/{tweet_id}"
                    print(f"Replying to this tweet - {tweet_url}")

        
        account = accounts[current_account_index]
        print(f"Account {current_account_index+1}")

        bearer_token, consumer_key, consumer_secret, access_token, access_token_secret,Twitterusername = (
            account["bearer_token"], account["consumer_key"], account["consumer_secret"], account["access_token"],
            account["access_token_secret"],account["Twitterusername"])

        try:

            client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

            if tweet_ids_list:
                proxy_string = random.choice(proxy_list)
                server, port, username, password = proxy_string.split(':')
                os.environ['http_proxy'] = f"http://{username}:{password}@{server}:{port}"
                response = requests.get(test_url)
                print(f"{Twitterusername}- used this proxy for replying {response.text}")

                tweet_id = tweet_ids_list.pop(0)
                reply_text = random.choice(reply_texts)
                create_comment(client, tweet_id, reply_text)
                time.sleep(delay)
                current_account_index = (current_account_index + 1) % len(accounts)

        except (tweepy.Unauthorized, Exception) as e:
            print(f"Error occurred for account {e}\n")
            current_account_index = (current_account_index + 1) % len(accounts)
            continue

accounts_file = 'cred.json'
reply_texts_file = 'reply.txt'
delay = 5

accounts = load_data(accounts_file)
reply_texts = load_reply_texts(reply_texts_file)

def load_keywords(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()

keyword_file = 'keyword.txt'
keywords = load_keywords(keyword_file)

random_keyword = random.choice(keywords)
print(f"Using the keyword --{random_keyword}--  for searching tweets")
search_query = f'{random_keyword} -is:retweet'

yourproxy1 = random.choice(proxy_list)
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHFCqQEAAAAAn%2BRr5uPoGBBeyNSlPkMAAa1tKtg%3D1FkUNmLGEi9VLoqZMcBt9HJ2xepflU2MDYXZqZFSvNGP4HtF4a'

tweet_ids_list = []

searcher_and_replier(search_query,bearer_token, reply_texts, accounts, delay, tweet_ids_list)
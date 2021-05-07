from kafka import KafkaProducer
from datetime import datetime
import tweepy as tw
import time

consumer_key= <API KEYS>
consumer_secret= <API SECRET KEYS>
access_token= <ACCESS TOKEN>
access_token_secret= <ACCESS TOKEN SECRET>

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth,wait_on_rate_limit=True)

def normalize_timestamp(time):
    mytime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    return (mytime.strftime("%Y-%m-%d %H:%M:%S"))
    
producer = KafkaProducer(bootstrap_servers='172.18.0.2:6667')
topic_name = 'tweets'

def get_twitter_data():
    res = api.search("covid19 OR corona virus")
    for i in res:
        record =''
        record+=str(i.user.id_str)
        record+= ';'
        record+= str(normalize_timestamp(str(i.created_at)))
        record+= ';'
        record+=str(i.user.followers_count)
        record+= ';'
        record+=str(i.retweet_count)
        record+= ';'
        record+=str(i.id_str)
        record+= ';'
        record+=str(i.user.screen_name)
        record+= ';'
        record+=str(i.user.location)
        record+= ';'
        record+=str(i.text)
        record+= ';'
        producer.send(topic_name, str.encode(record))
        
get_twitter_data()
def periodic_work(interval):
    while True:
        get_twitter_data()
        time.sleep(interval)
        
periodic_work(60* 0.1)


import pyspark.sql.functions
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from textblob import TextBlob
import pandas as pd
import tweepy as tw
import findspark
findspark.init()


if __name__ == "__main__":

    consumer_key= <API KEYS>
    consumer_secret= <API SECRET KEYS>
    access_token= <ACCESS TOKEN>
    access_token_secret= <ACCESS TOKEN SECRET>


    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth)

    spark = SparkSession.builder.appName("TwitterSentimentAnalysis").getOrCreate()
    
    Stream = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "172.18.0.2:6667").option("subscribe", "tweets")\
    .option("startingOffsets", "earliest").load()

    df= (Stream.withColumn("key", Stream["key"].cast(StringType()))
           .withColumn("value", Stream["value"].cast(StringType())))

    df= df.select("value")

    split_col = pyspark.sql.functions.split(df['value'], ';')
    df = df.withColumn("User_ID", split_col.getItem(0))
    df = df.withColumn("Tweet_time", split_col.getItem(1))
    df = df.withColumn("Followers_Count", split_col.getItem(2))
    df = df.withColumn("Retweet_Count", split_col.getItem(3))
    df = df.withColumn("tweetID", split_col.getItem(4))
    df = df.withColumn("User_Handel", split_col.getItem(5))
    df = df.withColumn("Location", split_col.getItem(6))
    df = df.withColumn("Tweet_Text", split_col.getItem(7))


    df = df.drop("value")


    print(type(df))

    def sentiment_analysis(tweet_text):
        analysis = TextBlob(tweet_text)
        if analysis.sentiment.polarity > 0:
            return 'positive'
            
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
            
        else:
            return 'negative'

            
    def reply_to_tweet(tweet):
        username = tweet.User_Handel
        if tweet.message=="positive":
          msg = "@%s Spread positivity!"%username
        else:
          msg = "@%s Stay Safe!" %username
        msg_sent = api.update_status(msg, tweet.tweetID)
    
    
    udf_sentiment = udf(sentiment_analysis, StringType())
    df = df.withColumn("Sentiment", udf_sentiment("Tweet_Text"))
    
    reply_query = df.writeStream.foreach(reply_to_tweet).start()
    
    query = df \
        .writeStream \
        .format("parquet") \
        .option("path", "hdfs://sandbox-hdp.hortonworks.com:8020/apps/hive/warehouse/test1.db/tweets")\
        .option("checkpointLocation", "hdfs://sandbox-hdp.hortonworks.com:8020/apps/hive/warehouse/test1.db/CheckPoint")\
        .start()

    query.awaitTermination()
    spark.stop()
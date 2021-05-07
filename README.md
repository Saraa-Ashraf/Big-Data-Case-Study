<H1>Sentiment analysis on streaming twitter data using Spark Structured Streaming & Python </H1>

In this project I am presenting an end-to-end architecture on how to stream data from Twitter, clean it, and apply a simple sentiment analysis model to detect the polarity of each tweet and reply to each tweet according if it's a negative or positive tweets, 
then I attempt to visualize the data using Power BI as a visualization tool connected to Hive table to answer business questions regarding the situation of COVID19 in India.


## Project Architecture Description
STEP1: Setting up the Development Environment.<br>
STEP2: Acquiring Twitter Data into Kafka Topic.<br>
STEP3: Preprocess tweets using pyspark code.<br>
STEP4: Apply sentiment analysis.<br>
STEP5: Reply to tweets according to the sentiment analysis result.<br>
STEP6: Create a Hive Table to store data.<br>
STEP7: Save the parquet file on top of a HDFS dir.<br>
STEP8: Connect Microsoft Power BI with Hive.<br>
STEP9: Start Visualizing to answer business questions.<br>

Attached a .png Image describes the Project Architecture and the flow of data (Twitter Tweets).

The purpose of using Kafka is to have a queue where messages (Twitter Tweets) can be safely stored while awaiting for processing by a consumer, 
since the processing part can be relatively slower than the fetching from Twitter’s API. 
It acts as a FIFO — First-in first-out — datastore.

For the processing of real-time data, we need systems that support stream processing, such as Apache Spark.
Apache Spark provides two ways of working with streaming data; Spark Streaming and Spark Structured Streaming. 
I used Spark Structure Streaming because is more inclined towards real-time stream processing.

<b>Input data:</b> Live tweets from twitter with a keyword <br>
<b>Main model:</b> Data preprocessing and apply sentiment analysis on the tweets <br>
<b>Output:</b> A parquet file with all the tweets and their sentiment analysis state saved on hive table on top of HDFS and different visualizations created according to the extracted data<br>


## Main Libraries
<b> tweepy:</b> interact with the Twitter Streaming API and create a live data streaming pipeline with Twitter <br>
<b> pyspark: </b>preprocess the twitter data (Python's Spark library) <br>
<b> textblob:</b> apply sentiment analysis on the twitter text data <br>

## Development Environment 
1- Register for the Twitter Developer Account Application to provide an authorized access to pull live data through their API.<br>
2- Configure HDP SandBox 2.6.5<br>
3- Synchronizes System Clock with UTC (Universal Time Coordination), which Sandbox runs on, and it is needed to avoid running into authorization errors when connecting to the Twitter API.<br>
    <b>ntpdate -u time.google.com</b><br>
4- Create a Virtual Environment to run Python and PySpark Code with earlier versions and install all the needed libs on it. <br>
	<b>Python3.6 –m venv ./iti41</b><br>
	<b>source iti41/bin/activate</b><br>

## Instructions to run the project
First, run the <b>Part 1:</b> <i>Fetching_Tweets.py</i> and let it continue running. <br> 
	<b>python Fetching_Tweets.py</b><br>
Then, run the <b>Part 2:</b> <i>Sentiment_Analysis.py</i> from a different cmd. <br>
	<b>spark-submit --packages org.apache.spark:spark-streaming-kafka-0-10_2.12:2.4.3,org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.3 Sentiment_Analysis.py</b>

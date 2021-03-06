from opencage.geocoder import OpenCageGeocode
import streamlit as st
import os
import tweepy as tw
import pandas as pd
from textblob import TextBlob
import plotly.graph_objects as go

api_key = 'EHQ0MqA1nubDwv3G0Q4HyRtOg'
api_secret_key = 'vZFBEl7VDgMdTHKWR6QuIigJk7Ssd3qsYRH0a4goryLM7FaoCX'
access_token = '1358825958392754178-0YbtWtO9wcEEULprlYeImaAxwFOZ6x'
access_token_secret = 'gW6sWqrs10x6iBaewaoh9H4sSYIDJ9fCBGhB1zNJZYe1k'
key='06e141dcc97045b18d9854d5a0cf3987'


auth = tw.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
geocoder = OpenCageGeocode(key)

st.title("Tweet Sentiment Analyzer")
word=st.text_input("Enter the search topic for the tweets: ")
query = st.text_input("Enter the area you want to search: ")
search_words = "#"+word    
date_since = "2021-02-01"
if query:
    rad=st.text_input("Enter the search radius in miles: ")
    if rad:
        results = geocoder.geocode(query)
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        lat=str(lat)
        lng=str(lng)
        rad=str(rad)
        coord=lat+','+lng+','+rad+'mi'
        tweets = tw.Cursor(api.search,geocode=coord,q=search_words,lang="en",since=date_since).items(50)

        clean_tweets=[]
        clean_tweets=[tweet.text for tweet in tweets if 'RT @' not in tweet.text ]
        def analyze():
            positive_tweets, negative_tweets = [], []
            for tweet in clean_tweets:
                tweet_polarity = TextBlob(tweet).sentiment.polarity
                if tweet_polarity<0:
                    negative_tweets.append(tweet)
                    continue
                positive_tweets.append(tweet)
            return positive_tweets, negative_tweets
        positive, negative = analyze()
        
        st.header("Positive Tweets: \n")
        i=1
        for tweet in positive:
            st.write(i,']   ',tweet)
            i+=1
        st.header("\n\nNegative Tweets: \n")
        i=1
        for tweet in negative:
            st.write(i,']   ',tweet)
            i+=1

        st.header("\n\nComparison: \n")
        pas=len(positive)
        neg=len(negative)                
        labels = ['Positive','Negative']
        values = [pas,neg]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        st.plotly_chart(fig)

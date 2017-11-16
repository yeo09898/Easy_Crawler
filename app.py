from flask import Flask, request, redirect, url_for, render_template ,send_file, send_from_directory
import os
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shuzi@localhost/Web_Crawler'
app.debug = True
#db = SQLAlchemy(app) 

class requested_tags():
    tags = ""
    time = 0
import string
import json
import matplotlib.pyplot as plt
import tweepy
# to install tweepy, use: pip install tweepy
# import twitter authentication module
from tweepy import OAuthHandler
# import tweepy steam module
from tweepy import Stream
# import stream listener
from tweepy.streaming import StreamListener
# import the python package to handle datetime
import datetime

# set your keys to access tweets 
consumer_key = '7IKU6Hu1SfGPpyelNdJQOsMFc'
consumer_secret = 'rIibmcfcKxP6Z1o1owJz7kNc07R8odwlXqQZLi6twL7o6A0tMg'
access_token = '910751477613912064-5RlHjVTdAkAydsBfQeMDR7fGRWMMP65'
access_secret = 'KD2sFx2dGgTaeTrvoPYLVLcmPCiD9Py9O19XenU0SDx0g'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
class MyListener(StreamListener):
    # constructor
    def __init__(self, output_file, time_limit):
            # attribute to get listener start time
            self.start_time=datetime.datetime.now()
            
            # attribute to set time limit for listening
            self.time_limit=time_limit
            
            # attribute to set the output file
            self.output_file=output_file
            
            # initiate superclass's constructor
            StreamListener.__init__(self)
    
    # on_data is invoked when a tweet comes in
    # overwrite this method inheritted from superclass
    # when a tweet comes in, the tweet is passed as "data"
    def on_data(self, data):
        
        # get running time
        running_time=datetime.datetime.now()-self.start_time
        print(running_time)
        # check if running time is over time_limit
        if running_time.seconds/60.0<self.time_limit:    
            # ***Exception handling*** 
            # If an error is encountered, 
            # a try block code execution is stopped and transferred
            # down to the except block. 
            # If there is no error, "except" block is ignored
            try:
                # open file in "append" mode
                with open(self.output_file, 'w') as f:
                    # Write tweet string (in JSON format) into a file
                    f.write(data)
                    
                    # continue listening
                    return True
                
            # if an error is encountered
            # print out the error message and continue listening
            
            except BaseException as e:
                print("Error on_data:" , str(e))
                
                # if return "True", the listener continues
                return True
            
        else:  # timeout, return False to stop the listener
            print("time out")
            return False
    # on_error is invoked if there is anything wrong with the listener
    # error status is passed to this method
    def on_error(self, status):
        print(status)
        # continue listening by "return True"
        return True

def get_data(tags,time):
    tweet_listener=MyListener(output_file="doc/python.txt",time_limit=time)
    # start a staeam instance using authentication and the listener
    twitter_stream = Stream(auth, tweet_listener)
    # filtering tweets by topics
    twitter_stream.filter(track=[tags])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result/<tags>+<time>')
def result(tags,time):
    return render_template('result.html', tags=tags, time=time)

@app.route('/post_tags', methods=['POST'])
def post_tags():
    requested_tags.tags = request.form['tags']
    requested_tags.time = int(request.form['time'])
    print requested_tags.tags
    get_data(requested_tags.tags,requested_tags.time)
    return render_template('result.html', tags=requested_tags.tags, time=requested_tags.time)

@app.route("/download/")
def download_file():
    directory = os.getcwd()
    return send_from_directory(directory, 'doc/python.txt', as_attachment=True)


if __name__ == "__main__":
    app.run()

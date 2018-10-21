from flask import Flask, request, redirect, url_for, render_template, send_file, send_from_directory, session, \
    make_response
import os
import cralwer
import stackoverflow_scraper
import yelp_scraper
import time

# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shuzi@localhost/Web_Crawler'


# db = SQLAlchemy(app)
# SESSION_TYPE = 'redis'
path = "C:\Users\Bear\class\Easy_Crawler\doc"
class requested_tags():
    tags = ""
    time = 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result/<tags>+<time>')
def result(tags, time):
    requested_tags.tags = tags
    requested_tags.time = time
    return render_template('result.html', tags=requested_tags.tags, time=requested_tags.time)


@app.route('/post_tags', methods=['POST'])
def post_tags():
    requested_tags.tags = request.form['tags']
    requested_tags.time = int(request.form['time'])
    #    print requested_tags.tags
    #    print requested_tags.time
    selection = request.form['selection']
    # print selection
    if selection == "Twitter":
        cralwer.get_data(requested_tags.tags, requested_tags.time)
    if selection == "Yelp":
        yelp_scraper.run(requested_tags.tags, requested_tags.time)
    if selection == "Stack Overflow":
        stackoverflow_scraper.run(requested_tags.tags, requested_tags.time)
    return render_template('result.html', tags=requested_tags.tags, time=requested_tags.time)


@app.route("/download/")
def download_file():
    directory = os.getcwd()
    return send_from_directory(directory, 'doc/'+requested_tags.tags+str(requested_tags.time)+'.csv', as_attachment=True)

def listDir(fileDir):
    for eachFile in os.listdir(fileDir):
        if os.path.isfile(fileDir+"/"+eachFile):   #if it's a file 
            ft = os.stat(fileDir+"/"+eachFile);
            ltime = int(ft.st_mtime); #get the last mod time
            #print "file"+path+"/"+eachFile+"the last mod time:"+str(ltime);
            ntime = int(time.time())-3600*12; #get present time -12 hours
            if ltime<=ntime :         
                print "delete file in"+fileDir+"/"+eachFile;
                os.remove(fileDir+"/"+eachFile);   #delete file 12 hours ago

        elif os.path.isdir(fileDir+"/"+eachFile) :    #if it's a dir
            listDir(fileDir+"/"+eachFile);
			
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'redis'
    app.run(host='0.0.0.0',port=5000,threaded=True,debug=True) 
    while True :   
        time.sleep(3600*12);   
        print "12 hours wake up"
        listDir(path);

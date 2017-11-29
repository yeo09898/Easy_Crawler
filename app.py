from flask import Flask, request, redirect, url_for, render_template ,send_file, send_from_directory, session, make_response
import os
import cralwer
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shuzi@localhost/Web_Crawler'
app.debug = True
#db = SQLAlchemy(app)
#SESSION_TYPE = 'redis'

class requested_tags():
    tags = ""
    time = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result/<tags>+<time>')
def result(tags,time):
    requested_tags.tags = tags
    requested_tags.time = time
    return render_template('result.html', tags=requested_tags.tags, time=requested_tags.time)

@app.route('/post_tags', methods=['POST'])
def post_tags():
    requested_tags.tags = request.form['tags']
    requested_tags.time = int(request.form['time'])
#    print requested_tags.tags
#    print requested_tags.time
    cralwer.get_data(requested_tags.tags,requested_tags.time)
    return render_template('result.html', tags=requested_tags.tags, time=requested_tags.time)


@app.route("/download/")
def download_file():
    directory = os.getcwd()
    return send_from_directory(directory, 'doc/result.csv', as_attachment=True)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'redis'
    app.run()

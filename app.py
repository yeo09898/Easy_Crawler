from flask import Flask, request, redirect, url_for, render_template
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shuzi@localhost/Web_Crawler'
app.debug = True
#db = SQLAlchemy(app) 

class requested_tags():
    tags = ""
    time = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result/<tags>+<time>')
def result(tags,time):
    return render_template('result.html', tags=tags, time=time)

@app.route('/post_tags', methods=['POST'])
def post_tags():
    requested_tags.tags = request.form['tags']
    requested_tags.time = request.form['time']
    return render_template('result.html', tags=requested_tags.tags, time=requested_tags.time)

if __name__ == "__main__":
    app.run()

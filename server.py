from flask import Flask, request, jsonify, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import hashlib
import base64
import random
import os
import json
app = Flask(__name__)

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI']= os.getenv("DB_URI")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Url(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    key = db.Column(db.String(100))
    short_url = db.Column(db.String(100))
    long_url = db.Column(db.Text)
    def __init__(self, key, short_url, long_url):
        self.key = key 
        self.short_url = short_url
        self.long_url = long_url

def shortner(long_url):
    hashed_string = hashlib.sha256(long_url.encode('utf-8')).digest()
    b64 = base64.b64encode(hashed_string)
    b64= (b64.decode('utf-8'))
    shuffle = ''.join(random.sample(b64, len(b64)))
    final_url = shuffle.replace("/", "")
    final_url = final_url.replace("=","")
    return final_url[:7]

def error_message(message):
    res = json.dumps({'message':message})
    return Response(res, status=400, mimetype='application/json')

@app.route("/", methods = ["GET"])
def challenge():
    challenge =  "https://codingchallenges.fyi/challenges/challenge-url-shortener"
    return redirect(challenge,302)

@app.route("/home")
def home():
    msg = ("Welcome to my URL shortner! This is part of John Crickett's coding "
           "challenges. You can view this challenge here " 
           "https://codingchallenges.fyi/challenges/challenge-url-shortener "
           "You can also view my github solution to this here "
           "https://github.com/andrewkaldani/url_shortner"
           )
    return msg

@app.route("/solution", methods = ["GET"])
def my_soltion():
    return redirect("https://github.com/andrewkaldani/url_shortner")

@app.route("/add", methods = ['POST'])
def add_url():
    if not request.json:
        msg = "Request body MUST be in json format"
        return error_message(msg)
    if "url" not in request.json:
        msg = "url must be a key in your json request body"
        return error_message(msg)
    long_url = request.json["url"]

    url_db = Url.query.filter(Url.long_url == long_url).first()
    if url_db is None:
        key = shortner(long_url)
        shorten_url = "https://localhost:5000/"+key
        new_url = Url(key=key, short_url=shorten_url, long_url= long_url)
        db.session.add(new_url)
        db.session.commit()
        res = json.dumps({
            "key": key,
            "long_url": long_url,
            "short_url": shorten_url
        })
        return Response(res, status=302, mimetype='application/json')

    else:
        res = json.dumps({
            "msg":"url already exsists",
            "key":url_db.key,
            "short_url":url_db.short_url,
            "long_url": url_db.long_url
        })
        return Response(res, status=302, mimetype='application/json')


@app.route("/redirect/<key>", methods = ["GET"])
def redirect_url(key):
    check = Url.query.filter(Url.key == key).first()
    if check is None:
        msg = "This short url does not exist"
        return error_message(msg)
    else:
        return redirect(check.long_url,302)

@app.route("/delete",methods=["DELETE"])
def delete_url():
    if not request.json:
        msg = "Request body MUST be in json format"
        return error_message(msg)
    if "url" not in request.json:
        msg = "url must be a key in your json request body"
        return error_message(msg)
    url = request.json['url']
    check = Url.query.filter((Url.key == url)|(Url.long_url==url)).first()
    if check is None:
        res = json.dumps( "This url does not exist there is nothing to delete")
        return Response(res, status=404, mimetype='application/json')

    else:
        db.session.delete(check)
        db.session.commit()
        res = json.dumps( "Successfully Deleted the url from the database")
        return Response(res, status=202, mimetype='application/json')



if __name__ == '__main__':
    from server import app, db
    app.app_context().push()
    db.create_all()
    app.run(port=5000)
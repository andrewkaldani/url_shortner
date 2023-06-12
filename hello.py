
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import hashlib
import base64
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:pass@localhost:5432/shortner'
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    short_url = db.Column(db.String(100))
    long_url = db.Column(db.Text)



def shortner(long_url):
    hashed_string = hashlib.sha256(long_url.encode('utf-8')).digest()
    print(hashed_string)
    b64 = base64.b64encode(hashed_string)
    return (b64.decode('utf-8'))

def error_message(message):
    res = jsonify({'message':message})
    res.status_code = 400
    return res

@app.route("/home")
def hello():
    return "Hello World"

@app.route("/add")
def add_url(long_url):
    if not request.json or "url" not in request.json:


if __name__ == '__main__':
    app.run(port=5000)
   

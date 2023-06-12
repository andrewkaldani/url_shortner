
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
    # def __init__(self, short_url, long_url):
    #     self.short_url = short_url
    #     self.long_url = long_url




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

@app.route("/add", methods = ['POST'])
def add_url():
    if not request.json:
        msg = "Request body MUST be in json format"
        return error_message(msg)
    # if "url" not in request.json:
    #     msg = "url must be a key in your json request body"
    #     return error_message(msg)
    # long_url = request.json["url"]
    # shorten_url = shortner(long_url)
    # new_url = Test(short_url=shorten_url, long_url= long_url)
    # db.session.add(new_url)
    # db.session.commit()
    # res = {
    #     "key": shorten_url,
    #     "long_url": long_url
    # }
    # return jsonify(res)


if __name__ == '__main__':
    # from hello import app, db
    # app.app_context().push()
    # db.create_all()
    app.run(port=5000)
   

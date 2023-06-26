from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Url(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    key = db.Column(db.String(100))
    short_url = db.Column(db.String(100))
    long_url = db.Column(db.Text)
    def __init__(self, key, short_url, long_url):
        self.key = key 
        self.short_url = short_url
        self.long_url = long_url
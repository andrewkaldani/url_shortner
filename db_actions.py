from models import db, Url

class Actions:
    def __init__(self,query_key:str, key:str, shorten_url:str,long_url:str ) :
        self.query_key = query_key
        self.key = key 
        self.shorten_url = shorten_url
        self.long_url = long_url

    def query_db(query_key:str) -> Url:
        query = Url.query.filter((Url.key == query_key)|(Url.long_url==query_key)).first()
        return query
    def add_to_db(key:str,shorten_url:str,long_url:str) -> Url:
        add_url = Url(key=key, short_url=shorten_url, long_url= long_url)
        return add_url


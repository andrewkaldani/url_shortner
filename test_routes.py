from flask import Flask
import json 
import pytest
import coverage

from server import app, shortner, Url, db
app.app_context().push()
db.create_all()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_database_url():
    test_url = Url("wrtzhyr","https://localhost:wrtzhyr","https://gmail.com")
    assert test_url.key == "wrtzhyr"
    assert test_url.short_url == "https://localhost:wrtzhyr"
    assert test_url.long_url == "https://gmail.com"


def test_shortner():
    urla = "https://google.com"
    urlb = "https://codingchallenges.fyi/challenges/challenge-url-shortener"
    assert len(shortner(urla)) == 7
    assert len(shortner(urlb)) == 7

def test_base_route():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 302

def test_home_route(): 
    client = app.test_client()
    url = "/home"
    res = client.get(url)
    assert res.status_code == 200

def test_home_solution(): 
    client = app.test_client()
    url = "/solution"
    res = client.get(url)
    assert res.status_code == 302

def test_add_url():
    client = app.test_client()
    url = "/add"
    json_test = {
        "url":"https://gmail.com"
    }
    headers = {
        "Content-Type":'application/json'
    }
    res = client.post(url, headers= headers, data = json.dumps(json_test))
    assert res.status_code == 302
def test_url_key():
    json_test = {
        "dhu":"https://gmail.com"
    }
    test = False
    if 'url' in json_test.keys():
        assert test == False


def test_query_db():
    test_url = Url("KtM5543","https://localhost/KtM5543","https://gmail.com")
    db.session.add(test_url)
    url_db = Url.query.filter(Url.long_url == "https://gmail.com").first()
    assert url_db.key == "KtM5543"
    assert url_db.short_url == "https://localhost:5000/KtM5543"
    assert url_db.long_url == "https://gmail.com"









from flask import Flask
import json 
import pytest
import coverage
import requests
import requests_mock 
from server import app, shortner, db
from models import Url, db
app.app_context().push()
db.create_all()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def client(app):
    return app.test_client()

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

def test_base_route(requests_mock):
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 302


def test_base_route(requests_mock):
    requests_mock.get('http://127.0.0.1/', status_code=302)
    response = requests.get('http://127.0.0.1/')
    assert response.status_code == 302


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
    url_testing = {
        "url":"https://whatishappening.com"
    }
    headers = {
        "Content-Type":'application/json'
    }
    res = client.post(url, headers= headers, data = json.dumps(json_test))
    assert res.status_code == 302
    res = client.post(url, headers= headers, data = json.dumps(url_testing))
    assert b"url already exsists" in res.get_data()

def test_add_mock(requests_mock):
    url = "https://127.0.0.1/add"
    headers = {
        "Content-Type":'application/json'
    }
    expected_text = "url already exsists"
    requests_mock.post(url,status_code=302,text = json.dumps(expected_text),headers=headers )
    response = requests.post("https://127.0.0.1/add", headers=headers, json=({"url":"https://espn.com"}))
    assert response.status_code == 302
    assert "url already exsists" in response.json()
    new_text = "Succesfully added to DB"
    requests_mock.post(url,status_code=302,text = json.dumps(new_text),headers=headers )
    response = requests.post("https://127.0.0.1/add", headers=headers, json=({"url":"https://gmail.com"}))
    assert "Succesfully added to DB" in response.json()

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

    url_db = Url.query.filter(Url.long_url == "https://shouldbenone.com").first()
    assert url_db == None

def test_url_redirect():
    client = app.test_client()
    url = "/redirect/KtM5543"
    res = client.get(url)
    assert res.status_code == 302
    url = "/redirect/hello"
    res = client.get(url)
    assert b"This short url does not exist" in res.get_data()
    post_req = client.post(url)
    assert post_req.status_code == 405










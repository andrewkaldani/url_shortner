from flask import Flask
import json 
import pytest
import coverage

from server import app, shortner, Url


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client



def test_shortner():
    urla = "https://google.com"
    urlb = "https://codingchallenges.fyi/challenges/challenge-url-shortener"
    assert len(shortner(urla)) == 7
    assert len(shortner(urlb)) == 7

def test_base_route():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 302

def test_home_route(client): 
    client = app.test_client()
    url = "/home"
    res = client.get(url)
    assert res.status_code == 200







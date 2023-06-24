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









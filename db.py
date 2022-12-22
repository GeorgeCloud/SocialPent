from flask import Flask
from os import environ
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = bytes(environ.get('SECRET_KEY'), 'utf-8')

uri = environ.get('MONGODB_URI', 'mongodb://localhost:27017/reveal')
client = MongoClient(uri)

db = client.get_default_database()

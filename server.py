from flask import Flask, current_app, request, flash, redirect, url_for, render_template
from flask_pymongo import PyMongo
from dateutil.parser import parse
import os


app = Flask(__name__)
app.secret_key = 'secret'
# 以下でMongoDBの場所を指定。testdb(データベース)やuser(コレクション、SQLでいうテーブル)はあらかじめ作る必要なし。
app.config["MONGO_URI"] = os.environ.get('MONGODB_URI')
mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def show_entry():
	users = mongo.db.user.find()
	entries = []
	for row in users:
		entries.append({"name": row['name'], "birthday": row['birthday'].strftime("%Y/%m/%d")})
	return entries


@app.route('/add', methods=['POST'])
def add_entry():
    mongo.db.user.insert(
        {"name": request.form['name'], "birthday": parse(request.form['birthday'])})
    flash('New entry was successfully posted')
    return {"status": "success"}

@app.route('/search', methods=['POST'])
def filter_entry():
	start = parse(request.form['start'])
	end = parse(request.form['end'])
	cur = mongo.db.user.find({'birthday': {'$lt': end, '$gte': start}})
	results = []
	for row in cur:
		results.append({"name": row['name'], "birthday": row['birthday'].strftime("%Y/%m/%d")})
	return results


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

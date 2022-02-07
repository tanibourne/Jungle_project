from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           
client = MongoClient('localhost', 27017)  
db = client.dbsparta                      

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def listing():
    result = list(db.holo2.find({},{'_id':False}))  
    return jsonify({'result':'success', 'memos':result})

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def saving():
		
        title_receive = request.form['title_give']
        content_receive = request.form['content_give']

        doc = {'title': title_receive, 'content': content_receive}
        db.holo2.insert_one(doc)
        return jsonify({'result': 'success'})

@app.route('/memo/delete', methods=['POST'])
def memo_delete():
    title_receive = request.form['title_give']
    db.holo2.delete_one({'title':title_receive})
    return jsonify({'result': 'success'})


@app.route('/memo/update', methods=['POST'])
def update_set():
    new_title = request.form['new_title']
    new_content = request.form['new_content']
    old_title = request.form['old_title']
    db.holo2.update_one({'title':old_title},{'$set':{'title':new_title, 'content': new_content}})

    return jsonify({'result': 'success', 'msg': 'setting 연결 완료'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=4444, debug=True)
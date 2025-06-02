from flask import Flask, render_template, request, jsonify
import redis
import json
import os

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

COMMENTS_KEY = 'comments'

@app.route('/')
def main():
    comments_json = r.lrange(COMMENTS_KEY, 0, -1)
    comments = [json.loads(c) for c in comments_json]
    return render_template('main.html', comments=comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    name = request.form.get('name')
    comment = request.form.get('comment')
    if name and comment:
        r.rpush(COMMENTS_KEY, json.dumps({'name': name, 'comment': comment}))
    comments_json = r.lrange(COMMENTS_KEY, 0, -1)
    comments = [json.loads(c) for c in comments_json]
    return jsonify({'status': 'success', 'comments': comments})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

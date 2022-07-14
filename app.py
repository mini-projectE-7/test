from flask import Flask, jsonify, render_template, request, url_for, redirect
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import hashlib
import jwt
from datetime import datetime
from datetime import timedelta
import random
from werkzeug.utils import secure_filename

load_dotenv()
mongodbUri = os.environ.get('mongodbUri')

ca = certifi.where()
client = MongoClient(mongodbUri, tlsCAFile=ca)
db = client.liquor

SECRET_KEY = 'SPARTA'

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('home.html')
    # token_receive = request.cookies.get('mytoken')
    # try:
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #     print(payload)
    #     user_info = db.users.find_one({"userID": payload['id']})
    #     return render_template('index.html', user_info=user_info)
    # except jwt.ExpiredSignatureError:
    #     # return redirect(url_for("main"))
    #     return render_template('home.html')
    # except jwt.exceptions.DecodeError:
    #     # return redirect(url_for("main"))
    #     return render_template('home.html')


@app.route('/home')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        user_info = db.users.find_one({"userID": payload['id']})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        # return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
        return redirect(url_for("main"))


@app.route('/post')
def post():
    return render_template("post.html")


@app.route('/post/option', methods=["GET"])
def liquor_option():
    liquor_list = list(db.liquor.find({}, {'_id': False}))
    return jsonify({'liquors': liquor_list})


@app.route('/post/review', methods=["POST"])
def post_review():
    liquor = request.form['liquor_give']
    review_receive = request.form['review_give']
    review_list = list(db.review.find({}, {'_id': False}))
    count = len(review_list) + 1
    today = request.form['date_give']
    doc = {
        'num': count,
        'date': today,
        'liquor': liquor,
        'review': review_receive,
    }
    db.review.insert_one(doc)
    return jsonify({'msg': '리뷰등록 완료!'})


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/sign_in', methods=['POST'])
def sign_in():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    # 로그인때도 패스워스 암호화
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one(
        {'userID': username_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        mytoken = jwt.encode(payload, SECRET_KEY,
                             algorithm='HS256')
        return jsonify({'result': 'success', 'mytoken': mytoken})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/loginout', methods=["GET"])
def login_out():
    token_receive = request.cookies.get('mytoken')
    return jsonify({'result': 'success', 'token': token_receive})


@app.route('/join')
def join():
    return render_template("join.html")


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"userID": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/signUp', methods=["POST"])
def signUp():
    id_receive = request.form['id']
    pw_receive = request.form['pw']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        "userID": id_receive,
        "pw": pw_hash
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/review')
def review():
    return render_template("review.html")


@app.route("/reviewpage/review", methods=["GET"])
def review_list_get():
    review_list = list(db.review.find({}, {'_id': False}))
    print(review_list)
    return jsonify({'reviews': review_list})


@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅하기
        user_info = db.users.find_one({"userID": payload["id"]})
        comment_receive = request.form["comment_give"]
        date_receive = request.form["date_give"]
        doc = {
            "username": user_info["userID"],
            "profile_name": user_info["profile_name"],
            "profile_pic_real": user_info["profile_pic_real"],
            "comment": comment_receive,
            "date": date_receive
        }
        db.posts.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/random', methods=['GET'])
def getRandom():
    post_list = list(db.liquor.find({}, {'_id': False}))
    random_post = random.sample(post_list, 5)
    return jsonify({"random_posts": random_post})


@app.route('/random_review', methods=['GET'])
def getRandom_review():
    post_list = list(db.reviews.find({}, {'_id': False}))
    random_post = random.sample(post_list, 5)
    return jsonify({"random_posts": random_post})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

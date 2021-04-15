# Create your views here.
import json
import time
import jwt
import MySQLdb
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Create your views here.


conn = MySQLdb.connect('localhost', user="root", passwd="", db="JXC", charset='utf8')
# Select database
conn.select_db('JXC')
# get cursor
cursor = conn.cursor()


@csrf_exempt
def test(request):
    print(123)
    print(request)
    requestData = json.loads(request.body)
    print(requestData)
    dic = {'state': 200, 'message': "Success", 'number': 222}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))


def userlist(request):
    sql = "SELECT user_id,username,name,roles FROM users "
    cursor.execute(sql)
    users = []
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        users.append(res)
    dic = {'state': 200, 'message': "Success", 'userlist': users}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))


def add_users(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        users_names = requestData.get("username")
        users_pass = requestData.get("password")
        name = requestData.get("name")
        print(users_names)
        sql = "SELECT * FROM users WHERE username=\"" + users_names + "\""
        cursor.execute(sql)
        users = []
        while 1:
            res = cursor.fetchone()
            if res is None:
                break
            users.append(res)
        if len(users) == 0:
            # use pbkdf2_sha256
            print(users_names, users_pass)
            sha256_encrypt = make_password(users_pass, None, 'pbkdf2_sha256')
            # use pbkdf2_sha1
            sha1_encrypt = make_password(users_pass, None, 'pbkdf2_sha1')
            if len(users_names) > 0 and len(users_pass) > 0:
                sql = "insert into users values(%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (0, users_names, sha256_encrypt, sha1_encrypt, name,1))
                conn.commit()
                print(sha1_encrypt)
                dic = {'state': 200, 'message': "Success"}
                return HttpResponse(json.dumps(dic, ensure_ascii=False))
        else:
            dic = {'state': 200, 'message': "uplicate user name"}
            return HttpResponse(json.dumps(dic, ensure_ascii=False))


def deleteUser(request):
    requestData = json.loads(request.body)
    user_id = requestData.get("user_id")
    sql = "delete from users where user_id ="+user_id
    cursor.execute(sql)
    dic = {'state': 200, 'message': "Success delete"}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))


def get_login(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        print(requestData)
        users_names = requestData.get("username")
        users_pass = requestData.get("password")
        sql = "SELECT * FROM users WHERE username='" + users_names + "'"
        cursor.execute(sql)
        users = []
        while 1:
            res = cursor.fetchone()
            if res is None:
                break
            users.append(res)
        print(users)
        if len(users) == 1:
            ip = request.META.get("REMOTE_ADDR")
            print(ip)
            token = generate_token(ip, users_names)
            sha256_decode = check_password(users_pass, users[0][2])
            sha1_decode = check_password(users_pass, users[0][3])
            if sha256_decode and sha1_decode:
                conn.commit()
                dic = {'state': 200, 'message': "Success", "token": token,"roles":users[0][5]}
                res = HttpResponse(json.dumps(dic, ensure_ascii=False))
                return res
            else:
                dic = {'state': 200, 'message': "Failed", }
                res = HttpResponse(json.dumps(dic, ensure_ascii=False))
                return res
        else:
            dic = {'state': 200, 'message': "Failed", }
            res = HttpResponse(json.dumps(dic, ensure_ascii=False))
            return res


def generate_token(ip, users_names):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    salt = "asgfdgerher"
    exp = int(time.time() + 604800)
    payload = {
        "username": users_names,
        "exp": exp
    }
    print(payload)
    t = jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers)
    print(t)
    return t


def checkToken(request):
    token = request.COOKIES.get('token')
    print(token)
    salt = "asgfdgerher"
    try:
        info = jwt.decode(token, salt, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        print('token out date')
        print(info)
        dic = {'state': 300, 'message': "timeout"}
        return HttpResponse(json.dumps(dic, ensure_ascii=False))
    except jwt.InvalidTokenError:
        print('token error')
        dic = {'state': 300, 'message': "Failed"}
        return HttpResponse(json.dumps(dic, ensure_ascii=False))
    dic = {'state': 200, 'message': "Success"}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))

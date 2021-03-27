# Create your views here.
import json
import time
import MySQLdb
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Create your views here.


conn = MySQLdb.connect('localhost', user="root", passwd="root", db="JXC")
# Select database
conn.select_db('JXC')
# get cursor
cursor = conn.cursor()


@csrf_exempt
def test(request):
    dic = {'state': 200, 'message': "Success", 'number': 222}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))


def add_users(request):
    if request.method == "POST":
        users_names = request.POST.get("username")
        users_pass = request.POST.get("password")
        name = request.POST.get("name")
        sql = "SELECT * FROM users WHERE username='" + users_names + "'"
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
            if users_names != '' and users_pass != '':
                sql = "insert into users values(%s,%s,%s,%s,%s)"
                cursor.execute(sql, (0,users_names, sha256_encrypt, sha1_encrypt, name))
                conn.commit()
                print(sha1_encrypt)
                dic = {'state': 200, 'message': "Success"}
                return HttpResponse(json.dumps(dic, ensure_ascii=False))
        else:
            dic = {'state': 200, 'message': "uplicate user name"}
            return HttpResponse(json.dumps(dic, ensure_ascii=False))


def get_login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        users_names = request.POST.get("username")
        users_pass = request.POST.get("password")
        sql = "SELECT * FROM users WHERE username='"+users_names+"'"
        cursor.execute(sql)
        users = []
        while 1:
            res = cursor.fetchone()
            if res is None:
                break
            users.append(res)
        if len(users) == 1:
            ip = request.META.get("REMOTE_ADDR")
            print(ip)
            c_time = time.ctime()
            token = generate_token(ip, users_names, c_time)
            users_token = token
            sha256_decode = check_password(users_pass, users[0][2])
            sha1_decode = check_password(users_pass, users[0][3])
            if sha256_decode == True and sha1_decode == True:

                dic = {'state': 200, 'message': "Success"}
                res = HttpResponse(json.dumps(dic, ensure_ascii=False))
                res.set_cookie('token',value=token)
                res.set_cookie('c_time',value=c_time)
                res.set_cookie('username',value=users_names)
                return res
            else:
                dic = {'state': 200, 'message': "Failed",}
                res = HttpResponse(json.dumps(dic, ensure_ascii=False))
                return res
        else:
            dic = {'state': 200, 'message': "Failed", }
            res = HttpResponse(json.dumps(dic, ensure_ascii=False))
            return res
# create token,ip+username+current time+static string
def generate_token(ip, users_names,c_time):
    r = users_names
    print(ip + c_time + r+'laodiggn')
    sha256_encrypt = make_password((ip + c_time + r+'laodiggn'), None, 'pbkdf2_sha256')
    return sha256_encrypt
# check token
def checkToken(request):
    token = request.COOKIES.get('token')
    c_time = request.COOKIES.get('c_time')
    users_names = request.COOKIES.get('username')
    ip = request.META.get("REMOTE_ADDR")
    tokencheck = check_password( ip+c_time+users_names+"laodiggn",token)
    if tokencheck == True:
        dic = {'state': 200, 'message': "Success"}
        return HttpResponse(json.dumps(dic, ensure_ascii=False))
    else:
        dic = {'state': 300, 'message': "Failed"}
        return HttpResponse(json.dumps(dic, ensure_ascii=False))


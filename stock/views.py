from django.shortcuts import render
import json
import time
import MySQLdb
from django.http import HttpResponse
# Create your views here.
conn = MySQLdb.connect('localhost', user="root", passwd="root", db="JXC")
# Select database
conn.select_db('JXC')
# get cursor
cursor = conn.cursor()

def stocklist(request):
    stock_name = request.POST.get("stock_name")
    print(stock_name)
    stocks = [];
    if stock_name==None:
        sql = "select * from stock"
        cursor.execute(sql)
        while 1:
            res = cursor.fetchone()
            if res is None:
                break
            stocks.append(res)
    else:
        sql = "select * from stock where stock_name=\""+stock_name+"\""
        print(sql)
        cursor.execute(sql)
        while 1:
            res = cursor.fetchone()
            if res is None:
                break
            stocks.append(res)
    print(stocks)
    dic = {'state': 200, 'message': "Success",'stocklist':stocks}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))

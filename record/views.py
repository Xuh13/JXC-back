from django.shortcuts import render
import json
import time
import MySQLdb
from django.http import HttpResponse

# Create your views here.
conn = MySQLdb.connect('localhost', user="root", passwd="", db="JXC", charset='utf8')
# Select database
conn.select_db('JXC')
# get cursor
cursor = conn.cursor()


def recordlist(request):
    records = []
    sql = "select record_id,price,total,type,stock_name,username from record natural join stock"
    cursor.execute(sql)
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        records.append({
            "record_id":res[0],
            "price":res[1],
            "total":res[2],
            "type":res[3],
            "stock_name":res[4],
            "username":res[5]
        })
    print(records)
    dic = {'state': 200, 'message': "Success", 'recordlist': records}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))


def stockHisRecord(request):
    requestData = json.loads(request.body)
    stock_id = requestData.get("stock_id")
    recordsIn = []
    recordsOut = []
    sqlIn = "select record_id,price,total,type,stock_name from record natural join stock where stock_id = %s and type =0"
    sqlOut = "select record_id,price,total,type,stock_name from record natural join stock where stock_id = %s and type =1"
    cursor.execute(sqlIn, stock_id)
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        recordsIn.append(res)
    cursor.execute(sqlOut, stock_id)
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        recordsOut.append(res)
    dic = {'state': 200, 'message': "Success", 'InList': recordsIn, 'OutList': recordsOut}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))

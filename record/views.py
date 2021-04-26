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
            "record_id": res[0],
            "price": res[1],
            "total": res[2],
            "type": res[3],
            "stock_name": res[4],
            "username": res[5]
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
        recordsIn.append({
            'record_id':str(res[0]),
            'price':str(res[1]),
            'total':str(res[2]),
            'type':str(res[3]),
            'stock_name':res[4]
        })
    cursor.execute(sqlOut, stock_id)
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        recordsOut.append({
            'record_id':str(res[0]),
            'price':str(res[1]),
            'total':str(res[2]),
            'type':str(res[3]),
            'stock_name':res[4]
        })
    dic = {'state': 200, 'message': "Success", 'InList': recordsIn, 'OutList': recordsOut}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))


def monthRecord(request):
    requestData = json.loads(request.body)
    recordsIn = []
    recordsOut = []
    sqlIn = "select s.stock_id,s.stock_name,year(bill_time),month(bill_time),sum(total) from record r join bill b on r.record_id=b.record_id join stock s on r.stock_id=s.stock_id where r.type=0 and s.stock_name=\""+requestData['stock_name']+"\" group by year(b.bill_time),month(b.bill_time)"
    sqlOut = "select s.stock_id,s.stock_name,year(bill_time),month(bill_time),sum(total) from record r join bill b on r.record_id=b.record_id join stock s on r.stock_id=s.stock_id where r.type=1 and s.stock_name=\""+requestData['stock_name']+"\" group by year(b.bill_time),month(b.bill_time)"
    cursor.execute(sqlIn)
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        recordsIn.append({
            'stock_id':str(res[0]),
            'stock_name':res[1],
            'date': str(res[2]) + '-' + str(res[3]),
            'num': str(res[4])
        })
    cursor.execute(sqlOut)
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        recordsOut.append({
            'stock_id':str(res[0]),
            'stock_name':res[1],
            'date': str(res[2]) + '-' + str(res[3]),
            'num': str(res[4])
        })
    dic = {'state': 200, 'message': "Success", 'InList': recordsIn, 'OutList': recordsOut}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))


def totalRecord(request):
    # requestData = json.loads(request.body)
    records = []
    sql = "select stock_id,stock_name,sum(total) from record natural join stock where type=1 group by stock_id"
    cursor.execute(sql)
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        records.append({
            'stock_id': str(res[0]),
            'stock_name': res[1],
            'total': str(res[2])
        })
    dic = {'state': 200, 'message': "Success", 'totalList': records}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))


def stockPrice(request):
    requestData = json.loads(request.body)
    recordsIn = []
    recordsOut = []
    sqlIn = "select s.stock_id,s.stock_name,year(bill_time),month(bill_time),avg(price) from record r join bill b on r.record_id=b.record_id join stock s on r.stock_id=s.stock_id where r.type=0 and s.stock_name=\""+requestData['stock_name']+"\" group by year(b.bill_time),month(b.bill_time)"
    sqlOut = "select s.stock_id,s.stock_name,year(bill_time),month(bill_time),avg(price) from record r join bill b on r.record_id=b.record_id join stock s on r.stock_id=s.stock_id where r.type=1 and s.stock_name=\""+requestData['stock_name']+"\" group by year(b.bill_time),month(b.bill_time)"
    cursor.execute(sqlIn)
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        recordsIn.append({
            'stock_id':str(res[0]),
            'stock_name':res[1],
            'date': str(res[2]) + '-' + str(res[3]),
            'price': str(res[4])
        })
    cursor.execute(sqlOut)
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        recordsOut.append({
            'stock_id':str(res[0]),
            'stock_name':res[1],
            'date': str(res[2]) + '-' + str(res[3]),
            'price': str(res[4])
        })
    dic = {'state': 200, 'message': "Success", 'InList': recordsIn, 'OutList': recordsOut}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))
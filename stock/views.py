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


def stocklist(request):
    requestData = json.loads(request.body)
    stock_name = requestData.get("stock_name")
    stocks = [];
    if stock_name == "":
        sql = "select * from stock"
        cursor.execute(sql)
        while 1:
            res = cursor.fetchone()
            if res is None:
                break
            print(res)
            stocks.append({
                "stock_id":res[0],
                "stock_name":res[1],
                "stock_nums":res[2],
                "highest_price":res[3],
                "lowest_price":res[4],
                "unit":res[5],
                "warningval":res[6]
            })
    else:
        sql = "select * from stock where stock_name=\"" + stock_name + "\""
        print(sql)
        cursor.execute(sql)
        while 1:
            res = cursor.fetchone()
            if res is None:
                break
            print(res)
            stocks.append({
                "stock_id":res[0],
                "stock_name":res[1],
                "stock_nums":res[2],
                "highest_price":res[3],
                "lowest_price":res[4],
                "unit":res[5],
                "warningval":res[6]
            })
    print(stocks)
    dic = {'state': 200, 'message': "Success", 'stocklist': stocks}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))


def getunit(request):
    requestData = json.loads(request.body)
    stock_name = requestData.get("stock_name")
    sql = "select * from stock where stock_name=\"" + stock_name + "\""
    cursor.execute(sql)
    stocks = []
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        stocks.append(res)
    # encoding:utf-8
    unit = u""
    print(stocks)
    if len(stocks) == 1:
        unit = stocks[0][5]
    dic = {'state': 200, 'message': "Success", 'unit': unit}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))


def warehousing(request):
    requestData = json.loads(request.body)
    stock_name = requestData.get("stock_name")
    stock_nums = int(requestData.get("stock_nums"))
    price = float(requestData.get("price"))
    unit = requestData.get("unit")
    username = requestData.get("username")

    # stock
    sqlstock = "select * from stock where stock_name=\"" + stock_name + "\""
    cursor.execute(sqlstock)
    stocks = []
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        stocks.append(res)
    print(stocks)
    if len(stocks) == 0:
        sql1 = "insert into stock values(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql1, (0, stock_name, stock_nums, price, price, unit, -1))
        conn.commit()
    else:
        print(stocks[0][2] + stock_nums)
        sql1 = "update stock set stock_nums=%s where stock_name=%s"
        cursor.execute(sql1, (stocks[0][2] + stock_nums, stock_name))
        conn.commit()

    # record
    sqlrecord = "select * from stock where stock_name=\"" + stock_name + "\""
    cursor.execute(sqlrecord)
    stock = []
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        stock.append(res)
    sql2 = "insert into record values(%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql2, (0, int(stock[0][0]), price, stock_nums, 0, stock_nums, username))
    conn.commit()
    print(123)
    # bill
    sqlbill = "select * from record where stock_id=" + str(stock[0][0])
    cursor.execute(sqlbill)
    records = []
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        records.append(res)
    print(records)
    sql3 = "insert into bill values(%s,%s,%s,now(),%s)"
    cursor.execute(sql3, (0, records[len(records) - 1][0], price * stock_nums * -1, 0))
    conn.commit()
    dic = {'state': 200, 'message': "Success"}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))


def setWarning(request):
    requestData = json.loads(request.body)
    stock_id = requestData.get("stock_id")
    warningval = requestData.get("warningval")
    sql1 = "update stock set warningval=%s where stock_id=%s"
    cursor.execute(sql1, (warningval, stock_id))
    conn.commit()
    dic = {'state': 200, 'message': "Success"}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))


def outofstock(request):
    requestData = json.loads(request.body)
    stock_name = requestData.get("stock_name")
    stock_nums = int(requestData.get("stock_nums"))
    price = float(requestData.get("price"))
    username = requestData.get("username")
    warning = False
    sqlstock = "select * from stock where stock_name=\"" + stock_name+"\""
    print(sqlstock)
    cursor.execute(sqlstock)
    stocks = []
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        stocks.append(res)
    stock_id = str(stocks[0][0])
    if stocks[0][2] < stock_nums:
        dic = {'state': 300, 'message': "Not enough"}
        return HttpResponse(json.dumps(dic, ensure_ascii=False))
    else:
        sql = "update stock set stock_nums=%s where stock_id=%s"
        cursor.execute(sql, (int(stocks[0][2]) - stock_nums, stocks[0][0]))
        if int(stocks[0][6])!=-1 and int(stocks[0][2]) - stock_nums < int(stocks[0][6]):
            warning = True
        conn.commit()
    sqlrecord = "select * from record where stock_id=" + stock_id + " and type = 0"
    cursor.execute(sqlrecord)
    records = []
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        records.append(res)
    now = stock_nums
    i = 0
    profit = 0
    sql1 = "update record set surplus=%s where record_id=%s"
    for item in records:
        if item[5] >= now:
            profit += (price - float(item[2])) * now
            cursor.execute(sql1, (int(item[5]) - now, item[0]))
            now = 0;
            break
        else:
            profit += (price - float(item[2])) * item[5]
            now -= item[5]
            cursor.execute(sql1, (0, item[0]))
        conn.commit()
        i += 1
    sql2 = "insert into record values(%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql2, (0, stock_id, price, stock_nums, 1, 0, username))
    conn.commit()
    sqlbill = "select * from record where stock_id=" + str(stock_id)
    cursor.execute(sqlbill)
    record = []
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        record.append(res)
    sql3 = "insert into bill values(%s,%s,%s,now(),%s)"
    cursor.execute(sql3, (0, record[len(record) - 1][0], price * stock_nums, profit))
    conn.commit()
    dic = {'state': 200, 'message': "Success"}
    if warning:
        dic['warning'] = 1
    return HttpResponse(json.dumps(dic, ensure_ascii=False))
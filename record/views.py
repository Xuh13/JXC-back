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

def recordlist(request):
    records = []
    sql = "select record_id,price,total,type,stock_name from record natural join stock"
    cursor.execute(sql)
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        records.append(res)
    print(records)
    dic = {'state': 200, 'message': "Success",'recordlist':records}
    return HttpResponse(json.dumps(dic, ensure_ascii=False))

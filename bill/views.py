from django.shortcuts import render
import datetime,json
import time
import MySQLdb
from django.http import HttpResponse
# Create your views here.
conn = MySQLdb.connect('localhost', user="root", passwd="root", db="JXC")
# Select database
conn.select_db('JXC')
# get cursor
cursor = conn.cursor()

# resolve datetime to json
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)

def billlist(request):
    bills = []
    sql = "select * from bill b join record r on b.record_id=r.record_id join stock s on r.stock_id=r.stock_id"
    cursor.execute(sql)
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        bills.append(res)
    print(bills)
    dic = {'state': 200, 'message': "Success",'billlist':bills}
    print(dic)
    return HttpResponse(json.dumps(dic, cls=DateTimeEncoder))

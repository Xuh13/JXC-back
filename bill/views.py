from django.shortcuts import render
import datetime,json
import time
import MySQLdb
from django.http import HttpResponse
# Create your views here.
conn = MySQLdb.connect('localhost', user="root", passwd="", db="JXC", charset='utf8')
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
    sql = "select bill_id,total_amount,bill_time,profit,price,total,username,stock_name,unit from bill b join record r on b.record_id=r.record_id join stock s on r.stock_id=r.stock_id"
    cursor.execute(sql)
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        bills.append({
            "bill_id":res[0],
            "total_amount":res[1],
            "bill_time":res[2],
            "profit":res[3],
            "price":res[4],
            "total":res[5],
            "username":res[6],
            "stock_name":res[7],
            "unit":res[8]
        })
    print(bills)
    dic = {'state': 200, 'message': "Success",'billlist':bills}
    print(dic)
    return HttpResponse(json.dumps(dic, cls=DateTimeEncoder))

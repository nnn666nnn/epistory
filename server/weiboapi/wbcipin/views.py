from django.shortcuts import render

# Create your views here.
import pymysql

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
@api_view(['GET','POST'])
def wbcipinReturn(request):
    if request.method == 'GET':
        # 构造查询语句
        sql = ""
        # 构造查询个数
        num = "200"
        if request.query_params.get("num") is not None:
            num = request.query_params.get("num")
        # 确定是否地区
        if request.query_params.get("region") is not None:
            region = request.query_params.get("region")
            # 确定时间尺度
            if request.query_params.get("time") is not None:
                time = request.query_params.get("time")
                sql = "SELECT `word`, `weight` FROM `cp_weibo_region` WHERE `time` = '"+time+"' AND `region` LIKE '"+region+"' ORDER BY `weight` DESC"
            elif request.query_params.get("week") is not None:
                week = request.query_params.get("week")
                sql = "SELECT `word`, `weight` FROM `cp_weibo_region` WHERE `time` = '2010-01-"+week+"' AND `region` LIKE '"+region+"' ORDER BY `weight` DESC"
            elif request.query_params.get("month") is not None:
                month = request.query_params.get("month")
                sql = "SELECT `word`, `weight` FROM `cp_weibo_region` WHERE `time` = '2000-01-"+month+"' AND `region` LIKE '"+region+"' ORDER BY `weight` DESC"
            else:
                sql = "SELECT `word`, `weight` FROM `cp_weibo_region` WHERE `time` = '1990-01-01' AND `region` LIKE '"+region+"' ORDER BY `weight` DESC"
        else:
            if request.query_params.get("time") is not None:
                time = request.query_params.get("time")
                sql = "SELECT `word`, `weight` FROM `cp_weibo_time` WHERE `time` = '"+time+"' ORDER BY `weight` DESC"
            elif request.query_params.get("week") is not None:
                week = request.query_params.get("week")
                sql = "SELECT `word`, `weight` FROM `cp_weibo_time` WHERE `time` = '2010-01-"+week+"'  ORDER BY `weight` DESC"
            elif request.query_params.get("month") is not None:
                month = request.query_params.get("month")
                sql = "SELECT `word`, `weight` FROM `cp_weibo_time` WHERE `time` = '2000-01-"+month+"' ORDER BY `weight` DESC"
            else:
                return Response({"error":"不存在有效参数!"},status=400)
        sql += " LIMIT " + num
        # 查询
        # 获取数据库密码
        f = open('/home/pi/sqlpsd','r')
        psd = f.read()
        f.close()
        psd = psd[:-1]
        # 连接数据库 注意关闭连接
        db = pymysql.connect(host="localhost",
                             port=3306,
                             user="PiSql",
                             passwd=psd,
                             db="rdWeiBo")
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        v = cursor.fetchall()
        cursor.close()
        db.close()
        return Response(v) 
    return Response({"error":"请使用GET请求!"},status=400)

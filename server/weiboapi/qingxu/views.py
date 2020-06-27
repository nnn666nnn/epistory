# -*- coding:utf-8 -*-
from django.shortcuts import render

# Create your views here.a

import pymysql

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
@api_view(['GET','POST'])
def qingxuReturn(request):
    if request.method == 'GET':
        # 构造查询语句
        sql = ""
        # 判断是都为某地区所有数据
        if request.query_params.get("timecode") is not None:
            timecode = request.query_params.get("timecode")
            if request.query_params.get("region") is not None:
                region = request.query_params.get("region")
                if timecode == "t":
                    sql = "SELECT `sentiment`,`positive_prob`,`time` FROM `qx_weibo_region` WHERE `time` > '2019-12-26' AND `region` LIKE '"+region+"' ORDER BY `time`"
                elif timecode == "w":
                    sql = "SELECT `sentiment`,`positive_prob` FROM `qx_weibo_region` WHERE `time` BETWEEN '2010-1-1' AND '2010-2-1' AND `region` LIKE '"+region+"' ORDER BY `time`"
                elif timecode == "m":
                    sql = "SELECT `sentiment`,`positive_prob` FROM `qx_weibo_region` WHERE `time` < '2000-2-1' AND `region` LIKE '"+region+"' ORDER BY `time`"
                else :
                    return Response({"error":"timecode参数错误!"},status=400)
            else:
                return Response({"error":"没有有效参数!"},status=400)
        else:
            # 判断是否为具体区域
            if request.query_params.get("region") is not None:
                region = request.query_params.get("region")
                if request.query_params.get("time") is not None:
                    time = request.query_params.get("time")
                    sql = "SELECT `sentiment`,`positive_prob` FROM `qx_weibo_region` WHERE `time` = '"+time+"' AND `region` LIKE '"+region+"'"
                elif request.query_params.get("week") is not None:
                    week = request.query_params.get("week")
                    sql = "SELECT `sentiment`,`positive_prob` FROM `qx_weibo_region` WHERE `time` = '2010-01-"+week+"' AND `region` LIKE '"+region+"'"
                elif request.query_params.get("month") is not None:
                    month = request.query_params.get("month")
                    sql = "SELECT `sentiment`,`positive_prob` FROM `qx_weibo_region` WHERE `time` = '2000-01-"+month+"' AND `region` LIKE '"+region+"'"
                else:
                    return Response({"error":"不存在有效参数!"},status=400)
            else:
                if request.query_params.get("time") is not None:
                    time = request.query_params.get("time")
                    sql = "SELECT `sentiment`,`positive_prob`,`region` FROM `qx_weibo_region` WHERE `time` = '"+time+"'"
                elif request.query_params.get("week") is not None:
                    week = request.query_params.get("week")
                    sql = "SELECT `sentiment`,`positive_prob`,`region` FROM `qx_weibo_region` WHERE `time` = '2010-01-"+week+"'"
                elif request.query_params.get("month") is not None:
                    month = request.query_params.get("month")
                    sql = "SELECT `sentiment`,`positive_prob`,`region` FROM `qx_weibo_region` WHERE `time` = '2000-01-"+month+"'"
                else:
                    return Response({"error":"不存在有效参数!"},status=400)
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

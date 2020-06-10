# -*- coding:utf-8 -*-
from django.shortcuts import render

# Create your views here.

import pymysql

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from urllib.parse import unquote
@api_view(['GET','POST'])
def resouReturn(request):
    if request.method == 'GET':
        # 构造查询语句
        # 确定数据排列依据及顺序
        sort = ""
        if request.query_params.get("sortcode") is not None:
            sortcode = request.query_params.get("sortcode") 
            if "k" in sortcode :
                sort += "`keyword` "
            elif "r" in sortcode:
                sort += "`rank` "
            elif "s" in sortcode:
                sort += "`searchNum` "
            elif "t" in sortcode:
                sort += "`time` "
            else:
                sort += "`searchNum` "
            if "d" in sortcode:
                sort += "DESC "
            elif "a" in sortcode:
                sort += "ASC "
            else:
                sort += "DESC "
        else:
            sort = "`searchNum` DESC "
        # 确定查询数据
        data = ""
        
        if request.query_params.get("datacode") is not None:
            code = request.query_params.get("datacode")
            if "L" in code or "l" in code:
                data += "link,"
            if "K" in code or "k" in code:
                data += "keyword,"
            if "R" in code or "r" in code:
                data += "rank,"
            if "S" in code or "s" in code:
                data += "searchNum,"
            if "T" in code or "t" in code:
                data += "time,"
        else:
            data = "link, keyword, rank, searchNum,"
        data = data[:-1]
        # 确定查询数据个数
        num = "999"
        if request.query_params.get("num") is not None:
            num = request.query_params.get("num")
        # 确定查询方式
        if request.query_params.get("begintime") is not None \
	      and request.query_params.get("endtime") is not None:
            begintime = request.query_params.get("begintime")
            endtime = request.query_params.get("endtime")
            # 是否指定关键词
            if request.query_params.get("keyword") is not None:
                keyword = request.query_params.get("keyword")
                sql = "SELECT DISTINCT " + data + " FROM `rd_resou` WHERE `keyword` LIKE '%" + keyword + "%' AND `time` BETWEEN '" \
                        + begintime + "' AND '" + endtime + "' ORDER BY "+sort+"LIMIT " + num
            else:
                sql = "SELECT DISTINCT "+data+" FROM `rd_resou` WHERE `time` BETWEEN '" \
                +begintime+"' AND '"+endtime+"' ORDER BY "+sort+"LIMIT " + num
        else:
            if request.query_params.get("time") is not None:
                time = request.query_params.get("time")
                # sql = "SELECT distinct link,keyword,rank,searchNum FROM `rd_resou` WHERE `time` = '"+i+"'"
                # 是否指定关键词
                if request.query_params.get("keyword") is not None:
                    keyword = request.query_params.get("keyword")
                    sql = "SELECT DISTINCT "+data+" FROM `rd_resou` WHERE `keyword` LIKE '%"+keyword+"%' AND `time` = '" \
                            + time +"' ORDER BY "+sort+"LIMIT " + num
                else:
                    sql = "SELECT DISTINCT "+data+" FROM `rd_resou` WHERE `time` = '" \
                        + time+"' ORDER BY "+sort+"LIMIT " + num
            else:
                if request.query_params.get("keyword") is not None:
                    keyword = request.query_params.get("keyword")
                    sql = "SELECT DISTINCT "+data+" FROM `rd_resou` WHERE `keyword` LIKE '%" \
                            +keyword+"%' ORDER BY "+sort+"LIMIT "+num
                else:
                    return Response({"error":"不存在有效参数!"},status=400)
        # 读取数据库密码
        psd = ""
        f =  open('/home/pi/sqlpsd','r')
        psd = f.read()
        psd = psd[:-1]
        f.close()
        # 连接数据库 注意关闭连接
        db = pymysql.connect(host="localhost",
                             port=3306,
                             user="PiSql",
                             passwd=psd,
                             db="WeiBo",
                             charset='utf8',
                             use_unicode=True)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)    
        v = cursor.fetchall() 
       	cursor.close()
        db.close()
        return Response(v)
    return Response({"error":"请使用GET请求!"},status=400)

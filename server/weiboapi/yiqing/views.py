from django.shortcuts import render

# Create your views here.

import pymysql

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
@api_view(['GET','POST'])
def yiqingReturn(request):
    if request.method == 'GET':
        # 构造查询语句
        # 确定获取数据类型
        data = ""
        if request.query_params.get("datacode") is not None:
            datacode = request.query_params.get("datacode")
            if "t" in datacode:
                data += "rd_yiqing.time,"
            if "a" in datacode:
                data += "rd_yiqing.areacode,"
            if "n" in datacode:
                data += "area_code.name,"
            if "c" in datacode:
                data += "rd_yiqing.confirmed,"
            if "s" in datacode:
                data += "rd_yiqing.suspected,"
            if "h" in datacode:
                data += "rd_yiqing.cured,"
            if "d" in datacode:
                data += "rd_yiqing.dead,"
        else:
            data = "rd_yiqing.time,area_code.name,rd_yiqing.confirmed,"
        data = data[:-1]
        # 确定尺度
        scale = ""
        if request.query_params.get("scalecode") is not None:
            scalecode = request.query_params.get("scalecode")
            if "z" in scalecode:
                scale += "rd_yiqing.areacode = 0 OR "
            if "s" in scalecode:
                scale += "rd_yiqing.areacode LIKE '%0000' OR"
            if "h" in scalecode:
                scale += "rd_yiqing.areacode LIKE '42%' AND rd_yiqing.areacode NOT LIKE '420000' OR"
        else:
            scale = "rd_yiqing.areacode = 0 OR"
        scale = scale[:-3]
        # 判断多日期单日期
        if request.query_params.get("time") is not None:
            time = request.query_params.get("time")
            # 判断是否具体地区
            if request.query_params.get("areacode") is None and request.query_params.get("areaname") is None:
                sql = "SELECT "+data+" FROM rd_yiqing INNER JOIN area_code ON rd_yiqing.areacode=area_code.code WHERE" \
                    + " (" +scale+ ") AND rd_yiqing.time='"+time+"'"
            else:
                if request.query_params.get("areacode") is not None:
                    areacode = request.query_params.get("areacode")
                    sql = "SELECT "+data+" FROM rd_yiqing INNER JOIN area_code ON rd_yiqing.areacode=area_code.code WHERE" \
                        + " rd_yiqing.areacode="+areacode+" AND rd_yiqing.time='"+time+"'"
                else:
                    areaname = request.query_params.get("areaname")
                    sql = "SELECT "+data+" FROM rd_yiqing INNER JOIN area_code ON rd_yiqing.areacode=area_code.code WHERE" \
                        + " area_code.name LIKE'%"+areaname+"%' AND rd_yiqing.time='"+time+"'"
        else:
            if request.query_params.get("begintime") is not None \
                and request.query_params.get("endtime") is not None:
                begintime = request.query_params.get("begintime")
                endtime = request.query_params.get("endtime")
                # 判断是否具体地区
                if request.query_params.get("areacode") is None and request.query_params.get("areaname") is None:
                    sql = "SELECT "+data+" FROM rd_yiqing INNER JOIN area_code ON rd_yiqing.areacode=area_code.code WHERE" \
                    + " (" +scale+ ") AND rd_yiqing.time BETWEEN '"+begintime+"' AND '"+endtime+"'"
                else:
                    if request.query_params.get("areacode") is not None:
                        areacode = request.query_params.get("areacode")
                        sql = "SELECT "+data+" FROM rd_yiqing INNER JOIN area_code ON rd_yiqing.areacode=area_code.code WHERE" \
                        + " rd_yiqing.areacode="+areacode+" AND rd_yiqing.time BETWEEN '"+begintime+"' AND '"+endtime+"'"
                    else:
                        areaname = request.query_params.get("areaname")
                        sql = "SELECT "+data+" FROM rd_yiqing INNER JOIN area_code ON rd_yiqing.areacode=area_code.code WHERE" \
                            + " area_code.name LIKE'%"+areaname+"%' AND rd_yiqing.time BETWEEN '"+begintime+"' AND '"+endtime+"'"
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
                             db="WeiBo")
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        v = cursor.fetchall()
        cursor.close()
        db.close()
        return Response(v)
    return Response({"error":"请使用GET请求!"},status=400)


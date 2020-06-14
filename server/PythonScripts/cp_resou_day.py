# -*- coding:utf-8 -*-
import pymysql
from datetime import date
# 连接数据库
# 读取数据库密码
f = open('/home/pi/sqlpsd','r')
psd = f.read()
psd = psd[:-1]
f.close()
# 开始连接
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="PiSql",
                     passwd=psd,
                     db="WeiBo",
                     charset='utf8',
                     use_unicode=True)
cur = db.cursor(cursor=pymysql.cursors.DictCursor)
# 构造时间列表
cur.execute("SELECT DISTINCT `time` FROM `fc_resou` ORDER BY `time` ASC")
times = []
for each in cur.fetchall():
    times.append(each['time'].isoformat())
    print(times[-1])
    print("时间列表完成")
# 按天读取数据,并统计词频
for time in times:
    print("开始统计"+time+"词频")
    sqltime = "SELECT `word`, `weight`, `searchNum` FROM `fc_resou` WHERE `time` = '"+time+"'"
    cur.execute(sqltime)
    datas = cur.fetchall()
    # 统计词频
    results = {}
    for data in datas:
        if data['word'] in results.keys():
            results[data['word']] = results[data['word']] + data['weight'] * data['searchNum']
        else:
            results[data['word']] = data['weight'] * data['searchNum']
    # 储层结果至数据库
    # 构造插入语句
    sqlcp = "INSERT INTO `cp_resou` (`word`, `weight`, `time`) VALUES (%s,%s,%s)"
    # 插入数据
    for result in results.keys():
        cur.execute(sqlcp,(result,results[result],time))
        db.commit()
    print(time+"词频插入完成")
# 关闭数据库连接
cur.close()
db.close()

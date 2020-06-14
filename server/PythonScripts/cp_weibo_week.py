# -*- coding:utf-8 -*-
import pymysql
from datetime import date
from datetime import timedelta
# 构造每周始终时间
beginweek = [date(2019,12,27),date(2020,1,2)]
weeks = []
for i in range(23):
    weeks.append([beginweek[0]+timedelta(weeks=i),beginweek[1]+timedelta(weeks=i)])
print(weeks)
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
                     db="rdWeiBo",
                     charset='utf8',
                     use_unicode=True)
cur = db.cursor(cursor=pymysql.cursors.DictCursor)
# 按周读取数据并统计词频
num = -1 # 计数
for week in weeks:
    num += 1
    print("开始统计"+week[0].isoformat()+"~"+week[1].isoformat()+"词频")
    # 读取数据
    sql = "SELECT `word`, `weight`, `acrNum` FROM `fc_weibo` WHERE `time` BETWEEN '"+week[0].isoformat()+"' AND '"+week[1].isoformat()+"'"
    cur.execute(sql)
    datas = cur.fetchall()
    # 统计词频
    results = {}
    for data in datas:
        if data['word'] in results.keys():
            results[data['word']] = results[data['word']] + data['weight'] * data['acrNum']
        else:
            results[data['word']] = data['weight'] * data['acrNum']
    # 储存结果至数据库
    sqlcp = "INSERT INTO `cp_weibo_time` (`word`, `weight`, `time`) VALUES (%s, %s, %s)"
    # 插入数据
    for result in results.keys():
        cur.execute(sqlcp,(result,results[result],(date(2010,1,1)+timedelta(days=num)).isoformat()))
        db.commit()
# 关闭数据库连接
cur.close()
db.close()

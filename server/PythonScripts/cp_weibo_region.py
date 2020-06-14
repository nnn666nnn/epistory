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
                     db="rdWeiBo",
                     charset='utf8',
                     use_unicode=True)
cur = db.cursor(cursor=pymysql.cursors.DictCursor)
# 构造地区列表
cur.execute("SELECT DISTINCT `region` FROM `fc_weibo` ORDER BY `region` ASC")
regions = []
for each in cur.fetchall():
    regions.append(each['region'])
    print(regions[-1])
print('地区列表完成')
# 按地区读取数据,并统计词频
for region in regions:
    print("开始统计 --"+region+"-- 词频")
    sqltime = "SELECT `word`, `weight`, `acrNum` FROM `fc_weibo` WHERE `region` LIKE '" + region + "'"
    cur.execute(sqltime)
    datas = cur.fetchall()
    # 统计词频
    results = {}
    for data in datas:
        if data['word'] in results.keys():
            results[data['word']] = results[data['word']] + data['weight'] * data['acrNum']
        else:
            results[data['word']] = data['weight'] * data['acrNum']
    # 储层结果至数据库
    # 构造插入语句
    sqlcp = "INSERT INTO `cp_weibo_region` (`word`, `weight`, `time`, `region`) VALUES (%s, %s, %s, %s)"
    # 插入数据
    for result in results.keys():
        cur.execute(sqlcp,(result,results[result],'1990-1-1',region))
        db.commit()
# 关闭数据库连接
cur.close()
db.close()

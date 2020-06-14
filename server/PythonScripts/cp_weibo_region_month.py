# -*- coding:utf-8 -*-
import pymysql
from datetime import date
from datetime import timedelta
# 构造每月始终时间
beginmonth = [date(2019,12,27),date(2019,12,27)+timedelta(days=29)]
months = []
for i in range(6):
    months.append([beginmonth[0]+timedelta(days=30*i),beginmonth[1]+timedelta(days=30*i)])
print(months)
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

# 按读取数据并统计词频
num = -1 # 计数
for month in months:
    num +=1
    for region in regions:
        print("开始统计 --"+month[0].isoformat()+"~"+month[1].isoformat()+"_"+region+"-- 词频")
        # 读取数据
        sql = "SELECT `word`, `weight`, `acrNum` FROM `fc_weibo` WHERE `time` BETWEEN '"+month[0].isoformat()+"' AND '"+month[1].isoformat()+"'"+" AND `region` LIKE '"+region+"'"
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
        sqlcp = "INSERT INTO `cp_weibo_region` (`word`, `weight`, `time`, `region`) VALUES (%s,%s,%s,%s)"
        # 插入数据
        for result in results.keys():
            cur.execute(sqlcp,(result,results[result],(date(2000,1,1)+timedelta(days=num)).isoformat(),region))
            db.commit()
# 关闭数据库连接
cur.close()
db.close()

# -*- coding:utf-8 -*-
import pymysql
from datetime import date
from datetime import timedelta
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
# 构造每周时间
beginweek = [date(2019,12,27),date(2020,1,2)]
weeks = []
for i in range(23):
    weeks.append([beginweek[0]+timedelta(weeks=i),beginweek[1]+timedelta(weeks=i)])
print(weeks)
# 构造地区列表
regions = []
cur.execute("SELECT DISTINCT `region` FROM `qx_weibo`")
for each in cur.fetchall():
    regions.append(each['region'])
    print(regions[-1])
# 安周和地区读取数据,并综合情绪指数
# 计数
weeknum = -1
for week in weeks:
    weeknum += 1
    for region in regions:
        print("开始统计 --"+week[0].isoformat()+"~"+week[1].isoformat()+"_"+region+"-- 情绪")
        sqls = "SELECT `positive_prob` FROM `qx_weibo` WHERE `confidence` > 0.6 AND `time` BETWEEN '"+week[0].isoformat()+"' AND '"+week[1].isoformat()+"' AND `region` LIKE '"+region+"'"
        cur.execute(sqls)
        datas = cur.fetchall()
        # 计数
        num = 0
        sub = 0
        for data in datas:
            sub += data['positive_prob']
            num += 1
        if num == 0:
            re = 0.5
            print(str(weeknum) +"周"+region+"无数据")
        else:
            re = sub / num
        if re <= 0.45:
            se = 0
        elif re < 0.55:
            se = 1
        else:
            se = 2
        sqli = "INSERT INTO `qx_weibo_region` (`sentiment`, `positive_prob`, `region`, `time`) VALUES (%s, %s, %s, %s)"
        # 插入数据
        cur.execute(sqli,(se,re,region,(date(2010,1,1)+timedelta(days=weeknum)).isoformat()))
        db.commit()
# 关闭数据库
cur.close()
db.close()


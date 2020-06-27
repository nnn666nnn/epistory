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
# 构造时间列表
times = []
cur.execute("SELECT DISTINCT `time` FROM `qx_weibo` ORDER BY `time` ASC")
for each in cur.fetchall():
    times.append(each['time'].isoformat())
    print(times[-1])
# 构造地区列表
regions = []
cur.execute("SELECT DISTINCT `region` FROM `qx_weibo`")
for each in cur.fetchall():
    regions.append(each['region'])
    print(regions[-1])
# 按天和地区读取数据,并综合情绪指数
for time in times:
    for region in regions:
        print("统计 --"+time+"_"+region+"-- 情绪")
        sqls = "SELECT `positive_prob` FROM `qx_weibo` WHERE `confidence` > 0.6 AND `time` = '"+time+"' AND `region` LIKE '"+region+"'"
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
            print(time+"_"+region+ "无数据")
        else:
            re = sub / num
        if re <=0.45:
            se = 0
        elif re <0.55:
            se = 1
        else:
            se = 2
        sqli = "INSERT INTO `qx_weibo_region` (`sentiment`, `positive_prob`, `region`, `time`) VALUES (%s, %s, %s, %s)"
        # 插入数据
        cur.execute(sqli,(se,re,region,time))
        db.commit()
# 关闭数据库
cur.close()
db.close()

# -*- coding:utf-8 -*-
import pymysql
import jieba.analyse
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
# 读取数据
cur.execute("SELECT `region`, `text`, `created_at`, `attitudes_count`, `comments_count`, `reposts_count` FROM `weibo` ORDER BY `weibo`.`created_at` ASC")
# 构造插入sql
sql = "INSERT INTO `fc_weibo` (`word`, `weight`, `time`, `acrNum`, `region`) VALUES (%s, %s, %s, %s, %s)"
# 开始分词
datas = cur.fetchall()
for data in datas:
    print(data['created_at'])
    result = jieba.analyse.extract_tags(data['text'],topK=10,withWeight=True)
    for each in result:
        cur.execute(sql,(each[0],each[1],data['created_at'],data['attitudes_count']+data['comments_count']*2+data['reposts_count']*3,data['region']))
        db.commit()
cur.close()
db.close()

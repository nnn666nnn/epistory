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
                     db="WeiBo",
                     charset='utf8',
                     use_unicode=True)
cur = db.cursor(cursor=pymysql.cursors.DictCursor)
# 读取数据
cur.execute("SELECT `keyword`, `time`, `searchNum` FROM `rd_resou` ORDER BY `time` ASC")
# 构造插入sql
sql = "INSERT INTO `fc_resou` (`word`, `weight`, `time`, `searchNum`) VALUES (%s,%s,%s,%s)"
# 开始分词
datas = cur.fetchall()
for data in datas:
    print(data['time'])
    result = jieba.analyse.extract_tags(data['keyword'],topK=None,withWeight=True)
    for each in result:
        cur.execute(sql,(each[0],each[1],data['time'],data['searchNum']))
        db.commit()
cur.close()
db.close()

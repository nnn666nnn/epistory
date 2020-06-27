import requests
import json
import pymysql
from datetime import date
import time
# 读取token
f = open('/home/pi/baidutoken','r')
token = f.read()
token = token[:-1]
f.close()
# 构造请求url
url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=" + token
headers = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With':'XMLHttpRequest',
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                        'Content-Type':'application/json',
                            'Accept-Encoding':'gzip, deflate',
                                'Accept-Language':'zh-CN,zh;q=0.8',
                                    'Cache-Control':'no-cache',
                                    'Connection': 'close',
                                      }
#data = '{"text":"苹果是一个优秀的公司!"}'
#data = data.encode('gbk')
#res = requests.post(url=url,data=data)
#j = json.loads(res.text)
#print(j['items'][0]['sentiment'])

# 读取数据库密码
f1 = open('/home/pi/sqlpsd','r')
psd = f1.read()
psd = psd[:-1]
f1.close()
# 连接数据库
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="PiSql",
                     passwd=psd,
                     db="rdWeiBo",
                     charset='utf8',
                     use_unicode=True)
cur = db.cursor(cursor=pymysql.cursors.DictCursor)
# 读取数据
cur.execute("SELECT `region`, `bid`, `text`, `created_at` FROM `weibo` WHERE `created_at` = '2020-4-23' ORDER BY `created_at` ASC")
# 构造插入sql
sql = "INSERT IGNORE INTO `qx_weibo` (`bid`, `sentiment`, `confidence`, `positive_prob`, `negative_prob`, `time`, `region`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
# 情感分析
datas = cur.fetchall()
for index,one in enumerate(datas):
    # 构造body
    body = '{"text":"'+one['text']+'"}'
    # POST请求
    res = requests.post(url=url,data=body.encode('gbk','ignore'),headers=headers)
    # 结果转为json格式
    j = json.loads(res.text)
    if "error_code" in j.keys():
        if j['error_code'] != 18:
            continue
    while "items" not in j.keys():
        res.close()
        time.sleep(2)
        res = requests.post(url=url,data=body.encode('gbk','ignore'),headers=headers)
        j = json.loads(res.text)
        print(j)
    # 存入数据库
    cur.execute(sql,(one['bid'],
                j["items"][0]['sentiment'],
                j["items"][0]['confidence'],
                j["items"][0]['positive_prob'],
                j["items"][0]['negative_prob'],
                one['created_at'],
                one['region']
                ))
    db.commit()
    print(str(index)+"/"+str(len(datas))+" -- 完成 --"+one['created_at'].isoformat()+"__"+body+"-- 情感分析")
    res.close()
    time.sleep(0.5)
cur.close()
db.close()


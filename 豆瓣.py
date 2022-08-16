import requests
import re
import csv
import pymysql
import time
def main():
    #爬取的网页
    url = 'https://movie.douban.com/top250?start='
    haveurl(url)

def haveurl(url):
    #创建保存数据的列表
    chinese_title_list = []
    english_title_list = []
    score_list = []
    people_list = []
    overview_list = []
    Movie_url_list = []
    for i in range(1,11):
        #从第几条开始
        num = i *25
        newurl = url + str(num)
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
            "cookie":"buvid3=1EB8D59F-3A08-4D98-8A8B-A0CD23512368190950infoc; rpdid=|(JY)k)klY~Y0J'ul~uuu~)ml; LIVE_BUVID=AUTO5415711177935363; fingerprint3=a79aa6162605e6a2e0d03b21636b516e; fingerprint_s=18da7071ee7757206838a26efa570a6f; _uuid=CA5CBF59-A525-98C1-E11F-4B84AB22A74D65467infoc; LNG=zh-CN; DedeUserID=35141053; DedeUserID__ckMd5=98ef095b6cadbe19; video_page_version=v_old_home; b_ut=5; i-wanna-go-back=2; nostalgia_conf=2; hit-dyn-v2=1; sid=au8giw47; buvid_fp_plain=undefined; CURRENT_BLACKGAP=0; blackside_state=0; SESSDATA=0094c563%2C1668595598%2Cd4707*51; bili_jct=f1391df8add5ff2c8feb973dbe17c075; go_old_video=1; CURRENT_FNVAL=4048; CURRENT_QUALITY=80; fingerprint=3e331eb13bf244d9539b268283bf29d6; buvid_fp=3e331eb13bf244d9539b268283bf29d6; buvid4=2148738C-3C00-5BD7-E003-E40F8FC5DD1286820-022012418-c8mC4VtaIp9sn3xNj0%2FQSA%3D%3D; PVID=4; b_lsid=6D101DCDC_182A497E1BC; innersign=1; b_timer=%7B%22ffp%22%3A%7B%22333.851.fp.risk_1EB8D59F%22%3A%22182A497E9C2%22%2C%22333.1193.fp.risk_1EB8D59F%22%3A%22182A497EB90%22%2C%22333.788.fp.risk_1EB8D59F%22%3A%22182A497F0E6%22%7D%7D; bp_video_offset_35141053=694837970900877317"
        }
        res =requests.get(url=newurl,headers=headers)
        # 解析获取标题
        find_title = re.findall(r'<span class="title">(.*)</span>',res.text)
        find_str = '&nbsp;/&nbsp;'
        for title in find_title:
            if find_str in title:
                #去掉多余的符号
                english_title = title.replace('&nbsp;/&nbsp;','')
                english_title_list.append(english_title)
            else:
                chinese_title_list.append(title)
        # 获取评分
        score = re.findall('<span class="rating_num" property="v:average">(.*)</span>',res.text)
        for score_1 in score:
            score_list.append(score_1)
        #多少人评分
        people = re.findall('<span>(\d*)人评价</span>',res.text)
        for people_1 in people:
            people_list.append(people_1)
        #概况
        overview = re.findall('<span class="inq">(.*?)</span>',res.text)
        for overview_1 in overview:
            overview_list.append(overview_1)
        #详细页面
        Movie_url = re.findall('<a href="(.*?)" class="">',res.text)
        for Movie_url_1 in Movie_url:
            Movie_url_list.append(Movie_url_1)
        time.sleep(2)
    save(chinese_title_list,english_title_list,score_list,people_list,overview_list,Movie_url_list)

def save(chinese_title_list,english_title_list,score_list,people_list,overview_list,Movie_url_list):
    conn = pymysql.connect(host="localhost",  # 本地为localhost
                           user="root",
                           password="123456",
                           database="mysql",
                           charset="utf8")
    #创建游标
    cursor = conn.cursor()
    #创建表
    try:
        sql = '''create table movie(id INT auto_increment PRIMARY KEY,
                      chinese_title VARCHAR(20) NOT NULL,
                      english_title VARCHAR(100) NOT NULL,
                      score VARCHAR(100) NOT NULL,
                      people VARCHAR(100) NOT NULL,
                      overview VARCHAR(100) NOT NULL,
                      Movie_url VARCHAR(100) NOT NULL)'''
        cursor.execute(sql)
    except Exception as e:
            print(e)
    with open('douban.csv','w',encoding='utf-8')as f:
        spamwriter = csv.writer(f)
        #csv第一行
        spamwriter.writerow(['中文标题','其他标题','评分','多少人评分','概况','影片详细页面'])
        #for循环保存到csv文件
        for chinese_title,english_title,score,people,overview,Movie_url in zip(chinese_title_list,english_title_list,score_list,people_list,overview_list,Movie_url_list):
            spamwriter.writerow([chinese_title,english_title,score,people,overview,Movie_url])
            #把数据传入到表里
            sql = '''insert into movie(chinese_title,english_title,score,people,overview,Movie_url) values('%s','%s','%s','%s','%s','%s')''' %(chinese_title,english_title,score,people,overview,Movie_url)
            # 执行 sql 语句，把数据插入到数据库中的表
            cursor.execute(sql)
            # 把数据提交到数据库中，不提交数据库不会有数据
            conn.commit()
        f.close()



if __name__ == "__main__":   #当程序执行时候
    #调用函数
        main()
        print("爬取完毕")

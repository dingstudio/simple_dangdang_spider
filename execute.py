import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

table = []

def download(url):
    html = requests.get(url)
    html.encoding = "gbk"
    soup = BeautifulSoup(html.text, "lxml")
    book_list = soup.find("ul", class_="bang_list clearfix bang_list_mode")("li")
    for book in book_list:
        info = book.find_all("div")
        rank = info[0].text[0:-1]
        name = info[2].text
        comments = info[3].text.split("条")[0]
        recommend = info[3].text.split("条")[1].split("评论")[1].split("推荐")[0]
        author = info[4].text
        date_and_publisher = info[5].text.split()
        publish_time = date_and_publisher[0] if len(date_and_publisher) >= 2 else ""
        publisher = date_and_publisher[1] if len(date_and_publisher) >= 2 else ""
        evaluate_count = info[6].text.split("五星评分：")[1].split("次")[0]
        now_price = info[7].text.split("¥")[1] + "元"
        table.append([rank, name, comments, recommend, author, publish_time, publisher, evaluate_count, now_price])
        print("数据抓取成功，当前数据个数：" + str(len(table)))


print("### 当当网图书爬虫演示程序控制台 - 期末作业专用 ###")
print()
print("温馨提示：为了确保程序顺利执行请先确认启动先决条件。\n1、请关闭诸如Excel类的办公软件以避免文件独占锁；\n2、本程序运行所在目录可写入数据，或磁盘空间充裕；\n3、互联网通畅，并确保可以访问bang.dangdang.com网域。")
print()
print()
op = input("程序初始化任务处理完成，请输入您希望爬取的月份编号：（请输入阿拉伯数字，如需爬取近30日的数据，请直接按回车）")
t1 = time.time()
if (op == ""):
    download("http://bang.dangdang.com/books/fivestars")
    df = pd.DataFrame(table, columns=['信息编号', '书名', '评论数', '推荐比例', '作者', "出版日期", "出版社", "评分次数", "价格"])
    df.to_csv("ddangbooks.csv", index=False, encoding="gbk")
else:
    download("http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-month-2019-" + op + "-1-1")
    df = pd.DataFrame(table, columns=['信息编号', '书名', '评论数', '推荐比例', '作者', "出版日期", "出版社", "评分次数", "价格"])
    df.to_csv("ddangbooks0" + op + ".csv", index=False, encoding="gbk")

t2 = time.time()
print('执行总共耗时：%s' % (t2 - t1) + "秒")
print('#' * 30)

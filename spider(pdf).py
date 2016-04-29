#encoding:utf-8

import time
from bs4 import BeautifulSoup
import urllib2
import re
import threading

send_headers = {
    'Host':'pdf1.chnxp.com.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection':'keep-alive'
}

threads = []

HOST="http://www.chnxp.com.cn/"
def save_url(url):
    print(url)
    with open("url.txt","a") as code:
        code.write(url+"\n")

def download_book(url,book_name,send_headers):
    if url == None or book_name == None or send_headers == None:
        return

    req = urllib2.Request(url,headers=send_headers)
    u = urllib2.urlopen(req)
    f = open(book_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (book_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print(book_name,status)

    f.close()

# TODO: 完善返回URL的功能
# def get_url(url,**kwargs):
#     item = None
#     download_url_doc = urllib2.urlopen(url)
#     download_url_details = BeautifulSoup(download_url_doc,"html.parser")
#     for key in kwargs:
#         item = key +"="kwargs[key]
#     download_url_soup  = download_url_details.find("")
#
for x in xrange(4,5):
    sources_url = HOST + "/soft/index_" + str(x) + "newpdf.html"

    html_doc = urllib2.urlopen(sources_url,timeout=5)
    soup = BeautifulSoup(html_doc, "html.parser")
    urls = soup.find_all(href = re.compile("http://www.chnxp.com.cn/soft/2016"), class_="fcb")

    for url in urls:
        if url==None:
            continue
        download_url_book_name = url.get("title")+".zip"
        # 作品详情页，取出跳转下一页的地址
        details_doc = urllib2.urlopen(url.get("href"),timeout=5)
        details_soup = BeautifulSoup(details_doc, "html.parser")
        details_url = details_soup.find(href = re.compile("/e/DownSys/DownSoft/"))
        # 下载页面，取出正真的下载地址
        if details_url==None:
            continue
        download_doc = urllib2.urlopen(HOST+details_url.get("href"),timeout=5)
        download_soup = BeautifulSoup(download_doc, "html.parser")
        download_url = download_soup.find(id = "111111")
        # print download_url.get_text()
        if download_url==None:
            continue
        # 保存地址到URL.txt
        save_url(download_url.get_text())
        # 添加多线程任务
        t = threading.Thread(target=download_book, name=download_url_book_name.encode("utf8"),
                             args=(download_url.get_text(), download_url_book_name,send_headers))
        threads.append(t)
        # 直接下载文件
        # download_book(download_url.get_text(),download_url_book_name,send_headers)

# 开始多线程下载文件
for t in threads:
    print(t.name)
    time.sleep(10)
    t.setDaemon(True)
    t.start()

# 防止主线程退出导致的子线程被销毁
for t in threads:
    t.join()





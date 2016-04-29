#encoding:utf-8
from bs4 import BeautifulSoup
import urllib2
import re
import threading

def download_book(url,book_name):
    print(url,book_name)
    books = urllib2.urlopen(url).read()
    with open(book_name,"wb") as code:
        code.write(books)

for x in xrange(2,82):
    sources_url = "http://kankindle.com/simple/page/"+str(x)
    html_doc = urllib2.urlopen(sources_url)
    soup = BeautifulSoup(html_doc,"html.parser")

    urls = soup.find_all(href = re.compile("http://kankindle.com/view"))
    for url in urls:
        if url.get("title")=="大家好，欢迎来到看kindle！！！！！！":
            continue

        download_url_book_name = url.get("title")+".mobi"
        download_url_doc = urllib2.urlopen(url.get("href"))
        download_url_soup = BeautifulSoup(download_url_doc,"html.parser")
        download_url = download_url_soup.find(href = re.compile("down"))

        if download_url!=None:
            download_book(download_url.get("href"),download_url_book_name)






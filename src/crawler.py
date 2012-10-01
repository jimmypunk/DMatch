from bs4 import BeautifulSoup
import urllib2
import re
import os
import urlparse
import sys

def fetchImage(url):
    htmlData = urllib2.urlopen(url).read()
    soup = BeautifulSoup(htmlData)
    imgs = soup.findAll("img")
    for img in imgs:
        imgUrl = urlparse.urljoin(url,img['src'])
        print "downloading img" + imgUrl + "..."
        cmd = "wget -P ./../res "+imgUrl
        os.system(cmd)

def main():
<<<<<<< HEAD
	if(len(sys.argv) != 2):
		print "[usage] python crawler.py url"
		exit()
	fetchImage(argv[1])

if __name__ =="__main__":
	main()

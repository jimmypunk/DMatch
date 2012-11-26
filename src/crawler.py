from bs4 import BeautifulSoup
import urllib2
import urllib
import re
import os
import urlparse
import sys

def fetchImage(url):
    htmlData = urllib2.urlopen(url).read()
    soup = BeautifulSoup(htmlData)
    imgs = soup.findAll("img")
    count = 0
    for img in imgs:
        imgUrl = urlparse.urljoin(url,img['src'])
        print "downloading img" + imgUrl + "..."
        #cmd = "wget -P ./../res "+imgUrl
        #os.system(cmd)
        
        urllib.urlretrieve(imgUrl, "./../res/url"+str(count)+".jpg")
        count = count +1;

def main():
	if(len(sys.argv) != 2):
		print "[usage] python crawler.py url"
		exit()
      


	fetchImage(sys.argv[1])

if __name__ =="__main__":
	main()

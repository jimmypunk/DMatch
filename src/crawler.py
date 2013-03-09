from bs4 import BeautifulSoup
import urllib2
import urllib
import re
import os
import urlparse
import sys
from Queue import Queue
visited_url = []
loaded_image_url = []
container = Queue()
def fetchImage(hostname):

    while(container.empty() == False):
        url,depth = container.get()
        if url in visited_url or depth>3 or hostname!=urlparse.urlparse(url).hostname:
            continue
        visited_url.append(url)
        print 'visiting '+url +' at depth:',depth
        htmlData = urllib2.urlopen(url).read()
        soup = BeautifulSoup(htmlData)
        
        #search imgs in this body section
        
        articles = soup.body("article")
        count = 0
        for article in articles:
            if(article.img['src']==""):
                continue
            imgUrl = urlparse.urljoin(url,article.img['src'])
            appName = article.section.h3.a.string
            category = article.section.h3.span.string
            if(imgUrl not in loaded_image_url):
                print 'imgUrl:' + imgUrl + ' appName:' +appName.encode('big5','ignore') + ' category:'+category.encode('big5','ignore')+' found'
                loaded_image_url.append(imgUrl)
                count = count +1;
                #print "downloading img:" + imgUrl + "	..."
                #cmd = "wget -P ./../res "+imgUrl
                #os.system(cmd)
                #urllib.urlretrieve(imgUrl, "./../res/url"+str(count)+".jpg")
        
        #search for adjancy pages
        links = soup('a')
        for link in links:
            if('href' in dict(link.attrs)):
                newurl = urlparse.urljoin(url,link['href'])
                container.put((newurl,depth+1))
        
def main():
    if(len(sys.argv) != 2):
		print "[usage] python crawler.py url"
		exit()
    container.put((sys.argv[1],0))
    hostname = urlparse.urlparse(sys.argv[1]).hostname
    fetchImage(hostname)

if __name__ =="__main__":
	main()

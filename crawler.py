#!/usr/bin/env python
# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
from urllib2 import urlopen
import re

class Crawler(HTMLParser):
    def __init__(self, starting_url, depth, max_span):
        HTMLParser.__init__(self)
        self.url = starting_url
        self.db = {self.url: {'linkedPages':[],'staticAssets':[]}}
        #self.db = {self.url: 1}
        self.linksCrawled = []
        self.linksToBeCrawled = [self.url]
        #self.linksToBeCrawled = {self.url}
        # Get the domain from the link
        self.domain = re.sub(r'https?\:\/\/','',self.url,1)
        print('domain is ' + self.domain)

        self.depth = depth # recursion depth max
        self.max_span = max_span # max links obtained per url
        self.links_found = 0

    def handle_starttag(self, tag, attrs):
        if self.url not in self.db:
            # Add this new URL to the db
            self.db[self.url] = {'linkedPages':[],'staticAssets':[]}
        else:
            print(self.url + ' is already in db')
            print(self.db)

        if self.links_found < self.max_span and tag == 'a' and attrs:
            link = attrs[0][1]

            if link[:4] != "http":
                #print('link[:4] does not equal http')
                #print(link)
                link = '/'.join(self.url.split('/')[:3])+('/'+link).replace('//','/')
                #print('updated link is')
                #print(link)

            #print(self.db)
            # If this link is within the target domain and we haven't added it to the linksToBeCrawled yet, do so
            if (self.domain in link) and (link not in self.linksCrawled) and (link not in self.linksToBeCrawled):
                print "adding link to linksToBeCrawled ---> %s" % link
                #self.links_found += 1
                self.linksToBeCrawled.append(link)
                #self.linksToBeCrawled.add(link)
                print('@@@ Links to be crawled:')
                print(self.linksToBeCrawled)
            
            #print('about to add url to DB and add linkedPages, self.url is ' + self.url)
            # Add all links to the page's dict record
            print('&&& URL for this handle_ iteration is ' + self.url)
            linkedPages = self.db[self.url]['linkedPages']
            print('&&& linkedPages for this handle_ iteration is ')
            print(linkedPages)
            if link not in linkedPages:
                linkedPages.append(link)
            print('&&& linkedPages after append for this handle_ iteration is ')
            print(linkedPages)
            self.db[self.url]['linkedPages'] = linkedPages
            print(self.db)

            # Add this link to the linksCrawled list either way
            self.linksCrawled.append(self.url)
            self.links_found += 1
        elif tag in ['img','script'] and attrs:
            link = attrs[0][1]

            if link[:4] != "http":
                link = '/'.join(self.url.split('/')[:3])+('/'+link).replace('//','/')

            staticAssets = self.db[self.url]['staticAssets']
            print('&&& staticAssets for this handle_ iteration is ')
            print(staticAssets)
            if link not in staticAssets:
                staticAssets.append(link)
            print('&&& staticAssets after append for this handle_ iteration is ')
            print(staticAssets)
            self.db[self.url]['staticAssets'] = staticAssets
            print(self.db)

    def crawl(self):
        for depth in xrange(self.depth):
            print "*"*70+("\nScanning depth %d web\n" % (depth+1))+"*"*70
            #print('linksToBeCrawled is:')
            #print(self.linksToBeCrawled)
            context_node = self.linksToBeCrawled
            print('context_node is:')
            print(context_node)
            #self.linksToBeCrawled = []
            for self.url in context_node:
                print('*** context_node is:')
                print(context_node)
                print('### current url is ' + self.url)
                self.links_found = 0
                try:
                    req = urlopen(self.url)
                    res = req.read()
                    self.feed(res)
                except:
                    self.reset()
                # Add this URL to the linksCrawled list
                self.linksCrawled.append(self.url)
        print "*"*40 + "\nRESULTS\n" + "*"*40
        zorted = [(v,k) for (k,v) in self.db.items()]
        zorted.sort(reverse = True)
        #return zorted
        #print zorted
        #print self.db.items()
        #return self.db.items()
        return self.db

if __name__ == "__main__":
    crawler = Crawler(starting_url = 'http://cassieandalexwedding.com/', depth = 3, max_span = 25)
    result = crawler.crawl()
    #print('result is:')
    #print(result)
    for item in result:
        #print "%s was found %d time%s." %(link,n, "s" if n is not 1 else "")
        if not result[item]['linkedPages']:
            print "%s was found with no linked pages." %(item)
            print('\n')
        else:
            print "%s was found with linked page(s) %s \n and static assets %s" %(item,result[item]['linkedPages'],result[item]['staticAssets'])
            print('\n')


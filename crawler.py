#!/usr/bin/env python
# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
from urllib2 import urlopen
import re


class Crawler(HTMLParser):
    def __init__(self, starting_url, depth, max_span):
        """
        Initialize the Crawler object and its properties.

        parameters:
            self:         self reference to object
            starting_url: string. the URL of the site to be crawled, in the
                          format of 'http://sub.domain.com/'
            depth:        integer. level of recursion this script should allow.
                          Large values may result in very long run times
            max_span:     integer. The maximum number of links that can be
                          retrieved from a single page request.

        returns:
            Crawler object
        """
        if starting_url[:4] != "http":
            print('Site name must include http:// or https:// protocol')
            exit()

        HTMLParser.__init__(self)

        # Set class variables to passed parameter values or initial values
        self.depth = depth  # recursion depth max
        self.max_span = max_span  # max links obtained per url
        self.links_found = 0
        self.url = starting_url
        self.db = {self.url: {'linkedPages': [], 'staticAssets': []}}
        self.linksCrawled = []
        self.linksToBeCrawled = [self.url]

        # Get the domain from the URL
        self.domain = re.sub(r'https?\:\/\/', '', self.url, 1)

    def handle_starttag(self, tag, attrs):
        """
        Handle all opening XML (HTML in this case) tags passed to the
        HTMLParser object. This will normally be done via the HTMLParser.feed()
        function See https://docs.python.org/2/library/htmlparser.html \
        #HTMLParser.HTMLParser.handle_starttag

        parameters:
            self:         self reference to object
            tag:          string. the tag type ('a','img','link,'meta', etc)
            attrs:        list. List of two-valued tuples, representing
                          an attribute and it's value for a given tag.
                          For example, a 'span' tag
                          with style="width:100%;" would have attributes
                          as follows: attrs == [('style','width:100%;')]

        returns:
            None (NoneType)
        """
        if self.url not in self.db:
            # Add this new URL to the db as a key and initialize lists
            self.db[self.url] = {'linkedPages': [], 'staticAssets': []}
        else:
            # URL already in DB as a key, don't need to create a dict item
            pass

        if self.links_found < self.max_span and tag == 'a' and attrs:
            # Iterate over attrs list and find href value
            for attr in attrs:
                if attr[0] == 'href':
                    link = attr[1]

            # Handle relative paths by adding the self.url in front of the link
            if link[:4] != "http":
                link = '/'.join(self.url.split('/')[:3]) + \
                    ('/'+link).replace('//', '/')

            # If this link is within the target domain and we haven't added it
            # to the linksToBeCrawled yet, do so
            if ((self.domain in link) and (link not in self.linksCrawled) and
               (link not in self.linksToBeCrawled)):
                self.linksToBeCrawled.append(link)

            # Add all new links to the page's dict record
            linkedPages = self.db[self.url]['linkedPages']
            if link not in linkedPages:
                linkedPages.append(link)
            self.db[self.url]['linkedPages'] = linkedPages

            # Add this link to the linksCrawled list either way
            self.linksCrawled.append(self.url)
            # Increment links_found
            self.links_found += 1

        # Handle static assets such as img, script, and link tags
        elif tag in ['img', 'script', 'link'] and attrs:
            # Iterate over attrs list and find src (for image tags
            # and script tags) or href value (for link tags)
            for attr in attrs:
                if attr[0] in ['src', 'href']:
                    link = attr[1]

            if link[:4] != "http":
                link = '/'.join(self.url.split('/')[:3]) + \
                    ('/'+link).replace('//', '/')

            staticAssets = self.db[self.url]['staticAssets']
            if link not in staticAssets:
                staticAssets.append(link)
            self.db[self.url]['staticAssets'] = staticAssets

    def crawl(self):
        """
        For each link not yet crawled, captures HTML page content and feeds it
        to the HTMLParser for tag processing.

        parameters:
            self:         self reference to object

        returns:
            dict
        """
        for depth in xrange(self.depth):
            context_node = self.linksToBeCrawled
            for self.url in context_node:
                # Don't crawl links we've already crawled
                if self.url not in self.linksCrawled:
                    self.links_found = 0
                    try:
                        req = urlopen(self.url)
                        res = req.read()
                        self.feed(res)
                    except:
                        self.reset()
                    # Add this URL to the linksCrawled list
                    self.linksCrawled.append(self.url)
        return self.db

if __name__ == "__main__":
    crawler = Crawler(starting_url='http://dustyfeet.com', depth=3,
                      max_span=50)
    result = crawler.crawl()
    print('result is:')
    print(result)

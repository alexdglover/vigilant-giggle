#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawler import Crawler
import unittest


class MyTest(unittest.TestCase):

    def setUp(self):
        self.url = 'http://alexdglover.github.io'
        self.depth = 25
        self.max_span = 50
        self.crawler = Crawler(starting_url=self.url, depth=self.depth,
                               max_span=self.max_span)
        self.result = self.crawler.crawl()
        self.sampleSiteHTML = ''
        with open('sampleSite.html') as inputfile:
            for line in inputfile:
                self.sampleSiteHTML += line

    def testVerifyActualDepthMatchesDepthParameter(self):
        self.assertEqual(self.depth, self.crawler.depth)

    def testVerifyActualmax_spanLessThanOrEqualTomax_spanParameter(self):
        # Get the largest set of linkedPages
        maxLinkedPageCount = 0
        for k, v in self.crawler.db.iteritems():
            linkedPageCount = len(v['linkedPages'])
            if linkedPageCount > maxLinkedPageCount:
                maxLinkedPageCount = linkedPageCount
        self.assertLessEqual(maxLinkedPageCount, self.max_span)

    def testVerifyClassInstantiationReturnsClassObject(self):
        self.assertIsInstance(self.crawler, Crawler)

    def testVerifyhandle_starttagMethodThrowsErrorWithNoParameters(self):
        with self.assertRaises(TypeError) as cm:
            self.crawler.handle_starttag()

    def testVerifycrawlMethodThrowsErrorWithNoParameters(self):
        with self.assertRaises(TypeError) as cm:
            self.crawler.crawl('string')

    def testVerifyhandle_starttagHandlesTagsWithNoAttrs(self):
        self.assertIsNone(self.crawler.handle_starttag('a', []))

    def testVerifyhandle_starttagIncrementsLinksFound(self):
        startingLinksFound = self.crawler.links_found
        self.crawler.handle_starttag('a', [('href', 'http://someurl.com')])
        self.assertEqual((startingLinksFound + 1), self.crawler.links_found)

    def testVerifyhandle_starttagNotIncrementLinksFoundWhenFindingAssets(self):
        startingLinksFound = self.crawler.links_found
        self.crawler.handle_starttag('img', [('src',
                                     'http://someurl.com/image.jpg')])
        self.assertEqual((startingLinksFound), self.crawler.links_found)

    def testVerifyhandle_starttagDoesNotIncrementLinksFoundWhenNoAttrs(self):
        startingLinksFound = self.crawler.links_found
        self.crawler.handle_starttag('a', [])
        self.assertEqual((startingLinksFound), self.crawler.links_found)

    def testVerifyhandle_starttagAddsLinksFoundToDict(self):
        self.crawler.url = self.url
        self.crawler.handle_starttag('a', [('href', 'http://someurl.com')])
        self.assertTrue('http://someurl.com' in
                        self.crawler.db[self.crawler.url]['linkedPages'])

    def testVerifyhandle_starttagAddsStaticAssetsToDict(self):
        self.crawler.url = self.url
        self.crawler.handle_starttag('img',
                                     [('src', 'http://someurl.com/image.jpg')])
        self.assertTrue('http://someurl.com/image.jpg' in
                        self.crawler.db[self.crawler.url]['staticAssets'])

    def testVerifyCrawlMethodReturnsDictObject(self):
        self.assertIsInstance(self.result, dict)

    def testVerifyCrawlMethodReturnsDictObjectWithLinkedPageList(self):
        self.assertIsInstance(self.result[self.url]['linkedPages'], list)

    def testVerifyCrawlMethodReturnsDictObjectWithStaticAssestsList(self):
        self.assertIsInstance(self.result[self.url]['staticAssets'], list)

    # Test against a static sample page of HTML
    def testVerifyStaticAssetCountFromSampleSiteHTML(self):
        self.crawler.db = {}
        self.crawler.url = 'http://samplesite.com'
        self.crawler.feed(self.sampleSiteHTML)
        self.assertEqual(len(
            self.crawler.db['http://samplesite.com']['staticAssets']), 6)

    # Test against a static sample page of HTML
    def testVerifyLinkedPageCountFromSampleSiteHTML(self):
        self.crawler.db = {}
        self.crawler.url = 'http://samplesite.com'
        self.crawler.feed(self.sampleSiteHTML)
        self.assertEqual(len(
            self.crawler.db['http://samplesite.com']['linkedPages']), 4)

if __name__ == '__main__':
    unittest.main()

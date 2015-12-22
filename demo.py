#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crawler import Crawler
from publisher import Publisher
import pydot
import re
import xml.etree.cElementTree as ET


crawler = Crawler(starting_url='http://alexdglover.github.io', depth=5,
                  max_span=50)

result = crawler.crawl()

publisher = Publisher()

publisher.drawSiteMapImage(result)

publisher.exportToXMLSitemap(result)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawler import Crawler
import pydot
import re
import xml.etree.cElementTree as ET


class Publisher():

    def drawSiteMapImage(self, result):
        # Create a graph object
        graph = pydot.Dot(graph_type='digraph')
        # For each top level key in the dict (effectively each page crawled)
        for key, value in result.iteritems():
            # Cast the key to string in case it's unicode
            str(key)
            # Remove the http:// or https:// prefix and wrap in single quotes,
            # as PyDot will choke on special characters
            key = re.sub(r'https?\:\/\/', '', key, 1)
            safePageString = '"' + key + '"'
            # Create and add the node to the chart if it doesn't exist already
            pageNode = pydot.Node(safePageString, style="filled",
                                  fillcolor="red")
            graph.add_node(pageNode)

            # For each linked page, add a node if it doesn't exist already
            # If it the node does already exist, draw a line from this node
            # to the linked page node
            for linkedPage in value['linkedPages']:
                # Cast the linkedPage to string in case it's unicode
                str(linkedPage)
                # Remove http:// and https:// as PyDot doesn't handle it well
                linkedPage = re.sub(r'https?\:\/\/', '', linkedPage, 1)
                # Double quote node name as PyDot doesn't handle special chars
                # well
                safeLinkedPageString = '"' + linkedPage + '"'
                # Create a new node for the linked page
                linkedPageNode = pydot.Node(safeLinkedPageString)
                graph.add_node(linkedPageNode)
                # Draw a line from the original page node to the linkedPage
                # node
                edge = pydot.Edge(pageNode, linkedPageNode)
                graph.add_edge(edge)

            # For each static asset, add a node (with static asset icon) to the
            # chart if it doesn't exist already and draw a line from this node
            # to the static asset
            for staticAsset in value['staticAssets']:
                # Cast the linkedPage to string in case it's unicode
                str(staticAsset)
                # Remove http:// and https:// as PyDot doesn't handle it well
                staticAsset = re.sub(r'https?\:\/\/', '', staticAsset, 1)
                # Double quote node name as PyDot doesn't handle special
                # chars well
                safeStaticAssetString = '"' + staticAsset + '"'
                # Create a new node for the linked page
                staticAssetNode = pydot.Node(safeStaticAssetString,
                                             style="filled", fillcolor="blue")
                graph.add_node(staticAssetNode)
                # Draw a line from the page node to the linkedPage node
                edge = pydot.Edge(pageNode, staticAssetNode)
                graph.add_edge(edge)

        # Draw the chart
        try:
            graph.write_png('sitemap_graph.png')
        except:
            print('couldnt export to png')

    def exportToXMLSitemap(self, result):
        xmlString = ''
        root = ET.Element('urlset')
        loc = ''
        for key in result:
            doc = ET.SubElement(root, "url")
            loc = ET.SubElement(doc, "loc").text = key
        tree = ET.ElementTree(root)
        tree.write("sitemap.xml")

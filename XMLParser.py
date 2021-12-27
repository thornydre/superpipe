#!/usr/bin/python

import xml.etree.ElementTree

from os import makedirs

class XMLParser:
	def __init__(self, xml_file):
		self.xml_file = xml_file


	def parseXML(self, root_folder):
		root = xml.etree.ElementTree.parse(self.xml_file).getroot()
		self.recursiveParser(root, root_folder)


	def recursiveParser(self, root, root_folder):
		if root.tag == "dir":
			makedirs(root_folder)

		for child in root:
			self.recursiveParser(child, root_folder + "/" + child.attrib["name"])
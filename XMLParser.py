#!/usr/bin/python

import xml.etree.ElementTree

from pathlib import Path
from os import makedirs

class XMLParser:
	def __init__(self, xml_file):
		self.xml_file = xml_file

		self.tags = {}


	def parseXML(self, root_folder):
		root = xml.etree.ElementTree.parse(self.xml_file).getroot()
		self.recursiveParser(root, root_folder)


	def recursiveParser(self, root, root_folder):
		if root.tag == "dir":
			if not Path(root_folder).is_dir():
				makedirs(root_folder)

		for child in root:
			self.recursiveParser(child, root_folder + "/" + child.attrib["name"])


	def pathToTag(self, root_folder):
		root = xml.etree.ElementTree.parse(self.xml_file).getroot()
		self.recursivePathToTag(root, root_folder)

		return self.tags


	def recursivePathToTag(self, root, root_folder):
		if "tag" in root.attrib.keys():
			self.tags[root.attrib["tag"]] = root_folder

		for child in root:
			self.recursivePathToTag(child, root_folder + "/" + child.attrib["name"])

#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

from Resources import *

class Theme():
	def __init__(self, theme_name):
		self.main_color = Resources.readLine("save/themes/" + theme_name + ".spi", 1)
		self.second_color = Resources.readLine("save/themes/" + theme_name + ".spi", 2)
		self.list_color = Resources.readLine("save/themes/" + theme_name + ".spi", 3)
		self.button_color1 = Resources.readLine("save/themes/" + theme_name + ".spi", 4)
		self.over_button_color1 = Resources.readLine("save/themes/" + theme_name + ".spi", 5)
		self.button_color2 = Resources.readLine("save/themes/" + theme_name + ".spi", 6)
		self.over_button_color2 = Resources.readLine("save/themes/" + theme_name + ".spi", 7)
		self.separator_color = Resources.readLine("save/themes/" + theme_name + ".spi", 8)
		self.text_color = Resources.readLine("save/themes/" + theme_name + ".spi", 9)
		self.disabled_button_color2 = Resources.readLine("save/themes/" + theme_name + ".spi", 10)
		self.disabled_text_color = Resources.readLine("save/themes/" + theme_name + ".spi", 11)
		self.done_color = Resources.readLine("save/themes/" + theme_name + ".spi", 12)
		self.urgent_color = Resources.readLine("save/themes/" + theme_name + ".spi", 13)
		self.high_color = Resources.readLine("save/themes/" + theme_name + ".spi", 14)
		self.medium_color = Resources.readLine("save/themes/" + theme_name + ".spi", 15)
		self.done_select_color = Resources.readLine("save/themes/" + theme_name + ".spi", 16)
		self.urgent_select_color = Resources.readLine("save/themes/" + theme_name + ".spi", 17)
		self.high_select_color = Resources.readLine("save/themes/" + theme_name + ".spi", 18)
		self.medium_select_color = Resources.readLine("save/themes/" + theme_name + ".spi", 19)
		self.stat_list_color1 = Resources.readLine("save/themes/" + theme_name + ".spi", 20)
		self.stat_list_color2 = Resources.readLine("save/themes/" + theme_name + ".spi", 21)
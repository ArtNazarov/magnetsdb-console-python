#!/usr/bin/python
# import dependencies
import sqlite3
import os
# require pip install terminaltables
from terminaltables import AsciiTable
from subprocess import call

class Config:
	CONFIG = {
		"SEARCH_ACTION": "search",
		"PREV_PAGE": "prev",
		"NEXT_PAGE": "next",
		"REPEAT": "repeat",
		"QUIT": "quit",
		"PATH_TO_DB": "F:\magnetsdb\main-sqlite.db",
		"app": "qbittorrent.exe",
		"limit": 40
	}

class MainView:
	def cls(self):
		os.system('cls' if os.name == 'nt' else 'clear')
	def output(self, a, table_data):
		print("Output called")
		self.cls()
		print('request: {} page:{}'.format(a['request'], a['page']))
		table = AsciiTable(table_data)
		print(table.table)

class OnRequest:
	def __init__(self, controller):
		self.__c = controller;
	def request(self, a):
		conn = sqlite3.connect(Config.CONFIG['PATH_TO_DB'])
		sorting_field = 'caption'
		order_by = 'asc'
		limit = Config.CONFIG['limit']
		print(limit)
		offset = (int(a['page']) - 1) * int(limit)
		cursor = conn.execute(
			"SELECT category, caption, labels, hash from data WHERE caption LIKE '%{}%' ORDER BY {} {} LIMIT {} OFFSET {}".format(
				a['request'], sorting_field, order_by, limit, offset))
		table_data = [['Num', 'Category', 'Caption', 'Labels', 'Hash']]
		num = 0
		for row in cursor:
			# print("category={}".format(row[0]))
			# print("caption={}".format(row[1]))
			# print("labels={}".format(row[2]))
			# print("hash={}".format(row[3]))
			num = num + 1
			table_data.append([str(num), row[0], row[1], row[2], row[3]])
		return table_data

class OnExtApp:
	def ext_app(self, td):
		num = 99
		while num > 0:
			print("Download something? type 0 if not needed.")
			num = int(input("Choice:"))
			if num == 0:
				break
			call([
				Config.CONFIG['app'],
				td[num][4]
			])



class MainController:
	args = [];
	action_from_input = "start"
	request_from_input = "test"
	page_from_input = "1"

	def MainLoop(self):
		while not self.action_from_input == Config.CONFIG['QUIT']:
			self.action_from_input = input("Action(available:search,repeat,next,prev,quit): ")
			if self.action_from_input == Config.CONFIG["SEARCH_ACTION"]:
				self.request_from_input = input("Request: ")
				self.page_from_input = input("Page(1,2,etc): ")
			if self.page_from_input == "":
				self.page_from_input = "1"

			if self.action_from_input == Config.CONFIG["NEXT_PAGE"]:
				# request_from_input does not change
				self.page_from_input = str(int(self.args['page'])+1)

			if self.action_from_input == Config.CONFIG["PREV_PAGE"]:
				# request_from_input does not change
				if int(self.args['page'])>1:
					self.page_from_input = str(int(args['page'])-1)

			self.args = {
				'action': self.action_from_input,
				'request': self.request_from_input,
				"page" : self.page_from_input
			}

			if (self.args['action'] in (Config.CONFIG['REPEAT'], Config.CONFIG['SEARCH_ACTION'], Config.CONFIG['PREV_PAGE'], Config.CONFIG['NEXT_PAGE'])):
				if not self.args['action'] == Config.CONFIG['REPEAT']:
					MyRequest = OnRequest(self);
					table_data = MyRequest.request(self.args)

				MyView = MainView();
				MyView.output(self.args, table_data)
				MyExtApp = OnExtApp();
				MyExtApp.ext_app(table_data)


MyApp = MainController();
MyApp.MainLoop();

#!/usr/bin/python

CONST = {
	"SEARCH_ACTION" :  "search",
	"PATH_TO_DB" : "F:\magnetsdb\main-sqlite.db",
	"app"	: "qbittorrent.exe"
	}
print(CONST['SEARCH_ACTION'])
print(CONST['PATH_TO_DB'])

# import dependencies

import sqlite3
# require pip install terminaltables
from terminaltables import AsciiTable
# for calling external app
import os

action_from_input = input("Action(available:search): ")

request_from_input = "test"
if action_from_input == CONST["SEARCH_ACTION"]:
	request_from_input = input("Request: ")

args = {'action': action_from_input, 'request': request_from_input}

if args['action'] == CONST['SEARCH_ACTION']:
	conn = sqlite3.connect(CONST['PATH_TO_DB'])
	sorting_field = 'caption'
	order_by = 'asc'
	cursor = conn.execute("SELECT category, caption, labels, hash from data WHERE caption LIKE '%{}%' ORDER BY {} {} LIMIT 10 OFFSET 0".format(args['request'], sorting_field, order_by))
	table_data = [['Num', 'Category', 'Caption', 'Labels', 'Hash']]
	num = 0
	for row in cursor:
		#print("category={}".format(row[0]))
		#print("caption={}".format(row[1]))
		#print("labels={}".format(row[2]))
		#print("hash={}".format(row[3]))
		num = num + 1
		table_data.append([str(num), row[0], row[1], row[2], row[3]])
	table = AsciiTable(table_data)
	print(table.table)

	num = 99
	while num > 0:
		print("Download something? type 0 if not needed.")
		num = int(input("Choice:"))
		if num == 0:
			break
		os.system("{} magnet:?xt=urn:btih:{}".format(
				CONST['app'],
				table_data[num][4]
					))





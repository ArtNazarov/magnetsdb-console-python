#!/usr/bin/python

CONST = { "SEARCH_ACTION" :  "search", "PATH_TO_DB" : "F:\magnetsdb\main-sqlite.db"}
print(CONST['SEARCH_ACTION'])
print(CONST['PATH_TO_DB'])

# import dependencies

import sqlite3
# require pip install terminaltables
from terminaltables import AsciiTable


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
	table_data = [
		['Category', 'Caption', 'Labels', 'Hash']
	]
	for row in cursor:
		#print("category={}".format(row[0]))
		#print("caption={}".format(row[1]))
		#print("labels={}".format(row[2]))
		#print("hash={}".format(row[3]))
		table_data.append([row[0], row[1], row[2], row[3]])
	table = AsciiTable(table_data)
	print(table.table)
	print("request ended")

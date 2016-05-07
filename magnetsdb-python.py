#!/usr/bin/python
# import dependencies
import sqlite3
import os
# require pip install terminaltables
from terminaltables import AsciiTable
from subprocess import call


def output(args, table_data):
	cls()
	print('request: {} page:{}'.format(args['request'], args['page']))
	table = AsciiTable(table_data)
	print(table.table)

def request(a):
	conn = sqlite3.connect(CONST['PATH_TO_DB'])
	sorting_field = 'caption'
	order_by = 'asc'
	offset = (int(a['page']) - 1) * 10
	cursor = conn.execute(
		"SELECT category, caption, labels, hash from data WHERE caption LIKE '%{}%' ORDER BY {} {} LIMIT 10 OFFSET {}".format(
			a['request'], sorting_field, order_by, offset))
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

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def ext_app(C, td):
	num = 99
	while num > 0:
		print("Download something? type 0 if not needed.")
		num = int(input("Choice:"))
		if num == 0:
			break
		call([
			C['app'],
			td[num][4]
		])

action_from_input = "start"
request_from_input = "test"
page_from_input = "1"


CONST = {
	"SEARCH_ACTION" :  "search",
	"PREV_PAGE" : "prev",
	"NEXT_PAGE" : "next",
	"REPEAT" : "repeat",
	"QUIT" : "quit",
	"PATH_TO_DB" : "F:\magnetsdb\main-sqlite.db",
	"app"	: "qbittorrent.exe"
	}

print(CONST['SEARCH_ACTION'])
print(CONST['PATH_TO_DB'])

while not action_from_input == CONST['QUIT']:
	action_from_input = input("Action(available:search,repeat,next,prev,quit): ")
	if action_from_input == CONST["SEARCH_ACTION"]:
		request_from_input = input("Request: ")
		page_from_input = input("Page(1,2,etc): ")
		if page_from_input == "":
			page_from_input = "1"

	if action_from_input == CONST["NEXT_PAGE"]:
		# request_from_input does not change
		page_from_input = str(int(args['page'])+1)

	if action_from_input == CONST["PREV_PAGE"]:
		# request_from_input does not change
		if int(args['page'])>1:
			page_from_input = str(int(args['page'])-1)

	args = {'action': action_from_input, 'request': request_from_input, "page" : page_from_input}

	if (args['action'] in ( CONST['REPEAT'], CONST['SEARCH_ACTION'],CONST['PREV_PAGE'], CONST['NEXT_PAGE'])):
		if not args['action'] == CONST['REPEAT']:
			table_data = request(args)
		output(args, table_data)
		ext_app(CONST, table_data)





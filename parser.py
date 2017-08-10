#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import argparse
import os
import re
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help='the file to parse')
parser.add_argument('-d', '--write-to-db', action="store_true", default=False, help="Write the log to the database")
args = parser.parse_args()

if not args.filename:
	print "You need to specify a file to parse"
	parser.print_help()
	exit(1)

# create a sqlite3 database to hold the logs
if args.write_to_db:
	db = sqlite3.connect('logs.db')
	db.text_factory = str
	db.execute('CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME, username TEXT, message TEXT)')

# https://regex101.com/r/pMp8Gz/1
#TODO: combine these two res into one. should be doable.
re_parser = re.compile('(?P<timestamp>\d{1,2}[/.]\d{1,2}[/.]\d{2,4},? \d{1,2}:\d{2}(?::\d{2})?(?: [AP]M)?)(?: -|:) (?P<username>.+?): (?P<message>.+)')
re_attach = re.compile('(?P<filename>.+) <.+attached>', re.UNICODE)

log = open(args.filename).readlines()
for line in log:
	match = re_parser.match(line)
	if match:
		line = line.replace('\r\n', ' ')

		dt = datetime.strptime(match.group('timestamp'), '%m/%d/%y, %H:%M:%S')
		who = match.group('username')
		message = match.group('message')

		amatch = re_attach.match(message)
		if amatch:
			pass
			# attachment messages look like: `ATTACHMENT: 2017-03-19-PHOTO-00003492.jpg <<U+200E>‎attached>` 
			print 'ATTACHMENT: {} -> {}'.format(match.group('username'), amatch.group('filename'))
		else:
			pass
			# normal chat message
			print "({}) {}: {}".format(dt, who, message)

		if args.write_to_db:
			db.execute(u'insert into logs (timestamp, username, message) values(?, ?, ?)', (dt, who, message))

# Fix my name
if args.write_to_db:
	db.execute('update logs set username = "Nick Kuzmik" where username = "Nick"')
	db.commit()

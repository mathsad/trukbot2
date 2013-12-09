#!/usr/bin/env python
import json

class commandHandler:
	def __init__(self):
		print "commandhandler.py loaded"

	def parse_question(self, user

fileload = file("#hpqoeu.json", "r").read()

jsonfile = json.loads(fileload)
print jsonfile

command = raw_input("enter your command: ")
answer = raw_input("enter your answer: ")

jsonfile[command] = answer

print jsonfile

with file("#hpqoeu.json", "w") as outfile:
	json.dump(jsonfile, outfile, indent=4)
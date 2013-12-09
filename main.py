#!/usr/bin/env python
import multiprocessing, json, sys, traceback # for shit
from modules import irc, lastfm
from ConfigParser import RawConfigParser

import re

class bot:
	def __init__(self):

		parser = RawConfigParser()

		parser.read("botconfig.cfg")

		self.botNick, self.botPassword, self.lastFMApiKey = parser.get("settings", "botNick"), parser.get("settings", "botPassword"), parser.get("settings", "lastFMApiKey")

		self.np = lastfm.NowPlaying()

	def load_channels(self):

		self.channelFile = open("channels.txt", "r")
		self.channelsToJoin = self.channelFile.readlines()	# all this reads in channels.txt to know which channels to join
		self.channelsToJoin = [line.rstrip("\r\n") for line in self.channelsToJoin]
		self.channelFile.close()

		self.commandFiles = {}
		self.channelCommands = {}
		self.channelExecs = {}
		self.channelTriggers = {}

	def load_commands(self):

		try:
			for x in self.channelsToJoin:
				self.commandFiles[x] = file(x + ".commands.json", "r").read()
				self.channelCommands[x] = json.loads(self.commandFiles[x])

			for x in self.channelsToJoin:
				self.commandFiles[x] = file(x + ".execs.json", "r").read()
				self.channelExecs[x] = json.loads(self.commandFiles[x])

			for x in self.channelsToJoin:
				self.commandFiles[x] = file(x + ".triggers.json", "r").read()
				self.channelTriggers[x] = json.loads(self.commandFiles[x])
		except:
			print sys.exc_info()[0] #prints the exception class
			print sys.exc_info()[1] #prints the error message
			print repr(traceback.format_tb(sys.exc_info()[2])) #prints the stack

	def do_last_fm(self, lastfmUserName, userChannel):
			artistName, trackName, albumName = self.np.main(lastfmUserName, self.lastFMApiKey)
			self.ircConnection.send_message(userChannel, "Now playing: %s - %s (album: %s)" % (artistName, trackName, albumName))


	def channel_commands(self, userNick, userChannel, userMessage): # searches through the sent message to see if it's actually a command
		if re.search("#", userChannel, re.I): # makes sure there's actually a # in userChannel to make sure it's a channel
			if userChannel == "#bongrippez420":
				pass
			else:
				for x in self.channelCommands[userChannel]:
					if re.search(x, userMessage, re.I): #searches for commands in the user message
						self.ircConnection.send_message(userChannel, self.channelCommands[userChannel].get(x)) # gives sendMessage the channel to send to and what message

				for x in self.channelExecs[userChannel]:
					if re.search(x, userMessage, re.I):
						exec(self.channelExecs[userChannel].get(x))

				for x in self.channelTriggers[userChannel]:
					if re.search(x, userMessage, re.I):
						self.ircConnection.send_message(userChannel, self.channelTriggers[userChannel].get(x))

	def main(self):
		self.load_channels()
		self.load_commands()
		
		self.ircConnection = irc.ircConnection() # starts instance of ircConnection

		self.ircSock = self.ircConnection.connect("199.9.253.210", 6667) # connects to twitch.tvs IRC server

		self.authed = self.ircConnection.auth(self.botNick, self.botPassword) # auths with the IRC server

		if self.ircSock: # if it can connect
			if self.authed: # if it has authed
				for x in self.channelsToJoin: # joins every channel specified in channels.txt
					x = multiprocessing.Process(target=self.ircConnection.join_channel, args=(x,))
					x.start()
					x.join()

				while self.authed: # while its authed, do a bunch of shit like look for messages
					self.ircMessage = self.ircConnection.get_irc_messages()

					if len(self.ircMessage) == 0:
						print "Disconnected?"
						break

					if self.ircMessage.find('PING ') != -1:
						self.ircSock.send('PING :PONG \n')

					if self.ircMessage.find(" PRIVMSG ") != -1:
						self.userNick = self.ircMessage.split("!")[0][1:]
						self.userMessage = self.ircMessage.split(" PRIVMSG ")[-1].split(' :')[1].lower()
						self.userChannel = self.ircMessage.split(" PRIVMSG ")[1].split(" :")[0].lower()

						print "%s (%s): %s" % (self.userNick, self.userChannel, self.userMessage)

						self.channel_commands(self.userNick, self.userChannel, self.userMessage)

x = bot()
x.main()
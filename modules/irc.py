#!/usr/bin/env python
import socket, sys, traceback

class ircConnection:
	def __init__(self):
		print "irc.py loaded" # well, I don't know what this does

	def connect(self, server, port):
		self.ircSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # defines a new socket
		try: # tries to connect to server and port it is given, if it manages to do so returns true
			self.ircSock.connect((server, port))
			return self.ircSock
			return True

		except: # if there's a problem this guy takes care of it by printing the error and returning false so the bot doesnt keep trying or whatever
			print sys.exc_info()[0] #prints the exception class
			print sys.exc_info()[1] #prints the error message
			print repr(traceback.format_tb(sys.exc_info()[2])) #prints the stack

			return False

	def auth(self, botNickname, botPassword):
		try: # sends authing info
			self.ircSock.send("Pass %s\n" % (botPassword))			
			self.ircSock.send("NICK %s\n" % (botNickname))

			return True
		except:
			print sys.exc_info()[0] #prints the exception class
			print sys.exc_info()[1] #prints the error message
			print repr(traceback.format_tb(sys.exc_info()[2])) #prints the stack

			return False

	def get_irc_messages(self): # recieves messages 
			self.ircMessage = self.ircSock.recv(1024)
			self.ircMessage = self.ircMessage.strip("\r\n")
			return self.ircMessage

	def join_channel(self, channelName): # joins channels
		try:
			self.ircSock.send("JOIN %s\n" % (channelName))
			print "Joined %s" % (channelName)

		except:
			print sys.exc_info()[0] #prints the exception class
			print sys.exc_info()[1] #prints the error message
			print repr(traceback.format_tb(sys.exc_info()[2])) #prints the stack

	def send_message(self, channelName, message): # sends specified message to specified channel
			self.ircSock.send('PRIVMSG %s :%s\n' % (channelName, message)) 
			print "Sent \"%s\" to \"%s\"" % (message, channelName)
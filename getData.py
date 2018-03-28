import numpy as np
import urllib.parse
import urllib.request
import json
import time
import datetime
import os
import sys
sys.path.append("./messenger.py")
sys.path.append("./main.py")
from params import Params
from messenger import message #message and number
import random
import decimal

class GetData(Params):
	def __init__(self):
		Params.__init__(self)
		self.PrivateUrl = "https://poloniex.com/tradingApi" #base url for private API methods
		self.nonce = None
		self.repeat = False #if it is true: the downloading cycle repeates, it is meant for requests with erros
		self.numberOfRepeats = 0 
		self.maxNumberOfRepeats = 10 #max number of attemps of same reuests

	#PUBLIC METHODS
	def scrape(self,command,info={}):
		PublicMethods = ["returnTicker","returnOrderBook","returnTradeHistory","returnChartData","returnCurrencies","returnLoanOrders"]
		if command not in PublicMethods:
			print("ERROR 1")
			return 
		params = urllib.parse.urlencode(info) #Encode url paramenters to url style from dictionary
		# print("https://poloniex.com/public?command="+command+"&"+params+"")
		try:
			ret = urllib.request.urlopen("https://poloniex.com/public?command="+command+"&"+params+"",timeout=15).read() #Actual request to server here
		except:
			self.repeat = True
			print("ERROR 3")
		ret = ret.decode("utf8")
		return json.loads(ret) #converts to json

	#API COMMANDS

	def returnOrderBook(self,pair,depth): 
		#Returns the order book for a given market, as well as a sequence number for use with the Push API
		# and an indicator specifying whether the market is frozen. You may set currencyPair to "all" to get the order books of all markets 
		return self.scrape("returnOrderBook",info={"currencyPair":pair,"depth":depth})

	def returnTradeHistory(self,pair,start=None,end=None): #start and end are unix timestamps
		info = {}
		if type(start) != type(end):
			print("ERROR 2")
			return
		
		elif start != None and end != None: #if the dates are defined
			info["start"] = start
			info["end"] = end

		info["currencyPair"] = pair
		data = self.scrape("returnTradeHistory",info)
		if len(data) == 50000: #recursively breaks dates down until the range is small enough to fit all trades
			print("WARNING 1")
			diff = end-start
			dates1 = [start,start+int((diff)/2)] #INCLUSIVE INFORMATION
			dates2 = [dates1[1]+1,end]
			return self.returnTradeHistory(pair,start=dates1[0],end=dates1[1]) + self.returnTradeHistory(pair,start=dates2[0],end=dates2[1])
		return data
	#-----------------------------

	def dateUnix(x):
		date = x["date"]	 
		date = time.strptime(date, "%Y-%m-%d %H:%M:%S")
		date = datetime.fromtimestamp(time.mktime(date))
		date = date.timestamp()
		return int(date)


	def downloadTrades(self,start): #End is the current day rounded down.
		try:
			files = os.listdir(self.dataPath)

		except FileNotFoundError:
			print("File Not Found")
			message("File Not Found")
			return "FINISHED downloadTrades"

		end = int(time.time())
		#86400 is the number of seconds in one day
		end -= int(end % 86400) #rounds the time down to start of day
		start -= int(start % 86400)
		assert(start != end), "Invalid Start Date"
		dates = [x for x in range(start,end,86400)]
		total = len(self.currencyPairs)*len(dates)
		counter = 1
		dates.pop(0) #becuase start is calculated by subtracting from date
		try:
			for pair in self.currencyPairs:
				for date in dates:
					counter += 1
					start = date - 86400
					end  = date
					title = (pair + "_" + str(start) + "-" + str(end))

					if title in files: #file already exists
						continue
					print(counter/total,time.time())
					try:
						# time.sleep(random.uniform(.,1.317))
						data = self.returnTradeHistory(pair,start=start,end=end)
					except:
						message("An eror occured fetching data")

					with open(self.dataPath+title, "w") as file:
						json.dump(data,file)
					print("loc " + self.dataPath + title)	
		except:
			print("An error occured in downloading trades")
			message("An error occured in downloading trades")
			self.repeat = True

		if self.repeat == True :
			print("Repeating")
			self.numberOfRepeats += 1
			self.repeat = False
			if self.numberOfRepeats > self.maxNumberOfRepeats:
				self.repeat = False
				self.numberOfRepeats = 0
				print("REPEAT HAS FAILED")
				message("REPEAT HAS FAILED")
				return ("FINISHED downloadTrades")

			message("Repeating " + self.getTimestamp())
			self.downloadTrades(start)

		print("Downloaded A trade")
		return ("FINISHED downloadTrades")


	def getTimestamp(self): #gets an English timestamp (can be understood by a 👤)
		time = datetime.datetime.now()
		timestamp = "day is " + str(time.day) + " hour is " + str(time.hour) + " min is " + str(time.minute)
		return timestamp



	def downloadAll(self,start): #Downloads continueously 
		try:
			while True:
				if int(datetime.datetime.now().hour) == 14: # 2 AM
					note = "Started Downloading " + self.getTimestamp()
					message(note)
					print(note)
					self.downloadTrades(self.dataPath,start)
					note = "Finished Downloading " + self.getTimestamp()
					message(note)
					print(note)
					time.sleep(76400) #A bit then One day - 1 hour
				time.sleep(3600)

		except:
			print("THE CODE HAS BROKEN " + self.getTimestamp())
			message("THE CODE HAS BROKEN " + self.getTimestamp())
			return 


# GetData().downloadAll("/Volumes/DanielDrive/cryptoData/",start=1483228800)
GetData().downloadTrades(start=int(time.time())  - (86400*30))
import datetime
from datetime import datetime
import os
import json
import time
import numpy as np
import pandas as pd
import numpy as np

#DEPRICATED, REPLACED BY READ DATA
class InterpretData(object):
	def __init__(self):
		self.currencyPairs = ["BTC_AMP","BTC_ARDR","BTC_BCN","BTC_BCY","BTC_BELA","BTC_BLK","BTC_BTCD","BTC_BTM","BTC_BTS","BTC_BURST","BTC_CLAM","BTC_DASH","BTC_DCR","BTC_DGB",
			"BTC_DOGE","BTC_EMC2","BTC_ETC","BTC_ETH","BTC_EXP","BTC_FCT","BTC_FLDC","BTC_FLO","BTC_GAME","BTC_GNO","BTC_GNT","BTC_GRC","BTC_HUC","BTC_LBC",
			"BTC_LSK","BTC_LTC","BTC_MAID","BTC_NAV","BTC_NEOS","BTC_NMC","BTC_NXC","BTC_NXT","BTC_OMNI","BTC_PASC","BTC_PINK","BTC_POT",
			"BTC_PPC","BTC_RADS","BTC_REP","BTC_RIC","BTC_SBD","BTC_SC","BTC_STEEM","BTC_STR","BTC_STRAT","BTC_SYS","BTC_VIA","BTC_VRC","BTC_VTC",
			"BTC_XBC","BTC_XCP","BTC_XEM","BTC_XMR","BTC_XPM","BTC_XRP","BTC_XVC","BTC_ZEC","ETH_ETC","ETH_GNO","ETH_GNT","ETH_LSK","ETH_REP","ETH_STEEM",
			"ETH_ZEC","USDT_BTC","USDT_DASH","USDT_ETC","USDT_ETH","USDT_LTC","USDT_NXT","USDT_REP","USDT_STR","USDT_XMR","USDT_XRP","USDT_ZEC","XMR_BCN",
			"XMR_BLK","XMR_BTCD","XMR_DASH","XMR_LTC","XMR_MAID","XMR_NXT","XMR_ZEC"]
		#self.path = "/Users/DanielLongo/Desktop/cryptoCurrency/src/cryptoData/rawCryptoData/"
		#self.start = 1514073600
		#self.end = 1514160000
		self.path = "/Users/DanielLongo/Desktop/CryptoRnn/cryptoData/"
		self.start = 1521590400
		self.end = 1521676800
		self.interval = 600 #interval is the time ampunt at which trades are grouped
		self.PPE = 20 #periods per example
		self.ExPerBatch = 2 #examples per batch

	def fetchArray(self,pair): #fetches json files with trade data for specific periods of time
		final = []
		if (self.start % 86400 != 0) or (self.end % 86400 != 0):
			print("error, invalid start and end dates in fetchArray")
			return None
		dates = [x for x in range(self.start,self.end,86400)]
		for date in dates:
			start = date
			end = date + 86400
			fileName = self.path + pair + "_" + str(start) + "-" + str(end)
			try:
				final += json.load(open(fileName))
			except FileNotFoundError:
				print(fileName)
				print("invalid path")
		return final

	#start of old code :
	def normalizeExamples(self,examples): #normalizes examples to percent of  mac by column
		for example in examples:
			example = example.T/example.max(axis=1)
			example = example.T
			for item in example:
				for thing in item:
					if np.isnan(thing) == True:
						thing = 0
		return examples


	def getExamples(self,data,stagTrue):
		examples = []
		if stagTrue:
			data = np.delete(data,0,axis=0)
		else:
			data = np.delete(data,-1,axis=0)
		remainder = len(data) % self.PPE
		for start in range(0,len(data)-remainder,self.PPE): #excludes remanders
			end = start + self.PPE
			adding = np.squeeze([data[start:end]])
			if stagTrue:
				adding = [(adding)[-1]]
			examples += [adding]
		# if stagTrue:
		# 	return examples[-1]

		return examples

	def getBatches(self,examples):
		batches = []
		reamainder = len(examples) % self.ExPerBatch
		for start in range(0,len(examples)-reamainder,self.ExPerBatch):
			end = start + self.ExPerBatch
			batches += [examples[start:end]]
		return batches

	def concatenate(self,a,b,axis=1): #a is final b is the adding data
		if a is None:
			##print('None')
			return b
		if b is None:
			##print("NONE")
			return a
	   # ###print("concatenate",np.shape(a),np.shape(b))
		##print("The Shapes of concatenate",np.shape(a),np.shape(b))
		##print("Following",np.shape(np.concatenate((a,b),axis=axis)))
		return np.concatenate((a,b),axis=axis)

	def dateUnix(self,x):
		date = x["date"]
		date = time.strptime(date, "%Y-%m-%d %H:%M:%S")
		date = datetime.fromtimestamp(time.mktime(date))
		date = date.timestamp()
		return int(date)

	def process_IB(self,data): #takes in data of one pair for one day, time interval is in seconds
		data = sorted(data,key=self.dateUnix)
		final = [[1,1,1,1,1,1,1,1,1,1]] #final is a list of lists
		
		start = self.dateUnix(data[0])
		#end = self.dateUnix(data[-1])
		#dateRanges = [(x,x+time_interval) for x in range(start,end,time_interval)]
		location = 0
		whichDates = 0
		ending = start
		endingNow = False
		while True:
			#start,end = dateRanges[whichDates] 
			ending += self.interval
			add = {"type":[],"rate":[],"total":[],"volume":0}
			while True:
				try:
					adding = data[location]
				except IndexError:
					endingNow = True #this means we have gone through all the lines and now want to return final
					break
				if self.dateUnix(adding) >= ending:
					break

				if adding["type"] == "buy":
					add["type"] += [1*float(adding["amount"])]
				if adding["type"] == "sell":
					add["type"] += [-1*float(adding["amount"])]

				add["rate"] += [float(adding["rate"])]
				add["total"] += [float(adding["total"])]
				add["volume"] += 1

				location += 1
			
			if add["type"] == []:
				final += [[ending,-404,-404,-404,-404,-404,-404,-404,-404,-404]]
				###print(np.shape([[ending,0,0,0,0,0,0,0,0]]))
				if endingNow == True:
					return final
				continue
			#This parts adds new features to add 
			add["rate_sd"] = np.std(add["rate"]) #returns volitility of prices
			add["total_sd"] = np.std(add["total"]) #returns volitility of order sizes
			add["last_rate"] = (add["rate"])[-1] #retuns the last rate 
			add["last_types"] = sum(add["type"][-5:-1] + [add["type"][-1]]) #returns the last 4 types of trades
			#This part configures pre-existing features of add
			add["rate"] = sum(add["rate"])/len(add["rate"]) #retuns the average rate
			add["avg_total"] = sum(add["total"])/len(add["total"]) #returns the average order size
			add["total"] = sum(add["total"]) #retuns the total sum of trades
			add["type"] = sum(add["type"]) #retunrs whether there were more buys + or sells - and by how much

			final += [[ending/(10**10),add["type"],add["rate"],add["total"],add["volume"],add["rate_sd"],add["avg_total"],add["total_sd"],add["last_rate"],add["last_types"]]]
			#["End Timestamp","Average type",Average Rate","Total Amount Traded","Number of Trades","Volitility of Rates","Volitility of Order Sizes","Average Order Size","The Last Rate","Last 4 Types of Trades"]
			###print(np.shape([[ending,add["type"],add["rate"],add["total"],add["volume"],add["rate_sd"],add["total_sd"],add["last_rate"],add["last_types"]]]))
			###print("THIS IS HERE",np.shape(final))
			if endingNow == True:
				###print(np.shape(final))
				final.pop(0)
				##print(np.shape(final))
				##print(final[1])
				return final

	# end of old code :)

	def processArray(self,data): #takes an array of dicts and coverts to array with scalars
		final = []
		if data == []:
			##print("No data avalible in processArray")
			return None

		data = self.process_IB(data) #collapses data into one large numpy array
		examplesX = self.getExamples(data,False)
		examplesY = self.getExamples(data,True)

		#print("examples X",np.shape(examplesX))
		#print("examples Y",np.shape(examplesY))

		# #print(np.shape(examplesX),"Examples X shape")
		examplesX = self.normalizeExamples(np.squeeze(examplesX))

		#print(np.shape(examplesX))
		# #print(np.shape(examplesX),"shape of examplesX")
		batchesX = np.squeeze(self.getBatches(examplesX))
		batchesY = np.squeeze(self.getBatches(examplesY))

		#print("batchesX",np.shape(batchesX))
		#print("BatchesY",np.shape(batchesY))

		# #print(np.shape(batchesX),"Batches X shape")
		# #print(np.shape(batchesX), "shape of batchesY")

		# ##print(np.shape(batchesX))
		# ##print(np.shape(batchesY))

		# ##print(np.shape(final))

		return (batchesX,batchesY)

	def createBatches(self): #the main function of the class
		finalX = None
		finaly = None
		for pair in self.currencyPairs:
			##print("PAIR:",pair)
			data = self.fetchArray(pair)
			if data == []:
				#print("Pair invalid: " + pair)
				continue
			# #print(np.shape(data))
			X,y = self.processArray(data)
			##print("Adding",np.shape(X),np.shape(y),pair)
			##print("final",np.shape(finalX),np.shape(finaly))
			print("shape of X:",np.shape(X),np.shape(finalX))
			print("shape of y:",np.shape(y),np.shape(finaly))
			finalX,finaly = self.concatenate(X,finalX,axis=3),self.concatenate(y,finaly,axis=2)
			#print('djakldja',np.shape(finalX),np.shape(finaly))
			# #print((np.shape(finalX)))

		##print("Final",np.shape(finalX),np.shape(finaly))

		# #print(np.shape(self.getBatches(finalX)))
		#print('FINALANALNALNALNA',np.shape(finalX),np.shape(finaly))
		print("shape of finalX:",np.shape(finalX))
		print("shape of finalY:",np.shape(finaly))

		return zip(finalX,finaly)


# InterpretData().processArray(InterpretData().fetchArray("ETH_ETC"))
InterpretData().createBatches()
# InterpretData().process_IB(InterpretData().fetchArray("ETH_ETC"))

# class InterpretData(object):
# 	def __init__(self):
# 		self.currencyPairs = ["BTC_AMP","BTC_ARDR","BTC_BCN","BTC_BCY","BTC_BELA","BTC_BLK","BTC_BTCD","BTC_BTM","BTC_BTS","BTC_BURST","BTC_CLAM","BTC_DASH","BTC_DCR","BTC_DGB",
# 			"BTC_DOGE","BTC_EMC2","BTC_ETC","BTC_ETH","BTC_EXP","BTC_FCT","BTC_FLDC","BTC_FLO","BTC_GAME","BTC_GNO","BTC_GNT","BTC_GRC","BTC_HUC","BTC_LBC",
# 			"BTC_LSK","BTC_LTC","BTC_MAID","BTC_NAV","BTC_NEOS","BTC_NMC"SJ,"BTC_NXC","BTC_NXT","BTC_OMNI","BTC_PASC","BTC_PINK","BTC_POT",
# 			"BTC_PPC","BTC_RADS","BTC_REP","BTC_RIC","BTC_SBD","BTC_SC","BTC_STEEM","BTC_STR","BTC_STRAT","BTC_SYS","BTC_VIA","BTC_VRC","BTC_VTC",
# 			"BTC_XBC","BTC_XCP","BTC_XEM","BTC_XMR","BTC_XPM","BTC_XRP","BTC_XVC","BTC_ZEC","ETH_ETC","ETH_GNO","ETH_GNT","ETH_LSK","ETH_REP","ETH_STEEM",
# 			"ETH_ZEC","USDT_BTC","USDT_DASH","USDT_ETC","USDT_ETH","USDT_LTC","USDT_NXT","USDT_REP","USDT_STR","USDT_XMR","USDT_XRP","USDT_ZEC","XMR_BCN",
# 			"XMR_BLK","XMR_BTCD","XMR_DASH","XMR_LTC","XMR_MAID","XMR_NXT","XMR_ZEC"]
# 		self.path = "/Users/DanielLongo/Desktop/rawCryptoData/"

# 	def readDataToArray(self,start):#reads data to numpy.array(len(currencyParis by number of examples for each)) 
# 		final = []
# 		end = int(time.time())
# 		end -= int(end % 86400) #rounds the time down to start of day
# 		start -= int(start % 86400)
# 		dates = [x for x in range(start,end,86400)] 
# 		for pair in self.currencyPairs:
# 			##print(pair)
# 			add = []
# 			for date in dates:
# 				start = date - 86400
# 				end  = date
# 				title = (pair + "_" + str(start) + "-" + str(end))
# 				path = self.path + title
# 				try:
# 					file = open(path,"r")
# 					add += json.load(file)
# 				except FileNotFoundError:
# 					##print("FileNotFoundError")



# InterpretData().readDataToArray(1512000000)



import datetime
from datetime import datetime
import os
import json
import time
import numpy as np
import pandas as pd
import numpy as np
import sys
sys.path.append("./messenger.py")
sys.path.append("./main.py")
from main import CryptoRnn

class ReadData(CryptoRnn):
	def __init__(self):
		CryptoRnn.__init__(self)

	def fetchArray(self,pair): #fetches json files with trade data for specific periods of time
		final = []
		if (self.start % 86400 != 0) or (self.end % 86400 != 0):
			print("error, invalid start and end dates in fetchArray")
			return None
		dates = [x for x in range(self.start,self.end,86400)]
		for date in dates:
			start = date
			end = date + 86400
			fileName = self.dataPath + pair + "_" + str(start) + "-" + str(end)
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
			return b
		if b is None:
			return a
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
		location = 0
		whichDates = 0
		ending = start
		endingNow = False
		while True:
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
			
			if endingNow == True:
				final.pop(0)
				return final

	# end of old code :)

	def processArray(self,data): #takes an array of dicts and coverts to array with scalars
		final = []

		if data == []:
			return None

		data = self.process_IB(data) #collapses data into one large numpy array
		examplesX = self.getExamples(data,False)
		examplesY = self.getExamples(data,True)
		examplesX = self.normalizeExamples(np.squeeze(examplesX))

		batchesX = np.squeeze(self.getBatches(examplesX))
		batchesY = np.squeeze(self.getBatches(examplesY))

		assert(len(batchesX.shape) == 4), "BatchesX shape error " + str(batchesX.shape) + " try changing ExPerBatch. Shape should be 4D"
		assert(len(batchesY.shape) == 3), "BatchesY shape error " + str(batchesY.shape) + " try changing ExPerBatch. Shape should be 3D"
		return (batchesX,batchesY)

	def createBatches(self): #the main function of the class
		print("Creating Batches")
		finalX = None
		finaly = None
		for pair in self.currencyPairs:
			data = self.fetchArray(pair)
			if data == []:
				continue
			X,y = self.processArray(data)
			finalX,finaly = self.concatenate(X,finalX,axis=3), self.concatenate(y,finaly,axis=2)
		print("shape of finalX:",np.shape(finalX))
		print("shape of finalY:",np.shape(finaly))
		print("Batches Created")

		return zip(finalX,finaly)

ReadData().createBatches()
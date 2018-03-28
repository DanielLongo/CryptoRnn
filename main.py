import os
import sys
# sys.path.append("./params.py")
from params import Params

# sys.path.append("./readData.py")
from readData import ReadData

# sys.path.append("./RNN.py")
from RNN import Rnn

class CryptoRnn(ReadData,Rnn):
	def __init__(self):
		# Params.__init__(self)
		ReadData.__init__(self)
		Rnn.__init__(self)

	def checkData(self): #ensures there is data for start and end dates
		files = os.listdir(self.dataPath)
		startDates = []
		endDates = []
		for fileName in files:
			dates = fileName.split("_")[-1]
			startDate, endDate = dates.split("-")[0],dates.split("-")[1]
			startDates += [int(startDate)]
			endDates += [int(endDate)]
		# print("start dates",startDates)
		assert(self.start in startDates), "Data Does not have start date: " + str(self.start)
		#assuming we don't grab data for end day, TODO: need to ensure this is true
		assert(self.end in endDates), "Data Does not have end date: " + str(self.end)
		print("Data Succesfully checked")
	
	def build(self):
		self.checkData()
		self.batches = list(self.createBatches())
		self.buildRnn()
		self.rnn()
		shuffle(self.batches)



def main():
	print("Started Main :O")
	CryptoRnn().build()
	print("Finished Main ;)")

main()


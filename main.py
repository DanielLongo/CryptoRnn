import os 
class CryptoRnn(object):
	def __init__(self):
		self.key = "5GC8VYTZ-3LMAY2RT-RGMBKY88-FUBL52D1" #change
		self.secret = "6b8d51e9e2fdcd24bb1a4482ae6f539bd1fd10b21405b0c3ffb75d2dedf924f4447501f4324c77f2434c572dcd41cb1fdf3037fc91ccf603fa74720264c31cfa"
		self.currencyPairs = ["BTC_AMP","BTC_ARDR","BTC_BCN","BTC_BCY","BTC_BELA","BTC_BLK","BTC_BTCD","BTC_BTM","BTC_BTS","BTC_BURST","BTC_CLAM","BTC_DASH","BTC_DCR","BTC_DGB",
			"BTC_DOGE","BTC_EMC2","BTC_ETC","BTC_ETH","BTC_EXP","BTC_FCT","BTC_FLDC","BTC_FLO","BTC_GAME","BTC_GNO","BTC_GNT","BTC_GRC","BTC_HUC","BTC_LBC",
			"BTC_LSK","BTC_LTC","BTC_MAID","BTC_NAV","BTC_NEOS","BTC_NMC","BTC_NXC","BTC_NXT","BTC_OMNI","BTC_PASC","BTC_PINK","BTC_POT",
			"BTC_PPC","BTC_RADS","BTC_REP","BTC_RIC","BTC_SBD","BTC_SC","BTC_STEEM","BTC_STR","BTC_STRAT","BTC_SYS","BTC_VIA","BTC_VRC","BTC_VTC",
			"BTC_XBC","BTC_XCP","BTC_XEM","BTC_XMR","BTC_XPM","BTC_XRP","BTC_XVC","BTC_ZEC","ETH_ETC","ETH_GNO","ETH_GNT","ETH_LSK","ETH_REP","ETH_STEEM",
			"ETH_ZEC","USDT_BTC","USDT_DASH","USDT_ETC","USDT_ETH","USDT_LTC","USDT_NXT","USDT_REP","USDT_STR","USDT_XMR","USDT_XRP","USDT_ZEC","XMR_BCN",
			"XMR_BLK","XMR_BTCD","XMR_DASH","XMR_LTC","XMR_MAID","XMR_NXT","XMR_ZEC"]
		self.dataPath = "/Users/DanielLongo/Desktop/CryptoRnn/cryptoData/"
		self.start = 1521590400
		self.end = 1521676800
		self.interval = 600 #interval is the time ampunt at which trades are grouped
		self.PPE = 20 #periods per example
		self.ExPerBatch = 2 #examples per batch

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


def main():
	print("Started :0")
	CryptoRnn().build()
	print("Finished ;)")

#main()




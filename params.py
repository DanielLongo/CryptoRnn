import os

class Params():
	def __init__(self):
		self.key = ""
		self.secret = ""
		self.currencyPairs = ["BTC_AMP","BTC_ARDR"]#,"BTC_BCN","BTC_BCY","BTC_BELA","BTC_BLK","BTC_BTCD","BTC_BTM","BTC_BTS","BTC_BURST","BTC_CLAM","BTC_DASH","BTC_DCR","BTC_DGB",
			# "BTC_DOGE","BTC_EMC2","BTC_ETC","BTC_ETH","BTC_EXP","BTC_FCT","BTC_FLDC","BTC_FLO","BTC_GAME","BTC_GNO","BTC_GNT","BTC_GRC","BTC_HUC","BTC_LBC",
			# "BTC_LSK","BTC_LTC","BTC_MAID","BTC_NAV","BTC_NEOS","BTC_NMC","BTC_NXC","BTC_NXT","BTC_OMNI","BTC_PASC","BTC_PINK","BTC_POT",
			# "BTC_PPC","BTC_RADS","BTC_REP","BTC_RIC","BTC_SBD","BTC_SC","BTC_STEEM","BTC_STR","BTC_STRAT","BTC_SYS","BTC_VIA","BTC_VRC","BTC_VTC",
			# "BTC_XBC","BTC_XCP","BTC_XEM","BTC_XMR","BTC_XPM","BTC_XRP","BTC_XVC","BTC_ZEC","ETH_ETC","ETH_GNO","ETH_GNT","ETH_LSK","ETH_REP","ETH_STEEM",
			# "ETH_ZEC","USDT_BTC","USDT_DASH","USDT_ETC","USDT_ETH","USDT_LTC","USDT_NXT","USDT_REP","USDT_STR","USDT_XMR","USDT_XRP","USDT_ZEC","XMR_BCN",
			# "XMR_BLK","XMR_BTCD","XMR_DASH","XMR_LTC","XMR_MAID","XMR_NXT","XMR_ZEC"]
		# self.dataPath = "/Users/DanielLongo/Desktop/CryptoRnn/cryptoData/"
		self.dataPath = "../cryptoData/"

		# self.start = 1521590400
		self.end = 1521676800
		self.start = self.end - (86400*2)

		self.interval = 600 #interval is the time ampunt at which trades are grouped
		self.PPE = 24 #periods per example
		self.ExPerBatch = 4 #examples per batch
		self.sequence_length = 10 # len(time)
		self.batches = []
		#RNN Params
		
		self.epoch = 100
		self.learningRate = .000005
		self.state_size = 200 # depth of rnn number of hidden layers 


# def x():
	# print("x")
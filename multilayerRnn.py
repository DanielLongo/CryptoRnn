import tensorflow as tf
from tensorflow.contrib import rnn
import sys
sys.path.append("./params.py")
from params import Params
from time import strftime, gmtime
import numpy as np
from random import shuffle 

# to reference drop out rnn.DropoutWrapper

class MultilayerRnn(object):
	def __init__(self):
		Params.__init__(self)
		self.number_of_pairs = len(self.currencyPairs)
		self.epochCounter = 0 #counts for tensorboard
		self.logs_path = 'tensorboard/'+strftime("%Y_%m_%d_%H_%M_%S",gmtime()) #filename for tensorboard

	def initializeVariables(self):
		rnn_layers = [rnn.BasicLSTMCell(self.state_size) for _ in range(self.num_layers)]
		self.multi_rnn_cell = rnn.MultiRNNCell(rnn_layers)



	def propagate(self):
		input_placeholder = tf.placeholder(tf.float32, [None, None, 28])
		outputs, state = tf.nn.dynamic_rnn(self.multi_rnn_cell, inputs=input_placeholder, dtype=tf.float32)
		final_output = outputs[-1]
		print("Shape of final output", final_output.shape)


	def multilayerRnn(self):
		self.initializeVariables()
		sess = tf.Session()
		init = tf.global_variables_initializer()
		sess.run(init)
		assert(self.batches != []), "Batches = []"

		self.train_writer = tf.summary.FileWriter(self.logs_path+'/train',sess.graph) #creates a summary path for files 
		self.epochCounter = 0

		for i in range(self.epoch):
			for batchX, batchY in self.batches:
				self.epochCounter += 1
				print("Shape of batch Y",np.shape(batchY),"Shape of batch X",np.shape(batchX))
				self.propagate(batchX)


print("Finsihed")


import tensorflow as tf
import sys
sys.path.append("./params.py")
from params import Params
from time import strftime, gmtime
import numpy as np
from random import shuffle 
#tensorboard --logdir=path/to/directory
#		tf.reset_default_graph()

class Rnn(object):
	def __init__(self):
		Params.__init__(self)
		self.number_of_pairs = len(self.currencyPairs)
		# self.Spred = None unesessary?
		self.epochCounter = 0 #counts for tensorboard
		self.logs_path = 'tensorboard/'+strftime("%Y_%m_%d_%H_%M_%S",gmtime())
		
	def add_placeholders(self):
		self.input_placeholder = tf.placeholder(tf.float32, (self.ExPerBatch, self.PPE, self.number_of_pairs*self.sequence_length))
		self.labels_placeholder = tf.placeholder(tf.float32, (self.ExPerBatch, 1, self.number_of_pairs*self.sequence_length))

	def create_feed_dict(self,inputs_batch,labels_batch = None):
		feed_dict = {}
		feed_dict[self.input_placeholder] = inputs_batch
		feed_dict[self.labels_placeholder] = labels_batch
	 #   print("Here",np.shape(self.input_placeholder),np.shape(inputs_batch))
#		print(feed_dict[self.input_placeholder])
		return feed_dict

	def add_prediction_op(self):
		# basic_cell = tf.nn.rnn_cell.BasicRNNCell(self.state_size)
		lstm_cell = tf.contrib.rnn.LSTMCell(self.state_size)
		# rnn_cell = tf.contrib.rnn.MultiRNNCell([tf.contrib.rnn.BasicLSTMCell(self.state_size),tf.contrib.rnn.BasicLSTMCell(self.state_size)]) 
		xavier = tf.contrib.layers.xavier_initializer()
		W = tf.get_variable('Weights',(self.state_size,self.number_of_pairs*10), initializer = xavier)
		B = tf.get_variable('Biasis',(1,self.number_of_pairs*10))
		Output,State = tf.nn.dynamic_rnn(lstm_cell,self.input_placeholder,dtype= tf.float32)
		# Output,State = tf.nn.dynamic_rnn(rnn_cell,self.input_placeholder,dtype= tf.float32)
		print("HIHHIIIIIIIIHHHHHHHH")
		print("Output",Output.shape)
		print("State",State.shape)
		State = State[1] # 0 = initial state, 1 = the final
		self.State = State
		self.Spred = tf.matmul(State,W) + B
		return self.Spred

	def add_loss_op(self,preds):
		Diff = (tf.subtract(self.labels_placeholder,preds))
		batch_loss = tf.sqrt(tf.reduce_sum(tf.square(Diff),axis=1))
		mean_loss = tf.reduce_mean(batch_loss)
		return mean_loss


	def add_training_op(self,loss):
		train_op = tf.train.AdamOptimizer(learning_rate=self.learningRate).minimize(loss)
		self.trains = train_op
		return train_op

	def train_on_batch(self,sess,inputs_batch,labels_batch):
		feed = self.create_feed_dict(inputs_batch,labels_batch=labels_batch)
		_, loss,summary = sess.run([self.train_op,self.loss_op,self.merged_summary_op],feed_dict=feed)	   
		self.train_writer.add_summary(summary,self.epochCounter)
		self.train_writer.flush()
		# print("spred",self.Spred.eval(session=sess,feed_dict=feed).shape)
		# print("loss",self.loss.eval(session=sess,feed_dict=feed))
		# print("labels",self.labels_placeholder.eval(session=sess,feed_dict=feed))
		# print("final rnn state",self.State.eval(session=sess,feed_dict=feed).shape)
		print("trains",self.trains)
		return loss

	# def evalidateBatch(inputs_batch,labels_batch):
	# 	feed_dict = self.create_feed_dict(inputs_batch,labels_batch)
	# 	_, loss,summary = sess.run([self.train_op,self.loss_op,self.merged_summary_op],feed_dict=feed)
	# 	predicted = self.Spred.eval(session=sess,feed_dict=feed)
	# 	actual = self.labels_placeholder.eval(session=sess,feed_dict=feed)
	# 	Diff = (tf.subtract(actual,predicted))
	# 	batch_losses = tf.sqrt(tf.reduce_sum(tf.square(Diff),axis=1))
	# 	print("batches_loss", batch_losses)
	# 	#mean_loss = tf.reduce_mean(batch_loss)
	# 	return batch_losses

	def buildRnn(self):
		self.add_placeholders()
		self.pred = self.add_prediction_op()
		self.loss_op = self.add_loss_op(self.pred)
		self.train_op = self.add_training_op(self.loss_op)
		tf.summary.scalar('Loss', self.loss_op)
		self.merged_summary_op = tf.summary.merge_all()
		print("The model has been built")

	def rnn(self):
		sess = tf.Session()
		### if load != '':
		### 	saver = tf.train.import_meta_graph('./tesT.meta')
		### 	saver.restore(sess,'./tesT')
		
		#batches = list(InterpretData().createBatches())
		# shuffle(batches)
		init = tf.global_variables_initializer()
		sess.run(init) #initializes all global variables

		assert(self.batches != []), "Batches = []"

		self.train_writer = tf.summary.FileWriter(self.logs_path+'/train',sess.graph) #creates a summary path for files 

		self.epochCounter = 0
		for i in range(self.epoch):
			for batchX, batchY in self.batches:
				self.epochCounter += 1
				batchY = batchY.reshape((self.ExPerBatch,1,self.number_of_pairs*self.sequence_length))
				print(np.shape(batchX),np.shape(batchY),"HERERERERERERERR")
				print("loss",self.train_on_batch(sess,batchX,batchY))
				print("variables",tf.trainable_variables())

		# saver0 = tf.train.Saver()
		# saver0.save(sess,"tesT")
		# saver0.export_meta_graph("tesT.meta")


# more data, with more batches per epoch
# try different optimizer 
# try larger learning rate
# if time: try different loss function 


# def main():
# 	model = Rnn()
# 	model.build()
# 	return model.rnn()

	

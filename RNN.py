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
		self.Spred = None # -1 is for no normalization
		self.epochCounter = 0 #counts for tensorboard
		self.logs_path = 'tensorboard/'+strftime("%Y_%m_%d_%H_%M_%S",gmtime())
		
	def add_placeholders(self):
		self.input_placeholder = tf.placeholder(tf.float32, (self.ExPerBatch, self.PPE, self.number_of_pairs*self.sequence_length))
		self.labels_placeholder = tf.placeholder(tf.float32, (self.ExPerBatch, self.number_of_pairs*self.sequence_length))

	def create_feed_dict(self,inputs_batch,labels_batch = None):
		feed_dict = {}
		feed_dict[self.input_placeholder] = inputs_batch
		#####if labels_batch != None:
		feed_dict[self.labels_placeholder] = labels_batch
	 #   print("Here",np.shape(self.input_placeholder),np.shape(inputs_batch))
#		print(feed_dict[self.input_placeholder])
		return feed_dict

	def add_prediction_op(self):
 #	   masked_input = tf.boolean_mask(self.input_placeholder,self.input_mask_placeholder)
		lstm_cell = tf.contrib.rnn.LSTMCell(self.state_size)
#		print(masked_input,self.input__placeholder)
		xavier = tf.contrib.layers.xavier_initializer()
		W = tf.get_variable('Weights',(self.state_size,self.number_of_pairs*10),initializer = xavier)
		B = tf.get_variable('Biasis',(1,self.number_of_pairs*10))
#	   Output,State = tf.nn.dynamic_rnn(lstm_cell,masked_input,dtype= tf.float32)
		Output,State = tf.nn.dynamic_rnn(lstm_cell,self.input_placeholder,dtype= tf.float32)
		State = State[1] # 0th is the initial state
		self.Spred = tf.matmul(State,W)+B
		print('Spred',self.Spred)
		return self.Spred

	def add_loss_op(self,preds):
 #	   masked_loss = tf.boolean_mask(preds,labels_masks_placeholder)
		print("labels",self.labels_placeholder)
		print("preds",preds)
		Diff = (tf.subtract(self.labels_placeholder,preds)) #############################
		batch_loss = tf.sqrt(tf.reduce_sum(tf.square(Diff),axis=1))
		mean_loss = tf.reduce_mean(batch_loss)
		print("mean_loss:",mean_loss)
		return mean_loss


	def add_training_op(self,loss):
		print("loss")
		train_op = tf.train.AdamOptimizer(learning_rate=self.learningRate).minimize(loss)
		return train_op

	def train_on_batch(self,sess,inputs_batch,labels_batch):
		feed = self.create_feed_dict(inputs_batch,labels_batch=labels_batch)
	   # print(self.Spred.eval(session=sess,feed_dict=feed))
		#print(self.labels_placeholder.eval(session=sess,feed_dict=feed))
		# 
		_, loss,summary = sess.run([self.train_op,self.loss_op,self.merged_summary_op],feed_dict=feed)	   
		self.train_writer.add_summary(summary,self.epochCounter)
		self.train_writer.flush()
		#print(self.Spred.eval(session=sess,feed_dict=feed))
		#print(self.labels_placeholder.eval(session=sess,feed_dict=feed))
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

		for i in range(self.epoch):
			self.epochCounter += 1
			for batchX, batchY in self.batches:
				print(self.train_on_batch(sess,batchX,batchY))


# more data, with more batches per epoch
# try different optimizer 
# try larger learning rate
# if time: try different loss function 


# def main():
# 	model = Rnn()
# 	model.build()
# 	return model.rnn()

	

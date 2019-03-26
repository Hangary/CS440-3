import numpy as np

class MultiClassPerceptron(object):
	def __init__(self,num_class,feature_dim):
		"""Initialize a multi class perceptron model.

		This function will initialize a feature_dim weight vector,
		for each class.

		The LAST index of feature_dim is assumed to be the bias term,
			self.w[:,0] = [w1,w2,w3...,BIAS]
			where wi corresponds to each feature dimension,
			0 corresponds to class 0.

		Args:
		    num_class(int): number of classes to classify
		    feature_dim(int): feature dimension for each example
		"""

		self.w = np.zeros((feature_dim+1,num_class))
		self.b = 1
		self.learning_rate = 0.8

	def train(self,train_set,train_label):
		""" Train perceptron model (self.w) with training dataset.

		Args:
		    train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
		    train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
		"""

		# YOUR CODE HERE
		num_train = train_set.shape[0]
		train_set_b = np.append(train_set, np.ones((num_train,1)), axis=1)
		epoch = 100
		decay = self.learning_rate/epoch
		for iteration in range(epoch):
			#predict_matrix = np.matmul(train_set_b,self.w)
			for i in range(num_train):
				f = train_set_b[i,:]
				predict_label = np.argmax(np.matmul(f.T,self.w))
				#predict_label = np.argmax(predict_matrix[i,:])
				true_label = train_label[i]
				if predict_label != true_label:
					self.w[:,true_label] += self.learning_rate * f
					self.w[:,predict_label] -= self.learning_rate * f
			self.learning_rate *= 0.95


	def test(self,test_set,test_label):
		""" Test the trained perceptron model (self.w) using testing dataset.
			The accuracy is computed as the average of correctness
			by comparing between predicted label and true label.

		Args:
		    test_set(numpy.ndarray): testing examples with a dimension of (# of examples, feature_dim)
		    test_label(numpy.ndarray): testing labels with a dimension of (# of examples, )

		Returns:
			accuracy(float): average accuracy value
			pred_label(numpy.ndarray): predicted labels with a dimension of (# of examples, )
		"""

		# YOUR CODE HERE
		accuracy = 0
		pred_label = np.zeros((len(test_set)))
		test_set_b = np.append(test_set, np.ones((test_set.shape[0],1)), axis=1)
		scores = np.matmul(test_set_b,self.w)
		pred_label = np.argmax(scores, axis=1)
		accuracy = np.sum(pred_label == test_label) / len(test_set)

		return accuracy, pred_label

	def save_model(self, weight_file):
		""" Save the trained model parameters
		"""

		np.save(weight_file,self.w)

	def load_model(self, weight_file):
		""" Load the trained model parameters
		"""

		self.w = np.load(weight_file)

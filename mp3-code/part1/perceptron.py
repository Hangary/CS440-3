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

	def train(self,train_set,train_label):
		""" Train perceptron model (self.w) with training dataset. 

		Args:
		    train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
		    train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
		"""

		# YOUR CODE HERE
		model = self.w
		model[model.shape[0] - 1] = 1		# initialize bias as 1
		eta = 1

		for i in range(train_set.shape[0]):
			label = train_label[i]
			f_and_bias = np.append(train_set[i], 1)

			result = model.T @ f_and_bias
			max_index = np.argmax(result)
			if label != max_index:
				model.T[label] += eta * f_and_bias
				model.T[max_index] -= eta * f_and_bias

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

		model = self.w

		for i in range(test_set.shape[0]):
			label = test_label[i]
			f_and_bias = np.append(test_set[i], 1)

			result = model.T @ f_and_bias
			max_index = np.argmax(result)
			pred_label[i] = max_index
			if label == max_index:
				accuracy += 1

		accuracy = accuracy / len(test_set)
		print("accuracy: ", accuracy)
		return accuracy, pred_label

	def save_model(self, weight_file):
		""" Save the trained model parameters 
		""" 

		np.save(weight_file,self.w)

	def load_model(self, weight_file):
		""" Load the trained model parameters 
		""" 

		self.w = np.load(weight_file)


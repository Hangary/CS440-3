import numpy as np

class NaiveBayes(object):
    def __init__(self,num_class,feature_dim,num_value):
        """Initialize a naive bayes model. 
		This function will initialize prior and likelihood, where 
		prior is P(class) with a dimension of (# of class,)
			that estimates the empirical frequencies of different classes in the training set.
		likelihood is P(F_i = f | class) with a dimension of 
			(# of features/pixels per image, # of possible values per pixel, # of class),
			that computes the probability of every pixel location i being value f for every class label.  
		Args:
		    num_class(int): number of classes to classify
		    feature_dim(int): feature dimension for each example 
		    num_value(int): number of possible values for each pixel 
		"""

        self.num_value = num_value
        self.num_class = num_class
        self.feature_dim = feature_dim

        self.prior = np.zeros((num_class))
        self.likelihood = np.zeros((feature_dim,num_value,num_class))

    def train(self,train_set,train_label):
        """ Train naive bayes model (self.prior and self.likelihood) with training dataset. 
			self.prior(numpy.ndarray): training set class prior (in log) with a dimension of (# of class,),
			self.likelihood(numpy.ndarray): traing set likelihood (in log) with a dimension of 
				(# of features/pixels per image, # of possible values per pixel, # of class).
			You should apply Laplace smoothing to compute the likelihood. 
		Args:
		    train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
		    train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
		"""
        # YOUR CODE HERE
        K = 1
        num_class = self.num_class
        num_examples = train_set.shape[0]

        feature_dim = self.feature_dim
        prior = self.prior
        likelihood = self.likelihood

        for n in range(num_examples):
            ex_feature = train_set[n]
            ex_label = train_label[n]

            prior[ex_label] += 1

            for f in range(feature_dim):
                likelihood[f][ex_feature[f]][ex_label] += 1

        likelihood += K
        for c in range(num_class):
             likelihood = likelihood / (prior[c] + K * 256)

        prior  = prior / num_examples

    def test(self,test_set,test_label):
        """ Test the trained naive bayes model (self.prior and self.likelihood) on testing dataset,
			by performing maximum a posteriori (MAP) classification.  
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

        num_class = self.num_class
        prior = self.prior
        likelihood = self.likelihood
        feature_dim = self.feature_dim

        for t in range(len(test_set)):
            ex_feature = test_set[t]
            possibities = np.zeros(len(prior))
            possibities += np.log(prior)
            for i, v in enumerate(ex_feature):
                possibities += np.log(likelihood[i][v])
 
            pred_label[t] = np.argmax(possibities)
        
        accuracy = np.sum(pred_label == test_label) / len(test_set)

        print("test complete")
        return accuracy, pred_label


    def save_model(self, prior, likelihood):
        """ Save the trained model parameters 
		"""    

        np.save(prior, self.prior)
        np.save(likelihood, self.likelihood)

    def load_model(self, prior, likelihood):
        """ Load the trained model parameters 
		""" 

        self.prior = np.load(prior)
        self.likelihood = np.load(likelihood)

    def intensity_feature_likelihoods(self, likelihood):
        """
        Get the feature likelihoods for high intensity pixels for each of the classes,
            by sum the probabilities of the top 128 intensities at each pixel location,
            sum k<-128:255 P(F_i = k | c).
            This helps generate visualization of trained likelihood images. 

        Args:
            likelihood(numpy.ndarray): likelihood (in log) with a dimension of
                (# of features/pixels per image, # of possible values per pixel, # of class)
        Returns:
            feature_likelihoods(numpy.ndarray): feature likelihoods for each class with a dimension of
                (# of features/pixels per image, # of class)
        """
	    # YOUR CODE HERE
        likelihood = self.likelihood
        feature_likelihoods = np.zeros((likelihood.shape[0],likelihood.shape[2]))

        for d in range(likelihood.shape[0]):
            for c in range(likelihood.shape[2]):
                feature_likelihoods[d][c] = sum([likelihood[d][v][c] for v in range(128,256)])
                # vals_prob = likelihood[d, :, c]
                # prob_sort = np.argsort(vals_prob)
                # feature_likelihoods[d][c] = np.sum(vals_prob[prob_sort][128:])
        return feature_likelihoods

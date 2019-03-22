import numpy as np


class NaiveBayes(object):
    def __init__(self, num_class, feature_dim, num_value):
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
        self.likelihood = np.zeros((feature_dim, num_value, num_class))
        self.k = 1

    def train(self, train_set, train_label):
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
        print("train start")
        # prior_list = np.zeros(self.num_class)
        # likelihood_list = np.zeros((self.feature_dim, self.num_value, self.num_class))
        #
        # for example in range(len(train_label)):
        #     cur_label = train_label[example]
        #     prior_list[cur_label] += 1
        #     for feature in range(self.feature_dim):
        #         cur_feature = train_set[example][feature]
        #         likelihood_list[feature][cur_feature][cur_label] += 1
        #
        # self.prior = prior_list / self.num_class
        #
        # for classes, count in enumerate(prior_list):
        #     self.likelihood[:][:][classes] = (likelihood_list[:][:][classes] + self.k) / (count + self.k * 256)

        num_example = train_set.shape[0]
        # calculate prior
        for label in range(self.num_class):
            self.prior[label] = np.sum(train_label == label) / len(train_label)
        counter = np.ones((self.feature_dim, self.num_value, self.num_class)) * self.k
        for idx in range(num_example):
            c = train_label[idx]
            for i, feat in enumerate(train_set[idx, :]):
                counter[i, feat, c] += 1
        for c in range(self.num_class):
            for i in range(self.feature_dim):
                self.likelihood[i, :, c] = counter[i, :, c] / np.sum(counter[i, :, c])

        print("train finish")



    def test(self, test_set, test_label):
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

        # accuracy = 0
        print("test start")
        pred_label = np.zeros((len(test_set)))
        for idx in range(len(test_set)):
            pred_label[idx] = self.predict(test_set[idx, :])
        accuracy = np.sum(pred_label == test_label) / len(test_label)

        print("test finish")
        return accuracy, pred_label

    def predict(self, test):
        log_probs = np.log(self.prior)
        for label in range(self.num_class):
            for feature in range(self.feature_dim):
                log_probs[label] += np.log(self.likelihood[feature, test[feature], label])
        return np.argmax(log_probs)

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

        feature_likelihoods = np.zeros((likelihood.shape[0], likelihood.shape[2]))
        for feature in range(self.feature_dim):
            for label in range(self.num_class):
                vals_prob = likelihood[feature, :, label]
                prob_sum = np.argsort(vals_prob)[-128:]
                feature_likelihoods[feature][label] = np.sum(vals_prob[prob_sum])
        return feature_likelihoods


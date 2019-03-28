# TextClassifier.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Dhruv Agarwal (dhruva2@illinois.edu) on 02/21/2019

import math
import heapq

import numpy as np

"""
You should only modify code within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
class TextClassifier(object):
    def __init__(self):
        """Implementation of Naive Bayes for multiclass classification

        :param lambda_mixture - (Extra Credit) This param controls the proportion of contribution of Bigram
        and Unigram model in the mixture model. Hard Code the value you find to be most suitable for your model
        """
        self.lambda_mixture = 0.0

        self.K = 1
        self.model = dict()
        self.prior = dict()
        self.class_words_sum = dict()
        self.unique_words = set()

        for i in range(1,15):
            self.model[i] = dict()
            self.prior[i] = 0
            self.class_words_sum[i] = 0

    def fit(self, train_set, train_label):
        """
        :param train_set - List of list of words corresponding with each text
            example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
            Then train_set := [['i','like','pie'], ['i','like','cake']]

        :param train_labels - List of labels corresponding with train_set
            example: Suppose I had two texts, first one was class 0 and second one was class 1.
            Then train_labels := [0,1]
        """

        # TODO: Write your code here

        for i, v in enumerate(train_set):
            class_num = train_label[i]
            self.prior[class_num] += 1
            self.class_words_sum[class_num] += len(v)
            for word in v:
                self.unique_words.add(word)
                if word not in self.model[class_num].keys():
                    self.model[class_num][word] = 1
                else:
                    self.model[class_num][word] += 1

        top20 = dict()
        for c in range(1,15):
            words = []
            temp_prior = (self.prior[c]) / (len(train_label))
            if temp_prior == 0:
                self.prior[c] = float('-inf')
            else:
                self.prior[c] = math.log(temp_prior)
            
            for w in self.model[c].keys():
                heapq.heappush(words, (-self.model[c][w], w))
                self.model[c][w] = math.log((self.model[c][w] + self.K) / (self.class_words_sum[c] + self.K * len(self.unique_words)))
            top20[c] = [heapq.heappop(words) for i in range(20)]
        
        for c in top20.keys():
            print("class ", c, " :")
            for pair in top20[c]:
                print(pair)
            print("##########################")

    def predict(self, x_set, dev_label,lambda_mix=0.0):
        """
        :param dev_set: List of list of words corresponding with each text in dev set that we are testing on
              It follows the same format as train_set
        :param dev_label : List of class labels corresponding to each text
        :param lambda_mix : Will be supplied the value you hard code for self.lambda_mixture if you attempt extra credit

        :return:
                accuracy(float): average accuracy value for dev dataset
                result (list) : predicted class for each text
        """

        accuracy = 0.0
        result = []

        confusion_matrix = np.zeros((14,14))

        # TODO: Write your code here
        for i, v in enumerate(x_set):
            label = dev_label[i]
            predict = []
            for c in range(1,15):
                sum = 0
                sum += self.prior[c]
                for w in v:
                    if w in self.unique_words:
                        if w in self.model[c].keys():
                            sum += self.model[c][w]
                        else:
                            sum += math.log((self.K) / (self.class_words_sum[c] + self.K * len(self.unique_words)))

                predict.append(sum)
            max_value = max(predict)
            predict_class = predict.index(max_value) + 1

            confusion_matrix[label - 1][predict_class - 1] += 1
            result.append(predict_class)

            if predict_class == label:
                accuracy += 1
        
        for i in range(14):
            confusion_matrix[i] = np.around(confusion_matrix[i] / np.sum(confusion_matrix[i]), decimals=2)
        print(confusion_matrix)
        accuracy = accuracy / len(dev_label)
        return accuracy,result


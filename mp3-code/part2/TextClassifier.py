import math
import heapq
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
        self.s = set()
        self.class_words_sum = dict()
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
                if word not in self.model[class_num].keys():
                    self.model[class_num][word] = 1
                    self.s.add(word)
                else:
                    self.model[class_num][word] += 1

        top20 = dict()
        p = 3
        for c in range(1,15):
            words = []
            self.prior[c] = math.log2((self.prior[c]) / (len(train_label)))
            for w in self.model[c].keys():
                heapq.heappush(words, (-self.model[c][w], w))
                self.model[c][w] = math.log2((self.model[c][w]) / (self.class_words_sum[c]))
            top20[c] = [heapq.heappop(words) for i in range(20)]
        
        for c in top20.keys():
            print("class ", c, " :")
            for pair in top20[c]:
                print(pair[1])
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

        # TODO: Write your code here
        for i, v in enumerate(x_set):
            label = dev_label[i]
            predict = []
            for c in range(1,15):
                sum = self.prior[c]
                for w in v:
                    if w in self.model[c].keys():
                        sum += self.model[c][w]
                    else:
                        sum += math.log2((self.K) / (self.class_words_sum[c] + self.K * len(self.s)))

                predict.append(sum)
            max_value = max(predict)
            predict_class = predict.index(max_value) + 1

            result.append(predict_class)

            if predict_class == label:
                accuracy += 1
        
        accuracy = accuracy / len(dev_label)
        return accuracy,result


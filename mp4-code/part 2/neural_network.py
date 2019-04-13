import numpy as np
import time
"""
    Minigratch Gradient Descent Function to train model
    1. Format the data
    2. call four_nn function to obtain losses
    3. Return all the weights/biases and a list of losses at each epoch
    Args:
        epoch (int) - number of iterations to run through neural net
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - starting weights
        x_train (np array) - (n,d) numpy array where d=number of features
        y_train (np array) - (n,) all the labels corresponding to x_train
        num_classes (int) - number of classes (range of y_train)
        shuffle (bool) - shuffle data at each epoch if True. Turn this off for testing.
    Returns:
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - resulting weights
        losses (list of ints) - each index should correspond to epoch number
            Note that len(losses) == epoch
    Hints:
        Should work for any number of features and classes
        Good idea to print the epoch number at each iteration for sanity checks!
        (Stdout print will not affect autograder as long as runtime is within limits)
"""
def minibatch_gd(epoch, w1, w2, w3, w4, b1, b2, b3, b4, x_train, y_train, num_classes, shuffle=True):

    #IMPLEMENT HERE
    losses = []
    num_train = x_train.shape[0]
    for it in range(epoch):
        start = time.time()
        X_batch = x_train
        y_batch = y_train
        print("epoch: " + str(it))
        N = x_train.shape[0]
        loss = 0
        if shuffle == True:
            index = np.random.choice(num_train, num_train, replace = False)
            X_batch = x_train[index]
            y_batch = y_train[index]
        for i in range(int(N/200)):
            batch_x = X_batch[i*200:(i+1)*200]
            batch_y = y_batch[i*200:(i+1)*200]
            loss1,w1, w2, w3, w4, b1, b2, b3, b4 = four_nn(w1, w2, w3, w4, b1, b2, b3, b4, batch_x, batch_y,test = False)
            loss += loss1
        losses.append(loss)
        print(loss)
        end = time.time()
        print(end - start)

    return w1, w2, w3, w4, b1, b2, b3, b4, losses

"""
    Use the trained weights & biases to see how well the nn performs
        on the test data
    Args:
        All the weights/biases from minibatch_gd()
        x_test (np array) - (n', d) numpy array
        y_test (np array) - (n',) all the labels corresponding to x_test
        num_classes (int) - number of classes (range of y_test)
    Returns:
        avg_class_rate (float) - average classification rate
        class_rate_per_class (list of floats) - Classification Rate per class
            (index corresponding to class number)
    Hints:
        Good place to show your confusion matrix as well.
        The confusion matrix won't be autograded but necessary in report.
"""
def test_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, num_classes):
    classification = four_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, test=True)
    print (classification)
    class_rate_per_class = [0.0] * num_classes
    yy = np.zeros(num_classes)
    right = 0
    for i in range(x_test.shape[0]):
        if y_test[i] == classification[i]:
            class_rate_per_class[int(y_test[i])] += 1
            right += 1
        yy[int(y_test[i])] += 1
    avg_class_rate = right*1.0/x_test.shape[0]
    class_rate_per_class = class_rate_per_class/yy
    return avg_class_rate, class_rate_per_class

"""
    4 Layer Neural Network
    Helper function for minibatch_gd
    Up to you on how to implement this, won't be unit tested
    Should call helper functions below
"""
def four_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_train, y_train, test):
    Z1,acache1 = affine_forward(x_train, w1, b1)
    A1,rcache1 = relu_forward(Z1)
    Z2,acache2 = affine_forward(A1, w2, b2)
    A2,rcache2 = relu_forward(Z2)
    Z3,acache3 = affine_forward(A2, w3, b3)
    A3,rcache3 = relu_forward(Z3)
    F,acache4 = affine_forward(A3,w4,b4)
    if test == True:
        classification = np.argmax(F, axis=1)
        return classification
    loss, dF = cross_entropy(F, y_train)
    dA3, dW4, dB4 = affine_backward(dF,acache4)
    dZ3 = relu_backward(dA3,rcache3)
    dA2, dW3, dB3 = affine_backward(dZ3,acache3)
    dZ2 = relu_backward(dA2,rcache2)
    dA1, dW2, dB2 = affine_backward(dZ2,acache2)
    dZ1 = relu_backward(dA1,rcache1)
    dX, dW1, dB1 = affine_backward(dZ1,acache1)
    eta = 0.1
    w1 = w1 - eta*dW1
    w2 = w2 - eta*dW2
    w3 = w3 - eta*dW3
    w4 = w4 - eta*dW4
    b1 = b1 - eta*dB1
    b2 = b2 - eta*dB2
    b3 = b3 - eta*dB3
    b4 = b4 - eta*dB4
    return loss,w1, w2, w3, w4, b1, b2, b3, b4


"""
    Next five functions will be used in four_nn() as helper functions.
    All these functions will be autograded, and a unit test script is provided as unit_test.py.
    The cache object format is up to you, we will only autograde the computed matrices.

    Args and Return values are specified in the MP docs
    Hint: Utilize numpy as much as possible for max efficiency.
        This is a great time to review on your linear algebra as well.
"""
def affine_forward(A, W, b):
    # Inputs: A (data with size n,d)
    #W (weights with size d,d')
    #b (bias with size d')
    #Outputs: Z (affine output with size n,d')
    # cache (tuple of the original inputs)
    Z = np.dot(A,W) + b
    cache = (A,W,b)
    return Z, cache

def affine_backward(dZ, cache):
    A,W,b = cache
    dB = np.sum(dZ, axis=0)
    dA = np.dot(dZ,np.transpose(W))
    dW = np.dot(np.transpose(A),dZ)
    return dA, dW, dB

def relu_forward(Z):
    A = np.maximum(0,Z)
    cache = Z
    return A, cache

def relu_backward(dA, cache):
    Z = cache
    dA[Z <= 0] = 0
    return dA

def cross_entropy(F, y):
    n = F.shape[0]
    num_classes = F.shape[1]
    loss = 0
    match = np.zeros(F.shape)
    f_exp = np.exp(F)
    f_expsum = f_exp.sum(axis = 1)
    for i in range(n):
        loss += F[i][int(y[i])]
        match[i][int(y[i])] = 1
    loss -= np.log(f_expsum).sum()
    loss = -loss/n
    dF = f_exp/f_expsum[:, np.newaxis]
    dF = -(match - dF)/n
    return loss, dF

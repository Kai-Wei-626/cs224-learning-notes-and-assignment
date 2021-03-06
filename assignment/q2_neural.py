#!/usr/bin/env python

import numpy as np
import random

from q1_softmax import softmax
from q2_sigmoid import sigmoid, sigmoid_grad
from q2_gradcheck import gradcheck_naive


def forward_backward_prop(X, labels, params, dimensions):
    """
    Forward and backward propagation for a two-layer sigmoidal network

    Compute the forward propagation and for the cross entropy cost,
    the backward propagation for the gradients for all parameters.

    Notice the gradients computed here are different from the gradients in
    the assignment sheet: they are w.r.t. weights, not inputs.

    Arguments:
    X -- M x Dx matrix, where each row is a training example x.
    labels -- M x Dy matrix, where each row is a one-hot vector.
    params -- Model parameters, these are unpacked for you.
    dimensions -- A tuple of input dimension, number of hidden units
                  and output dimension
    """

    ### Unpack network parameters (do not modify)
    ofs = 0
    Dx, H, Dy = (dimensions[0], dimensions[1], dimensions[2])

    W1 = np.reshape(params[ofs:ofs+ Dx * H], (Dx, H))       # (10, 5)
    ofs += Dx * H
    b1 = np.reshape(params[ofs:ofs + H], (1, H))            # (1, 5)
    ofs += H
    W2 = np.reshape(params[ofs:ofs + H * Dy], (H, Dy))      # (5, 10)
    ofs += H * Dy
    b2 = np.reshape(params[ofs:ofs + Dy], (1, Dy))          # (1, 10)

    ### YOUR CODE HERE: forward propagation
    z1 = np.dot(X, W1) + b1                                 # (20, 5)
    a1 = sigmoid(z1)                                        # (20, 5)
    scores = np.dot(a1, W2) + b2                            # (20, 10)

    y_pred = softmax(scores)
    cost = -np.sum(labels * np.log(y_pred))

    # ### END YOUR CODE

    # ### YOUR CODE HERE: backward propagation
    dscores = y_pred - labels                               # (20, 10)
    gradW2 = np.dot(a1.T, dscores)                          # (5, 10)
    # gradW2 bp step 1: back to d(softmax(theta))/d(theta), this is equal to y-bar - y, which is dscores defined in line 52
    # gradW2 bp step 2: back to d(W2*X2)/d(W2), this is equal to X2
    # so combine 2 steps together, gradW2 = X2.T * (y-bar - y)

    gradb2 = np.sum(dscores, axis=0)                        #  (1, 10)    
    da1 = np.dot(dscores, W2.T)
    dz1 = sigmoid_grad(a1)*da1
    gradW1 = np.dot(X.T, dz1)
    gradb1 = np.sum(dz1, axis=0)
    ### END YOUR CODE

    ### Stack gradients (do not modify)
    grad = np.concatenate((gradW1.flatten(), gradb1.flatten(),
        gradW2.flatten(), gradb2.flatten()))

    return cost, grad                                       # cost is a single number, grad is a nparray


def sanity_check():
    """
    Set up fake data and parameters for the neural network, and test using
    gradcheck.
    """
    print("Running sanity check...")

    N = 20
    dimensions = [10, 5, 10]
    data = np.random.randn(N, dimensions[0])   # each row will be a datum
    labels = np.zeros((N, dimensions[2]))
    for i in range(N):
        labels[i, random.randint(0,dimensions[2]-1)] = 1

    params = np.random.randn((dimensions[0] + 1) * dimensions[1] + (
        dimensions[1] + 1) * dimensions[2], ) # place all parameters in 1-d array to make it easy for looping through

    gradcheck_naive(lambda params:
        forward_backward_prop(data, labels, params, dimensions), params) 

'''
def your_sanity_checks():
    """
    Use this space add any additional sanity checks by running:
        python q2_neural.py
    This function will not be called by the autograder, nor will
    your additional tests be graded.
    """
    print "Running your sanity checks..."
    ### YOUR CODE HERE
    raise NotImplementedError
    ### END YOUR CODE
'''

if __name__ == "__main__":
    sanity_check()
    #your_sanity_checks()

# Define 3 different Versions of an neural network matrix approximator
# - numpy
# - cpu only, torch
# - gpu + cpur, torch

import time

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.

#these parameters work, but numpy is fastest and gpu slowest
N, D_in, H, D_out = 64, 1000, 100, 10

#these parameters yield NANS, but the gpu speed is fastest
# N, D_in, H, D_out = 640, 10000, 1000, 100

# problems as above
# N, D_in, H, D_out = 300, 5000, 500, 50


# Define Learning Rate
learning_rate = 1e-6

#Define GPU + CPU torch implementation

def matrix_approximator_gpu_torch(N, D_in, H, D_out, learning_rate):
    import torch
    
    dtype = torch.float
    device = torch.device("cpu")
    # Activate GPU
    device = torch.device("cuda:0") 
    
    # Create random input and output data
    x = torch.randn(N, D_in, device=device, dtype=dtype)
    y = torch.randn(N, D_out, device=device, dtype=dtype)
    
    # Randomly initialize weights
    w1 = torch.randn(D_in, H, device=device, dtype=dtype)
    w2 = torch.randn(H, D_out, device=device, dtype=dtype)
    
    for t in range(500):
        # Forward pass: compute predicted y
        h = x.mm(w1)
        h_relu = h.clamp(min=0)
        y_pred = h_relu.mm(w2)
    
        # Compute and print loss
        loss = (y_pred - y).pow(2).sum().item()
        if t % 100 == 99:
            print(t, loss)
    
        # Backprop to compute gradients of w1 and w2 with respect to loss
        grad_y_pred = 2.0 * (y_pred - y)
        grad_w2 = h_relu.t().mm(grad_y_pred)
        grad_h_relu = grad_y_pred.mm(w2.t())
        grad_h = grad_h_relu.clone()
        grad_h[h < 0] = 0
        grad_w1 = x.t().mm(grad_h)
    
        # Update weights using gradient descent
        w1 -= learning_rate * grad_w1
        w2 -= learning_rate * grad_w2




#Define CPU-only torch implementation

def matrix_approximator_cpu_torch(N, D_in, H, D_out, learning_rate):
    import torch
    
    
    dtype = torch.float
    device = torch.device("cpu")
    # device = torch.device("cuda:0") # Uncomment this to run on GPU
    
    # Create random input and output data
    x = torch.randn(N, D_in, device=device, dtype=dtype)
    y = torch.randn(N, D_out, device=device, dtype=dtype)
    
    # Randomly initialize weights
    w1 = torch.randn(D_in, H, device=device, dtype=dtype)
    w2 = torch.randn(H, D_out, device=device, dtype=dtype)
    
    for t in range(500):
        # Forward pass: compute predicted y
        h = x.mm(w1)
        h_relu = h.clamp(min=0)
        y_pred = h_relu.mm(w2)
    
        # Compute and print loss
        loss = (y_pred - y).pow(2).sum().item()
        if t % 100 == 99:
            print(t, loss)
    
        # Backprop to compute gradients of w1 and w2 with respect to loss
        grad_y_pred = 2.0 * (y_pred - y)
        grad_w2 = h_relu.t().mm(grad_y_pred)
        grad_h_relu = grad_y_pred.mm(w2.t())
        grad_h = grad_h_relu.clone()
        grad_h[h < 0] = 0
        grad_w1 = x.t().mm(grad_h)
    
        # Update weights using gradient descent
        w1 -= learning_rate * grad_w1
        w2 -= learning_rate * grad_w2
    
    
    
    
#Define Numpy Implementation

def matrix_approximator_numpy(N, D_in, H, D_out, learning_rate):
    import numpy as np
    # Implemented as Example 1 from https://pytorch.org/tutorials/beginner/pytorch_with_examples.html
    
    # Create random input and output data
    
    x = np.random.randn(N, D_in)
    y = np.random.randn(N, D_out)
    
    # Randomly initialize weights
    
    w1 = np.random.randn(D_in,H)
    w2 = np.random.randn(H,D_out)
    
    # Start main loop, Iterations are set internally, should probably become an input eventually
    
    for t in range(500):
        # Forward pass: compute predicted y (is .dot efficient? is it numpy?)
        h = x.dot(w1)
        h_relu = np.maximum(h,0)
        y_pred = h_relu.dot(w2)
        
        # Compute and print loss
        loss = np.square(y_pred - y).sum()
        if t % 100 == 99:
            print(t, loss)
        
        # Backprop to compute gradients of w1 and w2 with respect to loss
        grad_y_pred = 2.0 * (y_pred - y)
        grad_w2 = h_relu.T.dot(grad_y_pred)
        grad_h_relu = grad_y_pred.dot(w2.T)
        grad_h = grad_h_relu.copy()
        grad_h[h < 0] = 0
        grad_w1 = x.T.dot(grad_h)
    
        # Update weights
        w1 -= learning_rate * grad_w1
        w2 -= learning_rate * grad_w2


tic = time.perf_counter()
print("\n Numpy:\n")        
matrix_approximator_numpy(N, D_in, H, D_out, learning_rate)
toc = time.perf_counter()
numpy_time = toc-tic
print("Runtime:",numpy_time)

tic = time.perf_counter()
print("\n CPU: \n")        
matrix_approximator_cpu_torch(N, D_in, H, D_out, learning_rate)
toc = time.perf_counter()
cpu_time = toc-tic
print("Runtime:",cpu_time)

tic = time.perf_counter()
print("\n GPU: \n")
matrix_approximator_gpu_torch(N, D_in, H, D_out, learning_rate)
toc = time.perf_counter()
gpu_time = toc-tic
print("Runtime:",gpu_time)

import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
# Load the dataset
file_path = "D:\\facultate\\an3\\ai\\tema 5\\seeds_dataset.txt"
data = np.genfromtxt(file_path)

# shuffle the data
np.random.shuffle(data)

X = data[:, :-1]
Y = data[:, -1]

# one-hot encoding
num_classes = len(np.unique(Y))
Y_one_hot = np.eye(num_classes)[Y.astype(int) - 1]

# training and testing sets

X_train, X_test, Y_train, Y_test = train_test_split(X, Y_one_hot, test_size=0.3, random_state=None)

# initialize parameters
input_size = X_train.shape[1]
hidden_size = 4
output_size = num_classes
learning_rate = 0.05
epochs = 50
np.random.seed(42)

weights_input_hidden = np.random.rand(input_size, hidden_size)
bias_input_hidden = np.random.rand(1)
weights_hidden_output = np.random.rand(hidden_size, output_size)
bias_hidden_output = np.random.rand(1)

# activation fct
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

# derivative of the activation fct
def sigmoid_derivative(x):
    return x * (1 - x)

# training 
for epoch in range(epochs):
    # fwd propagation
    hidden_input = np.dot(X_train, weights_input_hidden) + bias_input_hidden
    hidden_output = sigmoid(hidden_input)

    output_input = np.dot(hidden_output, weights_hidden_output) + bias_hidden_output
    predicted_output = softmax(output_input)

    # backpropagation
    output_error = Y_train - predicted_output
    output_delta = output_error / len(X_train) # adjusting the weights (error gradient for output)

    hidden_error = output_delta.dot(weights_hidden_output.T)
    hidden_delta = hidden_error * sigmoid_derivative(hidden_output)

    # update weights and biases
    weights_hidden_output -= learning_rate * hidden_output.T.dot(output_delta)
    bias_hidden_output -= learning_rate * np.sum(output_delta)/210
    
    weights_input_hidden -= learning_rate * X_train.T.dot(hidden_delta)
    bias_input_hidden -= learning_rate * np.sum(hidden_delta)/210

# testing
hidden_layer_test = sigmoid(np.dot(X_test, weights_input_hidden) + bias_input_hidden)
predicted_output_test = softmax(np.dot(hidden_layer_test, weights_hidden_output) + bias_hidden_output)

# # Convert the predicted probabilities to class labels
# predicted_labels = np.argmax(predicted_output_test, axis=1) + 1

# # Convert one-hot encoded true labels to class labels
# true_labels = np.argmax(Y_test, axis=1) + 1

# accuracy
correct_predictions = np.sum(np.argmax(predicted_output_test, axis=1) == np.argmax(Y_test, axis=1))
accuracy = correct_predictions / len(Y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

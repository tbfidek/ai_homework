import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# dataset
file_path = "D:\\facultate\\an3\\ai\\tema 5\\seeds_dataset.txt"
data = np.genfromtxt(file_path)

X = data[:, :-1]
Y = data[:, -1]

# one-hot encoding
num_classes = len(np.unique(Y))
Y_one_hot = np.eye(num_classes)[Y.astype(int) - 1]

# training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y_one_hot, test_size=0.2, random_state=None)

# initialize parameters with glorot 
def glorot_init(input_size, output_size):
    limit = np.sqrt(6 / (input_size + output_size))
    return np.random.uniform(-limit, limit, (input_size, output_size))

input_size = X_train.shape[1]
hidden_size = 4
output_size = num_classes
learning_rate = 0.05
epochs = 200
np.random.seed(42)

weights_input_hidden = glorot_init(input_size, hidden_size)
bias_input_hidden = np.zeros((1, hidden_size))
weights_hidden_output = glorot_init(hidden_size, output_size)
bias_hidden_output = np.zeros((1, output_size))

training_errors = []
testing_errors = []

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

    np.random.seed(epoch)
    np.random.shuffle(X_train)
    np.random.seed(epoch)
    np.random.shuffle(Y_train)
    
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

    # training error avg
    training_error = np.mean(np.abs(output_error))
    training_errors.append(training_error)

    # update weights and biases
    weights_hidden_output -= learning_rate * hidden_output.T.dot(output_delta)
    bias_hidden_output -= learning_rate * np.sum(output_delta)/210
    
    weights_input_hidden -= learning_rate * X_train.T.dot(hidden_delta)
    bias_input_hidden -= learning_rate * np.sum(hidden_delta)/210

# testing
hidden_layer_test = sigmoid(np.dot(X_test, weights_input_hidden) + bias_input_hidden)
predicted_output_test = softmax(np.dot(hidden_layer_test, weights_hidden_output) + bias_hidden_output)

# testing error avg
testing_error = np.mean(np.abs(Y_test - predicted_output_test))
testing_errors.append(testing_error)

# plotting convergence
plt.figure(figsize=(10, 5))
plt.plot(range(epochs), training_errors, label='Training Error')
plt.xlabel('epochs')
plt.ylabel('error')
plt.title('training convergence')
plt.legend()
plt.show()

# visualization of misclassified points
predicted_labels = np.argmax(predicted_output_test, axis=1) + 1
true_labels = np.argmax(Y_test, axis=1) + 1

misclassified_points = X_test[predicted_labels != true_labels]

plt.figure(figsize=(8, 8))
plt.scatter(X_test[:, 0], X_test[:, 1], c=true_labels, cmap=plt.cm.Paired, label='True Labels')
plt.scatter(misclassified_points[:, 0], misclassified_points[:, 1], marker='x', c='r', label='Misclassified')
plt.title('Misclassified Points')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.show()

# convert the predicted probabilities to class labels
predicted_labels = np.argmax(predicted_output_test, axis=1) + 1

# convert one-hot encoded true labels to class labels
true_labels = np.argmax(Y_test, axis=1) + 1

# accuracy
correct_predictions = np.sum(np.argmax(predicted_output_test, axis=1) == np.argmax(Y_test, axis=1))
accuracy = correct_predictions / len(Y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

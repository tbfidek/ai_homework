import numpy as np
from sklearn.model_selection import train_test_split

# the dataset
file_path = "seeds_dataset.txt"
data = np.genfromtxt(file_path)


X = data[:, :-1]
y = data[:, -1]

# random train/test data
test_size = np.random.uniform(0.1, 0.7)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=None)

# init
input_size = X_train.shape[1]
hidden_size = 4  # number of neurons in the hidden layer
output_size = len(np.unique(y_train))  # number of classes
learning_rate = 0.01
epochs = 10000
np.random.seed(42)
weights_input_hidden = np.random.rand(input_size, hidden_size)
weights_hidden_output = np.random.rand(hidden_size, output_size)


# activation thingy
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# activation for backpropagation cica
def sigmoid_derivative(x):
    return x * (1 - x)


# mean squared error
def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)


# for backpropagation cica
def mean_squared_error_derivative(y_true, y_pred):
    return 2 * (y_pred - y_true) / len(y_true)


# forward thingy
hidden_input = np.dot(X_train, weights_input_hidden)
hidden_output = sigmoid(hidden_input)
print("Hidden Output:", hidden_output)

output_input = np.dot(hidden_output, weights_hidden_output)
predicted_output = sigmoid(output_input)
print("Predicted Output:", predicted_output)


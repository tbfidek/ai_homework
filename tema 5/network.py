import numpy as np

class Network():
    # init network w/ specified layer sizes
    def __init__(self, input_layer_size, hidden_layer_size, output_layer_size):
        # standard deviation
        hidden_layer_st_dev = 1 / np.sqrt(input_layer_size)
        output_layer_st_dev = 1 / np.sqrt(hidden_layer_size)
        # intialise weights
        self.hidden_layer_weights = np.random.normal(scale = hidden_layer_st_dev, size = (hidden_layer_size, input_layer_size))
        self.output_layer_weights = np.random.normal(scale = output_layer_st_dev, size = (output_layer_size, hidden_layer_size))
        # intialise biases
        self.hidden_layer_biases = np.zeros((hidden_layer_size, 1))
        self.output_layer_biases = np.zeros((output_layer_size, 1))
    
    def input_reshape(self, data_set, i):
        # transform input and target from vectors to matrices with one column for an easier multiplication
        input_layer = data_set[0][i].reshape(-1, 1) # matrix w/ one column
        input_target = data_set[1][i]
        # one hot encoding
        binary_target = np.array([0 for _ in range(3)])
        binary_target[input_target] = 1
        binary_target.shape += (1,)
        return input_layer, binary_target

    # activation fct & its derivative
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def fwd_propagation(self, input_layer):
        hidden_layer_preactivation = self.hidden_layer_biases +  np.dot(self.hidden_layer_weights, input_layer)
        hidden_layer_activation = self.sigmoid(hidden_layer_preactivation)

        output_layer_preactivation = self.output_layer_biases + np.dot(self.output_layer_weights, hidden_layer_activation)
        output_layer_activation = self.sigmoid(output_layer_preactivation)

        return hidden_layer_activation, output_layer_activation
    
    def backpropagation(self, input_layer, binary_target, hidden_layer_activation, output_layer_activation, learning_rate):
        # error = predicted output - correct output for output layer
        output_layer_delta = output_layer_activation - binary_target
        # error for the hidden layer
        hidden_layer_delta = np.dot(np.transpose(self.output_layer_weights), output_layer_delta) * self.sigmoid_derivative(hidden_layer_activation)

        # adjusting weights & biases for output & hidden layer
        self.output_layer_weights -= learning_rate * np.dot(output_layer_delta, np.transpose(hidden_layer_activation))
        self.output_layer_biases -= learning_rate * output_layer_delta

        self.hidden_layer_weights -= learning_rate * np.dot(hidden_layer_delta, np.transpose(input_layer))
        self.hidden_layer_biases -= learning_rate * hidden_layer_delta
    
    def test(self, data_set):
        size = len(data_set[0]) # dataset size
        correct_count = 0
        actual = [] # actual class labels
        predicted = [] # predicted class labels
        input_results = {} # input results vs correct results
        
        for i in range(size):
            input_layer, binary_target = self.input_reshape(data_set, i) # input and target data

            # fwd propagation
            _, output_layer_activation = self.fwd_propagation(input_layer)

            correct_guess = int(np.argmax(output_layer_activation) == np.argmax(binary_target))
            correct_count += correct_guess
            input_results[(input_layer[0][0], input_layer[1][0])] = correct_guess
            actual += [np.argmax(output_layer_activation)]
            predicted += [np.argmax(binary_target)]

        print(f"test accuracy: {round((correct_count / size) * 100, 2)}%")
        # actual labels, predicted labels, input correctness result
        return (np.array(actual), np.array(predicted)), input_results

    def train(self, data_set, learning_rate, epochs_count):
        size = len(data_set[0])
        correct_count = 0
        for epoch in range(epochs_count):
            for i in range(size):
                # transform input and target from vectors to matrices with one column for an easier multiplication
                input_layer, binary_target = self.input_reshape(data_set, i)
                hidden_layer_activation, output_layer_activation = self.fwd_propagation(input_layer)
                correct_count += int(np.argmax(output_layer_activation) == np.argmax(binary_target))
                self.backpropagation(input_layer, binary_target, hidden_layer_activation, output_layer_activation, learning_rate)

            print(f"training accuracy (epoch {epoch}): {round((correct_count / size) * 100, 2)}%")
            correct_count = 0

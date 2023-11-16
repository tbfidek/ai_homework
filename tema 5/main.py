from random import shuffle
from network import Network
import numpy as np

def read_data(filename):
    with open(filename, 'r') as fd:
        data_input = []
        data_labels = []
        input_strings = []
        max_input_length = 0 

        for readline in fd:
            string = readline.strip()
            input_strings += [string]

        shuffle(input_strings)
        shuffle(input_strings)

        labels_dict = {}
        for string in input_strings:
            input_arr = string.split('\t') 
            input_values = list(map(lambda x: float(x) if x.strip() != '' else 0.0, input_arr[:-1]))
            max_input_length = max(max_input_length, len(input_values))
            data_input += [np.array(input_values)]
            label_key = input_arr[-1]
            label_value = labels_dict.setdefault(label_key, len(labels_dict))
            data_labels += [label_value]

        # zero-pad the input arrays to make them consistent in length
        data_input = [np.pad(arr, (0, max_input_length - len(arr))) for arr in data_input]

        inverted_dict = {}
        for key, value in labels_dict.items():
            inverted_dict[value] = key

    return (np.array(data_input), np.array(data_labels)), inverted_dict

def split_input_data(input_data):
    split_point = int(len(input_data[0]) * 8 / 10)
    train_set = (input_data[0][:split_point], input_data[1][:split_point])
    test_set = (input_data[0][split_point:], input_data[1][split_point:])
    return train_set, test_set

def init_layer_counts(input_data):
    input_layer_count = len(input_data[0][0]) # 7 neuroni pt 7 atribute
    print(input_layer_count)
    output_layer_count = max(input_data[1]) + 1 # 3 neuroni pt 3 clase
    hidden_layer_count = int(2 / 3 * (input_layer_count + output_layer_count))
    return input_layer_count, hidden_layer_count, output_layer_count

def print_set(data):
    for i in range(len(data[0])):
        print(data[0][i], data[1][i])

input_data, labels_dict = read_data('D:\\facultate\\an3\\ai\\tema 5\\seeds_dataset.txt') 
train_set, test_set = split_input_data(input_data)
#print_set(train_set)
network = Network(*init_layer_counts(input_data))
network.train(train_set, 0.01, 10)
(actual, predicted), results = network.test(test_set)

#print(results)

from random import shuffle
from network import Network
import numpy as np


# reads the dataset and splits it between attributes & labels 
def read_data(filename):
    with open(filename, 'r') as fd:
        # the attributes dataset
        data_input = []
        # the labels dataset
        data_labels = []
        input_strings = []
        max_input_length = 0 

        for readline in fd:
            string = readline.strip() # removes spaces
            input_strings += [string] # adds value to the list
        
        shuffle(input_strings)

        labels_dict = {}
   
        for string in input_strings:
            input_values = list(map(lambda x: float(x), string.split('\t')[:-1]))
            # number of attributes (all columns, except the last one)
            max_input_length = max(max_input_length, len(input_values))
            data_input += [np.array(input_values)]

            # label for grain (last column)
            label_key = string.split('\t')[-1]
            label_value = labels_dict.setdefault(label_key, len(labels_dict))
            data_labels += [label_value]

    return (np.array(data_input), np.array(data_labels)), max_input_length

# splits the data into training and testing sets
def split_input_data(input_data):
    split_point = int(len(input_data[0]) * 8 / 10)
    train_set = (input_data[0][:split_point], input_data[1][:split_point])
    test_set = (input_data[0][split_point:], input_data[1][split_point:])
    return train_set, test_set

# defines the number of neurons for each layer
def init_layer_counts(input_data):
    input_layer_count = len(input_data[0][0]) # 7 neuroni pt 7 atribute
    output_layer_count = max(input_data[1]) + 1 # 3 neuroni pt 3 clase
    hidden_layer_count = int(2 / 3 * (input_layer_count + output_layer_count))
    return input_layer_count, hidden_layer_count, output_layer_count

def main():
    input_data, _ = read_data('D:\\facultate\\an3\\ai\\tema 5\\seeds_dataset.txt') 
    train_set, test_set = split_input_data(input_data)
    network = Network(*init_layer_counts(input_data))
    network.train(train_set, 0.001, 1)
    (actual, predicted), results = network.test(test_set)

if __name__ == "__main__":
    main()

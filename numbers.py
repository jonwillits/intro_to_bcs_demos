import tkinter as tk
import sys
import numpy as np


class Network:
    ############################################################################################################
    def __init__(self, input_size, hidden_size, output_size):

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weight_mean = 0
        self.weight_stdev = 0.01

        self.h_bias = np.random.normal(0, self.weight_stdev, [self.hidden_size])
        self.h_x = np.random.normal(0, self.weight_stdev, [self.hidden_size, self.input_size])

        self.o_bias = np.random.normal(0, self.weight_stdev, [self.output_size])
        self.o_h = np.random.normal(0, self.weight_stdev, [self.output_size, self.hidden_size])

    ############################################################################################################
    def feedforward(self, x):
        h = self.tanh(np.dot(self.h_x, x) + self.h_bias)
        o = self.sigmoid(np.dot(self.o_h, h) + self.o_bias)
        return h, o

    ############################################################################################################
    @staticmethod
    def calc_cost(y, o):
        return y - o
        # absolute value of the difference

    ############################################################################################################
    def backpropogation(self, x, o, h, o_cost, learning_rate):
        o_delta = o_cost * self.sigmoid_prime(o)

        h_cost = np.dot(o_delta, self.o_h)
        h_delta = h_cost * self.tanh_prime(h)

        # change all these to -=
        self.o_bias += o_delta * learning_rate
        self.o_h += (np.dot(o_delta.reshape(len(o_delta), 1), h.reshape(1, len(h))) * learning_rate)

        self.h_bias += h_delta * learning_rate
        self.h_x += (np.dot(h_delta.reshape(len(h_delta), 1), x.reshape(1, len(x))) * learning_rate)

    ############################################################################################################
    @staticmethod
    def tanh(z):
        return np.tanh(z)

    ############################################################################################################
    @staticmethod
    def tanh_prime(z):
        return 1.0 - np.tanh(z)**2

    ############################################################################################################
    @staticmethod
    def sigmoid(z):
        return 1/(1+np.exp(-z))

    ############################################################################################################
    @staticmethod
    def sigmoid_prime(z):
        return 1/(1+np.exp(-z)) * (1 - 1/(1+np.exp(-z)))

############################################################################################################
############################################################################################################
class Display:
    def __init__(self, window_size, network, dataset):

        self.network = network
        self.dataset = dataset
        self.height = window_size[0]
        self.width = window_size[1]

        self.root = tk.Tk()

        self.root.title("Number Recognition Network")

        self.draw_network()

    def draw_network(self):
        pass

    def reset(self):
        self.network.init_network()

    @staticmethod
    def quit_simulation():
        sys.exit()

    @staticmethod
    def get_hex_color(value):
        abs_value = 1 - abs(value)
        scaled_value = int(round(255 * abs_value, 0))
        hex_value = hex(scaled_value)[2:]

        if len(hex_value) == 1:
            hex_value = "0" + hex_value

        if value > 0:
            return '#{}ff{}'.format(hex_value, hex_value)
        elif value < 0:
            return '#ff{}{}'.format(hex_value, hex_value)
        else:
            return "#ffffff"


class Dataset:

    def __init__(self, file_path):
        self.file_path = file_path
        self.number_list = []
        self.number_index_dict = {}
        self.number_data_dict = {}
        self.read_file()

    def read_file(self):
        f = open(self.file_path)
        line_counter = 0
        for line in f:
            data = (line.strip().strip('\n').strip()).split(',')
            self.number_list.append(data[0])
            self.number_index_dict[data[0]] = line_counter
            self.number_data_dict[data[0]] = data[1:]
        f.close()


def main():
    window_size = (800, 600)
    the_dataset = Dataset('numbers_items.txt')

    the_network = Network(25, 5, 10)
    np.set_printoptions(suppress=True, precision=3)
    the_display = Display(window_size, the_network, the_dataset)
    the_display.root.mainloop()


main()
import numpy as np


class NervousSystem:

    def __init__(self, input_size, output_size, hidden_size_list=None):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size_list = hidden_size_list if hidden_size_list is not None else []
        self.layer_size_list = []
        self.weight_list = []
        self.bias_list = []
        self.weight_init = .01
        self.num_layers = None

        self.init_weights()

    def init_weights(self):
        self.layer_size_list.append(self.input_size)
        for size in self.hidden_size_list:
            self.layer_size_list.append(size)
        self.layer_size_list.append(self.output_size)

        for i in range(len(self.layer_size_list) - 1):
            self.weight_list.append(self.create_layer_weight(self.layer_size_list[i], self.layer_size_list[i + 1]))
            self.bias_list.append(np.zeros((self.layer_size_list[i + 1], 1)))

        self.num_layers = len(self.weight_list)

    def create_layer_weight(self, input_size, output_size):
        return np.random.uniform(-self.weight_init, self.weight_init, size=(output_size, input_size))

    def update(self, x):
        # Ensure x is a column vector
        x = np.reshape(x, (x.shape[0], 1))

        # Loop through the layer and bias lists
        for i in range(self.num_layers):
            zx = self.bias_list[i] + self.weight_list[i] @ x
            x = 1 / (1 + np.exp(-zx))

        return x
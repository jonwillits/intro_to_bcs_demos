import tkinter as tk
import sys
import numpy as np
from tkinter import ttk


class Network:
    ############################################################################################################
    def __init__(self, input_size, hidden_size, output_size):

        self.input_size = input_size
        self.output_size = output_size
        self.weight_mean = 0
        self.weight_stdev = 0.0001

        self.init_network(hidden_size)

    ############################################################################################################
    def init_network(self, hidden_size):
        self.hidden_size = hidden_size
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
    def __init__(self, network, dataset):

        self.network = network
        self.dataset = dataset
        self.root = tk.Tk()
        self.root.title("Digit Recognition Neural Network")

        self.current_input = self.dataset.x[0]
        self.hidden_size = self.network.hidden_size
        self.num_epochs = 100
        self.learning_rate = 0.10
        self.cost_history = []

        self.init_display()
        self.draw_network()

    def init_display(self):
        self.interface_frame = tk.Frame(self.root, height=110, width=800, padx=0, pady=0, bg='black')
        self.interface_frame.pack()
        self.network_frame = tk.Frame(self.root, height=490, width=800, padx=0, pady=0)
        self.network_frame.pack()

        self.unit_info_canvas = tk.Canvas(self.network_frame, height=190, width=800, bg="#222222", bd=0,
                                        highlightthickness=0, relief='ridge')
        self.unit_info_canvas.pack()

        self.network_canvas = tk.Canvas(self.network_frame, height=300, width=800, bg="#000000", bd=0,
                                        highlightthickness=0, relief='ridge')
        self.network_canvas.pack()
        self.network_canvas.bind("<Button-1>", self.network_click)

        self.draw_interface()

    def draw_network(self):
        self.network_canvas.delete("all")
        self.draw_inputs()
        self.draw_input_layer()
        self.draw_hidden_layer()
        self.draw_output_layer()
        self.root.update()

    def draw_inputs(self):
        startx = 10
        starty = 10
        size = 20
        spacing = 8

        for i in range(10):
            number = self.dataset.number_list[i]
            the_tag = "n" + str(number)
            y1 = starty+(size+spacing)*i
            self.network_canvas.create_rectangle(startx, y1, startx+size, y1+size,
                                                 fill='grey', tags=the_tag)
            self.network_canvas.create_text(startx+10, y1+10, text=number, font="Arial 16 bold", fill='blue')

    def draw_input_layer(self):
        startx = 50
        starty = 45
        size = 40
        spacing = 1

        unit_counter = 0
        input_vector = np.copy(self.current_input)
        input_matrix = input_vector.reshape((5, 5))
        for i in range(input_matrix.shape[0]):
            for j in range(input_matrix.shape[1]):
                the_tag = "i" + str(unit_counter)
                if input_matrix[i, j] == 1:
                    color = "green"
                else:
                    color = "white"
                x1 = startx + (size + spacing) * i
                y1 = starty + (size + spacing) * j
                self.network_canvas.create_rectangle(x1, y1, x1 + size, y1 + size,
                                                     fill=color, tags=the_tag)
        self.network_canvas.create_text(150, 20, text="Input Layer", font="Arial 24 bold", fill='white')

    def draw_hidden_layer(self):
        startx = 350
        starty = 40
        size = 20
        spacing = 2

        h, o = self.network.feedforward(self.current_input)
        self.network_canvas.create_text(400, 20, text="Hidden Layer", font="Arial 24 bold", fill='white')
        for i in range(self.hidden_size):

            the_tag = "h" + str(i+1)
            y1 = starty+(size+spacing)*i
            color = self.get_hex_color(h[i])
            self.network_canvas.create_rectangle(startx, y1, startx+size, y1+size,
                                                 fill=color, tags=the_tag)
            if i == 9:
                startx += size+spacing
                starty -= 10*(size+spacing)

    def draw_output_layer(self):
        h, o = self.network.feedforward(self.current_input)
        self.network_canvas.create_text(600, 20, text="Output Layer", font="Arial 24 bold", fill='white')
        startx = 540
        starty = 40
        size = 22
        spacing = 2
        softmax = o / o.sum()

        for i in range(10):
            the_tag = "o" + str(i+1)
            color = self.get_hex_color(o[i])
            y1 = starty+(size+spacing)*i
            self.network_canvas.create_rectangle(startx, y1, startx+size, y1+size,
                                                 fill=color, tags=the_tag)
            self.network_canvas.create_text(startx+30, y1+10+2, text=i, font="Arial 14 bold", fill='white')
            value = "{:0.1f}%".format(100*softmax[i])
            bar_size = round(100*softmax[i])
            self.network_canvas.create_rectangle(startx+50, y1+4, startx+50+bar_size, y1+16, fill='blue')
            self.network_canvas.create_text(startx + 200, y1 + 10 + 2, text=value, font="Arial 12 bold", fill='white')

    def draw_interface(self):
        tk.Label(self.interface_frame, text="Training Epochs", bg='black', fg='white').place(x=20, y=5)
        v = tk.StringVar(self.root, value=self.num_epochs)
        self.epochs_entry = tk.Entry(self.interface_frame, width=6, textvariable=v, relief='flat', borderwidth=0)
        self.epochs_entry.place(x=150, y=5)

        tk.Label(self.interface_frame, text="Learning Rate", bg='black', fg='white').place(x=20, y=40)
        v = tk.StringVar(self.root, value=self.learning_rate)
        self.learning_rate_entry = tk.Entry(self.interface_frame, width=6, textvariable=v, relief='flat', borderwidth=0)
        self.learning_rate_entry.place(x=150, y=40)

        tk.Label(self.interface_frame, text="Hidden Size", bg='black', fg='white').place(x=20, y=75)
        v = tk.StringVar(self.root, value=self.hidden_size, )
        self.hidden_size_entry = tk.Entry(self.interface_frame, width=6, textvariable=v, relief='flat', borderwidth=0)
        self.hidden_size_entry.place(x=150, y=75)

        ttk.Style().configure("TButton", padding=0, relief="flat", background="white")
        self.train_button = ttk.Button(self.interface_frame, text="Train", width=4, command=self.train)
        self.train_button.place(x=250, y=25)
        self.reset_button = ttk.Button(self.interface_frame, text="Reset", width=4, command=self.reset)
        self.reset_button.place(x=250, y=60)

    def train(self):
        epoch_entry = self.epochs_entry.get()
        if isinstance(epoch_entry, int):
            if epoch_entry > 0:
                self.num_epochs = epoch_entry

        learning_rate_entry = self.learning_rate_entry.get()
        if isinstance(learning_rate_entry, float):
            if 0 < learning_rate_entry < 1:
                self.learning_rate = learning_rate_entry

        for i in range(self.num_epochs):
            epoch_cost_sum = 0
            for j in range(self.dataset.n):
                h, o = self.network.feedforward(self.dataset.x[j])
                o_cost = self.network.calc_cost(self.dataset.y[j], o)
                self.network.backpropogation(self.dataset.x[j], o, h, o_cost, self.learning_rate)
                epoch_cost_sum += (o_cost**2).sum()
            epoch_cost = epoch_cost_sum / self.dataset.n
            self.cost_history.append(epoch_cost)
            if i % 10 == 0:
                self.draw_network()
        self.draw_network()

    def network_click(self, event):
        x, y = event.x, event.y
        ids = self.network_canvas.find_overlapping(x - 5, y - 5, x + 5, y + 5)
        if len(ids) > 0:
            the_tag = self.network_canvas.itemcget(ids[0], "tags").split()[0]
            print(the_tag)
            if the_tag[0] == 'n':
                self.current_input = self.dataset.x[int(the_tag[1])]
                self.draw_network()

    def reset(self):
        hidden_size_entry = self.hidden_size_entry.get()
        if isinstance(hidden_size_entry, int):
            if 0 < hidden_size_entry > 21:
                self.hidden_size = hidden_size_entry
        self.current_input = self.dataset.x[0]
        self.cost_history = []
        self.network.init_network(self.hidden_size)
        self.draw_network()

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
        self.x = []
        self.y = []
        self.n = 0
        self.create_items()

    def read_file(self):
        f = open(self.file_path)
        line_counter = 0
        for line in f:
            data = (line.strip().strip('\n').strip()).split(',')
            self.number_list.append(data[0])
            self.number_index_dict[data[0]] = line_counter
            self.number_data_dict[data[0]] = data[1:]
        f.close()

    def create_items(self):
        for number in self.number_list:
            new_y = np.zeros([10], float)
            new_y[int(number)] = 1
            self.y.append(new_y)
            new_x_matrix = np.zeros([5, 5], float)
            number_data = self.number_data_dict[number]
            for i in range(len(number_data)):
                data = number_data[i].strip()
                x1 = int(data[0])
                x2 = int(data[1])
                new_x_matrix[x1, x2] = 1
            new_x_vector = new_x_matrix.flatten()
            self.x.append(new_x_vector)
            self.n += 1
        print(len(self.x), len(self.y))


def main():
    the_dataset = Dataset('digits_items.txt')

    the_network = Network(25, 8, 10)
    np.set_printoptions(suppress=True, precision=3)

    # for i in range(100):
    #     epoch_cost_sum = 0
    #     for j in range(the_dataset.n):
    #         h, o = the_network.feedforward(the_dataset.x[j])
    #         o_cost = the_network.calc_cost(the_dataset.y[j], o)
    #         the_network.backpropogation(the_dataset.x[j], o, h, o_cost, learning_rate)
    #         epoch_cost_sum += (o_cost**2).sum()
    #     epoch_cost = epoch_cost_sum / the_dataset.n
    #     print("{} {:0.5f}".format(i, epoch_cost))
    #
    # for i in range(the_dataset.n):
    #     h, o = the_network.feedforward(the_dataset.x[i])
    #     print("{}    {}".format(the_dataset.number_list[i], o))

    the_display = Display(the_network, the_dataset)
    the_display.root.mainloop()


main()

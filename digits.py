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

        self.selected_unit = "h1"
        self.current_input = np.copy(self.dataset.x[0])
        self.hidden_size = self.network.hidden_size
        self.num_epochs = 100
        self.learning_rate = 0.10
        self.cost_history = []

        self.init_display()
        self.update_display()

    def init_display(self):
        self.interface_frame = tk.Frame(self.root, height=35, width=800, padx=0, pady=0, bg='grey')
        self.interface_frame.pack()
        self.network_frame = tk.Frame(self.root, height=565, width=800, padx=0, pady=0)
        self.network_frame.pack()

        self.network_canvas = tk.Canvas(self.network_frame, height=300, width=800, bg="#000000", bd=0,
                                        highlightthickness=0, relief='ridge')
        self.network_canvas.pack()
        self.network_canvas.bind("<Button-1>", self.network_click)
        self.network_canvas.bind("<Double-Button-1>", self.network_doubleclick)

        self.weight_canvas = tk.Canvas(self.network_frame, height=265, width=800, bg="#000000", bd=0,
                                        highlightthickness=0, relief='ridge')
        self.weight_canvas.pack()



        self.draw_interface()

    def update_display(self):
        self.draw_network()
        self.draw_weights()

    def draw_network(self):
        self.network_canvas.delete("all")
        self.draw_inputs()
        self.draw_input_layer()
        self.draw_hidden_layer()
        self.draw_output_layer()
        self.root.update()

    def draw_weights(self):
        self.weight_canvas.delete("all")
        self.weight_canvas.create_line(0, 5, 800, 5, fill='white', width=2)
        self.weight_canvas.create_text(80, 25, text="Selected Unit: {}".format(self.selected_unit), font="Arial 14 bold", fill='white')
        if self.selected_unit[0] == 'i':
            self.weight_canvas.create_text(100, 50, text="Input-->Hidden Weights", font="Arial 11", fill='white')
            self.draw_hx_weights()
        elif self.selected_unit[0] == 'h':
            self.weight_canvas.create_text(100, 50, text="Input-->Hidden Weights", font="Arial 11", fill='white')
            self.weight_canvas.create_text(350, 50, text="Hidden-->Output Weights", font="Arial 11", fill='white')
            self.draw_hx_weights()
            self.draw_yh_weights()
        elif self.selected_unit[0] == 'o':
            self.weight_canvas.create_text(350, 50, text="Hidden-->Output Weights", font="Arial 11", fill='white')
            self.draw_yh_weights()
        self.root.update()

    def draw_hx_weights(self):
        startx = 30
        starty = 70
        size = 30
        spacing = 1

        index = int(self.selected_unit[1:])

        if self.selected_unit[0] == 'i':
            weight_vector = np.copy(self.network.h_x[:, index])
            x1 = startx
            for i in range(len(weight_vector)):
                color = self.get_hex_color(weight_vector[i])
                y1 = starty + (size + spacing) * i
                self.network_canvas.create_rectangle(x1, y1, x1 + size, y1 + size, fill=color)

        elif self.selected_unit[0] == 'h':
            print(self.network.h_x.shape)

            weight_vector = np.copy(self.network.h_x[index, :])
            weight_matrix = weight_vector.reshape((5, 5))
            print(weight_matrix.shape)
            for i in range(weight_matrix.shape[0]):
                for j in range(weight_matrix.shape[1]):
                    color = self.get_hex_color(weight_matrix[i, j])

                    x1 = startx + (size + spacing) * i
                    y1 = starty + (size + spacing) * j
                    print(x1, y1, x1 + size, y1 + size)
                    try:
                        self.weight_canvas.create_rectangle(x1, y1, x1 + size, y1 + size, fill=color)
                    except:
                        print(weight_matrix[i, j], color)

    def draw_yh_weights(self):
        pass

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
                unit_counter += 1
        self.network_canvas.create_text(150, 20, text="Input Layer", font="Arial 20 bold", fill='white')

    def draw_hidden_layer(self):
        startx = 350
        starty = 40
        size = 20
        spacing = 2

        h, o = self.network.feedforward(self.current_input)
        self.network_canvas.create_text(400, 20, text="Hidden Layer", font="Arial 20 bold", fill='white')
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
        self.network_canvas.create_text(620, 20, text="Output Layer", font="Arial 20 bold", fill='white')
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
        tk.Label(self.interface_frame, text="Training Epochs", bg='grey', fg='black').place(x=20, y=5)
        v = tk.StringVar(self.root, value=self.num_epochs)
        self.epochs_entry = tk.Entry(self.interface_frame, width=6, textvariable=v, relief='flat', borderwidth=0)
        self.epochs_entry.place(x=130, y=5)

        tk.Label(self.interface_frame, text="Learning Rate", bg='grey', fg='black').place(x=210, y=5)
        v = tk.StringVar(self.root, value=self.learning_rate)
        self.learning_rate_entry = tk.Entry(self.interface_frame, width=6, textvariable=v, relief='flat', borderwidth=0)
        self.learning_rate_entry.place(x=310, y=5)

        tk.Label(self.interface_frame, text="Hidden Size", bg='grey', fg='black').place(x=390, y=5)
        v = tk.StringVar(self.root, value=self.hidden_size, )
        self.hidden_size_entry = tk.Entry(self.interface_frame, width=6, textvariable=v, relief='flat', borderwidth=0)
        self.hidden_size_entry.place(x=480, y=5)

        ttk.Style().configure("TButton", padding=0, relief="flat", background="#111111", foreground='white')
        self.train_button = ttk.Button(self.interface_frame, text="Train", width=5, command=self.train)
        self.train_button.place(x=600, y=5)
        self.reset_button = ttk.Button(self.interface_frame, text="Reset", width=5, command=self.reset)
        self.reset_button.place(x=675, y=5)

    def train(self):
        epoch_entry = self.epochs_entry.get()
        try:
            new_epochs = int(epoch_entry)
            if new_epochs > 0:
                self.num_epochs = new_epochs
            else:
                self.epochs_entry.delete(0, tk.END)  # deletes the current value
                self.epochs_entry.insert(0, self.num_epochs)  # inserts new value assigned by 2nd parameter
        except:
            self.epochs_entry.delete(0, tk.END)  # deletes the current value
            self.epochs_entry.insert(0, self.num_epochs)  # inserts new value assigned by 2nd parameter

        learning_rate_entry = self.learning_rate_entry.get()
        try:
            new_lr = float(learning_rate_entry)
            if 0 <= new_lr <= 1:
                self.learning_rate = new_lr
            else:
                self.learning_rate_entry.delete(0, tk.END)
                self.learning_rate_entry.insert(0, self.learning_rate)
        except:
            self.learning_rate_entry.delete(0, tk.END)
            self.learning_rate_entry.insert(0, self.learning_rate)

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
                self.update_display()
        self.update_display()

    def network_click(self, event):
        the_tag = self.get_tags(event)
        if the_tag is not None:
            if the_tag[0] == 'n':
                self.current_input = np.copy(self.dataset.x[int(the_tag[1])])
                self.update_display()
            if the_tag[0] == 'i':
                self.selected_unit = the_tag
                self.update_display()
            if the_tag[0] == 'h':
                self.selected_unit = the_tag
                self.update_display()

    def network_doubleclick(self, event):
        the_tag = self.get_tags(event)
        if the_tag is not None:
            if the_tag[0] == 'i':
                index = int(the_tag[1:])

                if self.current_input[index] == 1:
                    self.current_input[index] = 0
                else:
                    self.current_input[index] = 1
                self.update_display()

    def reset(self):
        hidden_size_entry = self.hidden_size_entry.get()
        try:
            new_hidden_size = int(hidden_size_entry)
            if 0 < new_hidden_size <= 20:
                self.hidden_size = new_hidden_size
            else:
                self.hidden_size_entry.delete(0, tk.END)  # deletes the current value
                self.hidden_size_entry.insert(0, self.hidden_size)  # inserts new value assigned by 2nd parameter
        except:
            self.hidden_size_entry.delete(0, tk.END)  # deletes the current value
            self.hidden_size_entry.insert(0, self.hidden_size)  # inserts new value assigned by 2nd parameter

        self.current_input = np.copy(self.dataset.x[0])
        self.cost_history = []
        self.network.init_network(self.hidden_size)
        self.update_display()

    def get_tags(self, event):
        x, y = event.x, event.y
        ids = self.network_canvas.find_overlapping(x - 5, y - 5, x + 5, y + 5)
        if len(ids) > 0:
            the_tag = self.network_canvas.itemcget(ids[0], "tags").split()[0]
        else:
            the_tag = None
        return the_tag

    @staticmethod
    def quit_simulation():
        sys.exit()

    @staticmethod
    def get_hex_color(value):
        abs_value = 1 - abs(value)
        scaled_value = int(round(255 * abs_value, 0))
        print(scaled_value)
        if scaled_value < 0:
            scaled_value = 0
        if scaled_value > 255:
            scaled_value = 255
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

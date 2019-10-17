import tkinter as tk
import sys
import random
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

        self.selected_unit = None
        self.current_input = np.copy(self.dataset.x[0])
        self.hidden_size = self.network.hidden_size
        self.num_epochs = 100
        self.learning_rate = 0.10
        self.error_history = []
        self.current_epoch = 0

        self.init_display()
        self.update_display()

    def init_display(self):
        epoch_cost_sum = 0
        for i in range(self.dataset.n):
            h, o = self.network.feedforward(self.dataset.x[i])
            o_cost = self.network.calc_cost(self.dataset.y[i], o)
            epoch_cost_sum += (o_cost ** 2).sum()
        epoch_error = epoch_cost_sum / self.dataset.n
        print()
        self.error_history.append(epoch_error)

        self.interface_frame = tk.Frame(self.root, height=35, width=800, padx=0, pady=0, bg='grey')
        self.interface_frame.pack()

        self.network_frame = tk.Frame(self.root, height=300, width=790, padx=0, pady=0)
        self.network_frame.pack()

        self.info_frame = tk.Frame(self.root, height=265, width=790, padx=0, pady=0)
        self.info_frame.pack()

        self.network_canvas = tk.Canvas(self.network_frame, height=300, width=790, bg="#000000", bd=5,
                                        highlightthickness=0, relief='ridge')
        self.network_canvas.pack()
        self.network_canvas.bind("<Button-1>", self.network_click)
        self.network_canvas.bind("<Double-Button-1>", self.network_doubleclick)

        self.weight_canvas = tk.Canvas(self.info_frame, height=265, width=430, bg="#000000", bd=5,
                                       highlightthickness=0, relief='ridge')
        self.weight_canvas.pack(side=tk.LEFT)
        self.error_canvas = tk.Canvas(self.info_frame, height=265, width=350, bg="#000000", bd=5,
                                      highlightthickness=0, relief='ridge')
        self.error_canvas.pack(side=tk.LEFT)

        self.draw_interface()

    def update_display(self):
        self.draw_network()
        self.draw_weights()
        self.draw_error()

    def draw_error(self):
        x_is_0 = 40
        y_is_0 = 240
        x_scale = 300
        y_scale = 200

        self.error_canvas.delete("all")
        self.error_canvas.create_line(x_is_0, y_is_0, x_is_0+x_scale, y_is_0, fill='white', width=3)
        self.error_canvas.create_line(x_is_0, y_is_0, x_is_0, y_is_0-y_scale, fill='white', width=3)
        self.error_canvas.create_text(x_is_0+(0.5*x_scale), y_is_0+10, fill='white', text='Epochs')
        self.error_canvas.create_text(x_is_0-20, y_is_0-(0.5*y_scale), fill='white', text='Error')
        self.error_canvas.create_text(180, 20, fill='white', text='Error History', font="Arial 20 bold")

        if 1 < len(self.error_history) < 300:
            for i in range(len(self.error_history)-1):
                x1 = x_is_0 + (x_scale * (i / 300))
                y1 = y_is_0 - (y_scale * (self.error_history[i]/2.5))
                x2 = x_is_0 + (x_scale * ((i+1) / 300))
                y2 = y_is_0 - (y_scale * (self.error_history[i+1]/2.5))
                self.error_canvas.create_line(x1, y1, x2, y2, fill='yellow', width=2)

        self.root.update()

    def draw_network(self):
        self.network_canvas.delete("all")
        self.draw_inputs()
        self.draw_input_layer()
        self.draw_hidden_layer()
        self.draw_output_layer()
        self.root.update()

    def draw_weights(self):
        self.weight_canvas.delete("all")
        self.weight_canvas.create_text(230, 25, text="Selected Unit: {}".format(self.selected_unit), font="Arial 20 bold", fill='white')
        if self.selected_unit is not None:
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
        index = int(self.selected_unit[1:])-1

        if self.selected_unit[0] == 'i':
            startx = 90
            starty = 70
            size = 17
            spacing = 1
            weight_vector = np.copy(self.network.h_x[:, index])
            for i in range(len(weight_vector)):
                color = self.get_hex_color(weight_vector[i])
                x1 = startx
                y1 = starty + (size + spacing) * i
                self.weight_canvas.create_rectangle(x1, y1, x1 + size, y1 + size, fill=color)
                print(i, x1, y1, x1 + size, y1 + size)
                if i == 9:
                    print("HERE")
                    startx += size + spacing
                    starty -= 10 * (size + spacing)

        elif self.selected_unit[0] == 'h':
            startx = 30
            starty = 70
            size = 30
            spacing = 1
            weight_vector = np.copy(self.network.h_x[index, :])
            weight_matrix = weight_vector.reshape((5, 5))
            for i in range(weight_matrix.shape[0]):
                for j in range(weight_matrix.shape[1]):
                    color = self.get_hex_color(weight_matrix[i, j])

                    x1 = startx + (size + spacing) * i
                    y1 = starty + (size + spacing) * j
                    try:
                        self.weight_canvas.create_rectangle(x1, y1, x1 + size, y1 + size, fill=color)
                    except:
                        print(weight_matrix[i, j], color)

    def draw_yh_weights(self):
        index = int(self.selected_unit[1:])-1

        if self.selected_unit[0] == 'h':
            startx = 330
            starty = 65
            size = 18
            spacing = 1
            weight_vector = np.copy(self.network.o_h[:, index])
            for i in range(weight_vector.shape[0]):
                color = self.get_hex_color(weight_vector[i])
                x1 = startx
                y1 = starty + (size + spacing) * i
                self.weight_canvas.create_rectangle(x1, y1, x1 + size, y1 + size, fill=color)

        elif self.selected_unit[0] == 'o':
            startx = 330
            starty = 65
            size = 18
            spacing = 1
            weight_vector = np.copy(self.network.o_h[index, :])
            for i in range(weight_vector.shape[0]):
                color = self.get_hex_color(weight_vector[i])
                x1 = startx
                y1 = starty + (size + spacing) * i
                self.weight_canvas.create_rectangle(x1, y1, x1 + size, y1 + size, fill=color)
                if i == 9:
                    startx += size + spacing
                    starty -= 10 * (size + spacing)

    def draw_inputs(self):
        startx = 10
        starty = 10
        size = 20
        spacing = 8

        for i in range(10):
            number = self.dataset.number_list[i]
            the_tag = "n" + str(number)
            y1 = starty+(size+spacing)*i
            self.network_canvas.create_rectangle(startx, y1, startx+size, y1+size, fill='grey', tags=the_tag)
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
                    fcolor = "green"
                else:
                    fcolor = "white"

                if self.selected_unit == the_tag:
                    bcolor = 'yellow'
                else:
                    bcolor = 'black'
                x1 = startx + (size + spacing) * i
                y1 = starty + (size + spacing) * j
                self.network_canvas.create_rectangle(x1, y1, x1 + size, y1 + size,
                                                     outline=bcolor, fill=fcolor, tags=the_tag)
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
            fcolor = self.get_hex_color(h[i])
            if self.selected_unit == the_tag:
                bcolor = 'yellow'
            else:
                bcolor = 'black'
            self.network_canvas.create_rectangle(startx, y1, startx+size, y1+size, fill=fcolor, outline=bcolor, tags=the_tag)
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
            fcolor = self.get_hex_color(o[i])
            if self.selected_unit == the_tag:
                bcolor = 'yellow'
            else:
                bcolor = 'black'
            y1 = starty+(size+spacing)*i
            self.network_canvas.create_rectangle(startx, y1, startx+size, y1+size, fill=fcolor, outline=bcolor, tags=the_tag)
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

        ttk.Style().configure("TButton", padding=0, relief="flat", background="#EEEEEE", foreground='black')
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
            indexes = list(range(10))
            random.shuffle(indexes)

            for j in range(self.dataset.n):
                index = indexes[j]
                h, o = self.network.feedforward(self.dataset.x[index])
                o_cost = self.network.calc_cost(self.dataset.y[index], o)
                self.network.backpropogation(self.dataset.x[index], o, h, o_cost, self.learning_rate)
                epoch_cost_sum += (o_cost**2).sum()

            epoch_error = epoch_cost_sum / self.dataset.n
            self.current_epoch += 1
            print("Epoch: {}     Error: {:0.3f}".format(self.current_epoch, epoch_error))
            if i % 10 == 0:
                self.error_history.append(epoch_error)
                self.update_display()
        self.update_display()

    def network_click(self, event):
        the_tag = self.get_tags(event)
        if the_tag is not None:
            if the_tag[0] == 'n':
                self.current_input = np.copy(self.dataset.x[int(the_tag[1])])
                self.update_display()
            else:
                if the_tag == self.selected_unit:
                    self.selected_unit = None
                    self.update_display()
                else:
                    if the_tag[0] == 'i':
                        self.selected_unit = the_tag
                        self.update_display()
                    if the_tag[0] == 'h':
                        self.selected_unit = the_tag
                        self.update_display()
                    if the_tag[0] == 'o':
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
        self.error_history = []
        self.current_epoch = 0
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


def main():
    hidden_size = 8

    the_dataset = Dataset('digits_items.txt')

    the_network = Network(25, hidden_size, 10)
    np.set_printoptions(suppress=True, precision=3)

    the_display = Display(the_network, the_dataset)
    the_display.root.mainloop()


main()

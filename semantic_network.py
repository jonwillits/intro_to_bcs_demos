import tkinter as tk
import sys
import time
import numpy as np


class Network:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.learning_rate = 0.2
        self.decay_rate = 0.005
        self.init_network()

    def init_network(self):
        self.training_steps = 0
        self.time_steps = 0
        self.activation_history_list = []
        self.activations = np.zeros([self.num_nodes], float)
        self.activation_history_list.append(self.activations)
        self.weight_matrix = np.random.uniform(-1, 1, [self.num_nodes, self.num_nodes])

        self.activation_rate = []

    def train(self, x):
        self.training_steps += 1
        for i in range(len(x)):
            item = x[i]
            for j in range(self.num_nodes):
                for k in range(self.num_nodes):
                    self.weight_matrix[j, k] += self.learning_rate * item[j] * item[k]

    def next(self, selected_node_array):
        self.time_steps += 1
        net_input = np.dot((self.activations * self.decay_rate), self.weight_matrix)
        activations = np.tanh(net_input)

        for i in range(self.num_nodes):
            if selected_node_array[i]:
                activations[i] = 1

        self.activations = activations
        self.activation_history_list.append(self.activations)
        self.activation_rate.append(
            np.tanh(np.dot(self.activation_history_list[self.time_steps - 1], self.weight_matrix[0])))


class Display:
    def __init__(self, window_size, network, dataset):

        self.network = network
        self.dataset = dataset
        self.height = window_size[0]
        self.width = window_size[1]

        self.root = tk.Tk()

        self.root.title("Semantic Network")
        self.running = False

        self.node_coordinate_list = [(50, 240), (50, 270), (50, 300), (50, 330), (50, 360), (50, 390), (50, 420), (50, 450), (50, 480), (50, 510),
                                     (200, 240), (200, 270), (200, 300), (200, 330), (200, 360), (200, 390), (200, 420), (200, 450), (200, 480), (200, 510),
                                     (350, 240), (350, 270), (350, 300), (350, 330), (350, 360), (350, 390), (350, 420), (350, 450), (350, 480), (350, 510),
                                     (30, 90), (30, 120), (30, 150),  # category
                                     (150, 90), (150, 120), (150, 150),  # covering
                                     (270, 90), (270, 120), (270, 150),  # locomotion
                                     (390, 90), (390, 120), (390, 150),  # appendages
                                     (510, 90), (510, 120)  # diet
                                     #(500, 210), (500, 240), (500, 270), (500, 300), (500, 330), (500, 360), (500, 390), (500, 420)  # color
                                     ]
        self.node_size = 20
        self.text_offset = [40, 10]
        self.weight_size = 6
        self.selected_node_array = np.zeros([self.network.num_nodes], float)
        self.graph_selected_index = 0

        self.graph_selected_variable = tk.StringVar(self.root)
        self.graph_selected_variable.set(self.dataset.label_list[0])  # default value

        self.create_weight_frame()
        self.create_network_frame()
        self.create_activation_graph_frame()
        self.create_button_frame()

    def create_weight_frame(self):
        self.weight_frame = tk.Frame(self.root, width=self.width * .45, height=self.height * .62, padx=0, pady=0)
        self.weight_frame.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        self.weight_canvas = tk.Canvas(self.weight_frame, width=self.width * .45, height=self.height * .62, bg='white')
        self.weight_canvas.pack()
        self.update_weight_frame()

    def create_activation_graph_frame(self):
        self.graph_frame = tk.Frame(self.root, width=self.width * .45, height=self.height * .38, padx=0, pady=0, bg='white')
        self.graph_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)

        self.graph_title_canvas = tk.Canvas(self.graph_frame, height=self.height * .03, width=self.width*.25, bg="white", bd=0, highlightthickness=0, relief='ridge')
        self.graph_title_canvas.create_text(90, 10, font='Arial 12 bold', text='Activation Over Time')

        self.dropdown_menu = tk.OptionMenu(self.graph_frame, self.graph_selected_variable, *self.dataset.label_list)
        self.dropdown_menu.config(width=19, height=1, font=('Helvetica', 10))
        self.graph_selected_variable.trace("w", self.activation_graph_selection)
        self.top_filler_canvas = tk.Canvas(self.graph_frame, height=self.height * .05, width=self.width*.05, bg="white", bd=0, highlightthickness=0, relief='ridge')

        self.graph_data_canvas = tk.Canvas(self.graph_frame, height=self.height * .33, width=self.width*.45, bg="white", bd=0, highlightthickness=0, relief='ridge')

        self.graph_title_canvas.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        self.dropdown_menu.grid(row=0, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        self.top_filler_canvas.grid(row=0, column=2, ipadx=0, ipady=0, padx=0, pady=0)
        self.graph_data_canvas.grid(row=1, column=0, columnspan=3, ipadx=0, ipady=0, padx=0, pady=0)

        self.update_activation_graph_frame()

    def activation_graph_selection(self, *args):
        self.update_activation_graph_frame()

    def create_button_frame(self):
        self.button_frame = tk.Frame(self.root, width=self.width, height=self.height * .1, padx=0, pady=0)
        self.button_frame.grid(row=3, column=0, columnspan=2)
        self.train_button = tk.Button(self.button_frame, text="Train", fg="black", command=self.train)
        self.start_button = tk.Button(self.button_frame, text="Start", fg="black", command=self.start)
        self.next_button = tk.Button(self.button_frame, text="Next", fg="black", command=self.next)
        self.reset_button = tk.Button(self.button_frame, text="Reset", fg="black", command=self.reset)
        self.quit_button = tk.Button(self.button_frame, text="Quit", fg="black", command=self.quit_simulation)
        self.train_button.pack(side=tk.LEFT)
        self.start_button.pack(side=tk.LEFT)
        self.next_button.pack(side=tk.LEFT)
        self.reset_button.pack(side=tk.LEFT)
        self.quit_button.pack(side=tk.LEFT)

    def create_network_frame(self):
        self.network_frame = tk.Frame(self.root, width=self.width * .55, height=self.height * .9, padx=0, pady=0)
        self.network_frame.grid(row=0, column=1, rowspan=2)
        self.network_canvas = tk.Canvas(self.network_frame, width=self.width * .55, height=self.height, bg="white")
        self.network_canvas.pack()
        self.network_canvas.bind("<Button-1>", self.network_click)
        self.update_network_activation_frame()

    def network_click(self, event):
        x, y = event.x, event.y
        ids = self.network_canvas.find_overlapping(x, y, x, y)
        if len(ids) > 0:
            the_tag = self.network_canvas.itemcget(ids[0], "tags").split()[0]
            if the_tag in self.dataset.label_index_dict:
                the_index = self.dataset.label_index_dict[the_tag]
                if self.selected_node_array[the_index] == 1:
                    self.selected_node_array[the_index] = 0
                else:
                    self.selected_node_array[the_index] = 1
                self.update_network_activation_frame()

    def train(self):
        self.network.train(self.dataset.training_data)
        self.update_weight_frame()

    def start(self):
        if self.running:
            self.running = False
            self.start_button.config(text="Start")
        else:
            self.running = True
            self.start_button.config(text="Pause")

        while self.running:
            self.next()
            self.root.update()
            time.sleep(0.1)

    def next(self):
        self.network.next(self.selected_node_array)
        self.update_network_activation_frame()
        self.update_activation_graph_frame()

    def update_weight_frame(self):
        self.weight_canvas.delete("all")
        self.weight_canvas.create_text(140, 10,
                                       text="Network Weights (training steps={})".format(self.network.training_steps),
                                       font="Arial 12 bold")

        x = 60
        y = 20
        size = 6
        spacing = 3

        for i in range(self.network.num_nodes):
            self.weight_canvas.create_text(30, 23 + i * 9, font='Arial 7', text=self.dataset.label_list[i])
            for j in range(self.network.num_nodes):

                scaled_weight = self.network.weight_matrix[i, j] / 10
                if scaled_weight > 1:
                    scaled_weight = 1
                if scaled_weight < -1:
                    scaled_weight = -1
                color = self.get_hex_color(scaled_weight)

                self.weight_canvas.create_rectangle(x + j * (size + spacing), y + i * (size + spacing),
                                                    x + j * (spacing + size) + size, y + i * (spacing + size) + size,
                                                    outline="black", fill=color, width=1)

    def update_activation_graph_frame(self):
        self.graph_data_canvas.delete("all")

        selected_label = self.graph_selected_variable.get()
        selected_index = self.dataset.label_index_dict[selected_label]

        activation_history_matrix = np.array(self.network.activation_history_list)
        the_activations = activation_history_matrix[:, selected_index]


        max_act_count = 20
        top = 0
        bottom = 240
        left = 30
        right = 450
        y_middle = (bottom-top)/2
        x_middle = (right-left)/2

        self.graph_data_canvas.create_line(left, top, left, bottom, fill='black', width=2)
        self.graph_data_canvas.create_line(left, y_middle, right, y_middle, fill='silver', width=2)
        self.graph_data_canvas.create_text(left-10, y_middle, angle=90, text="Activation of " + selected_label)
        self.graph_data_canvas.create_text(x_middle+50, bottom+10, text="Time Steps")

        if len(the_activations) > 1:
            if len(the_activations) > max_act_count:
                recent_activations = the_activations[-max_act_count:]
                act_count = max_act_count
            else:
                recent_activations = the_activations
                act_count = len(recent_activations)
        else:
            recent_activations = None
            act_count = 1

        width = (right-left)/max_act_count

        for i in range(act_count-1):
            scaled_act1 = recent_activations[i] + 1
            scaled_act2 = recent_activations[i + 1] + 1
            y1 = bottom - y_middle * scaled_act1
            y2 = bottom - y_middle * scaled_act2
            x1 = left + i*width
            x2 = left + (i+1)*width
            self.graph_data_canvas.create_line(x1, y1, x2, y2, fill='black', width=2)

    def update_network_activation_frame(self):
        self.network_canvas.delete("all")
        self.network_canvas.create_text(160, 10,
                                        text="Network Activation (activation steps={})".format(self.network.time_steps),
                                        font="Arial 12 bold")
        for i in range(self.network.num_nodes):
            coords = self.node_coordinate_list[i]
            color = self.get_hex_color(self.network.activations[i])

            if self.selected_node_array[i] == 0:
                self.network_canvas.create_oval(coords[0],
                                                coords[1],
                                                coords[0] + self.node_size,
                                                coords[1] + self.node_size,
                                                outline="black", fill=color, width=1, tags=self.dataset.label_list[i])
                self.network_canvas.create_text(coords[0] + self.text_offset[0] + 2 * len(self.dataset.label_list[i]),
                                                coords[1] + self.text_offset[1],
                                                text=self.dataset.label_list[i], font="Arial 10", fill='black')
            else:
                self.network_canvas.create_oval(coords[0],
                                                coords[1],
                                                coords[0] + self.node_size,
                                                coords[1] + self.node_size,
                                                outline="black", fill=color, width=3, tags=self.dataset.label_list[i])

                self.network_canvas.create_text(coords[0] + self.text_offset[0] + 2 * len(self.dataset.label_list[i]),
                                                coords[1] + self.text_offset[1],
                                                text=self.dataset.label_list[i], font="Arial 10 bold", fill='green')

    def reset(self):
        self.network.init_network()
        self.selected_node_array = np.zeros([self.network.num_nodes], float)
        self.update_weight_frame()
        self.update_activation_graph_frame()
        self.update_network_activation_frame()

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
        self.read_file()
        self.create_summary_stats()

    def read_file(self):
        training_data = []
        f = open(self.file_path)
        line_counter = 0
        for line in f:
            data = (line.strip().strip('\n').strip()).split()
            if line_counter == 0:
                self.label_list = data
            else:
                training_data.append(np.array(data, float))
            line_counter += 1
        f.close()
        self.training_data = np.array(training_data, float)

    def create_summary_stats(self):
        self.num_items = len(self.training_data)
        self.num_features = len(self.label_list)
        self.label_index_dict = {}
        for i in range(self.num_features):
            self.label_index_dict[self.label_list[i]] = i


def main():
    window_size = (800, 1200)
    the_dataset = Dataset('semantic_network_items.txt')

    the_network = Network(the_dataset.num_features)
    np.set_printoptions(suppress=True, precision=3)
    the_display = Display(window_size, the_network, the_dataset)
    the_display.root.mainloop()


main()
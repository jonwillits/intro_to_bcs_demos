import tkinter as tk
import sys
import time
import numpy as np


class Network:
    def __init__(self):
        self.label_list = None
        self.training_data = None
        self.num_items = None
        self.num_nodes = None  # 0-14 animal names, 15-17 covering, 18-20 category, 21-23 movement, 24-30 color
        self.selected_activation_amount = 5.0

        self.learning_rate = 0.01
        self.currently_selected_index = None

        self.load_data()
        self.activations = np.random.uniform(-.5, .5, [self.num_nodes])
        self.weight_matrix = np.random.uniform(-.01, .01, [self.num_nodes, self.num_nodes])

    def load_data(self):
        f = open('semantic_network_items.txt')
        line_counter = 0
        training_data = []
        for line in f:
            data = (line.strip().strip('\n').strip()).split()
            if line_counter == 0:
                self.label_list = data
            else:
                training_data.append(np.array(data, float))
            line_counter += 1
        f.close()

        self.training_data = np.array(training_data, float)
        self.num_items = len(self.training_data)
        self.num_nodes = len(self.training_data[0])

    def train(self):
        for i in range(self.num_items):
            item = self.training_data[i]
            for j in range(self.num_nodes):
                for k in range(self.num_nodes):
                    if j <= k:
                        self.weight_matrix[j, k] += self.learning_rate * item[j] * item[k]
        for i in range(self.num_nodes):
            print(self.label_list[i], self.weight_matrix[i,:])

    def next(self):
        self.activations = np.tanh(np.dot(self.activations, self.weight_matrix))

        if self.currently_selected_index is not None:
            self.activations[self.currently_selected_index] = 1
        print(self.activations)

    def on_click(self, new_selected_index):
        if self.currently_selected_index == new_selected_index:
            self.currently_selected_index = None
        else:
            self.currently_selected_index = new_selected_index


class Display:
    def __init__(self, window_size, network):
        self.network = network
        self.height = window_size[0]
        self.width = window_size[1]

        self.root = tk.Tk()
        self.time_step = 0

        self.root.title("Semantic Network Time: {}".format(self.time_step))
        self.running = False

        self.node_coordinate_list = [(150, 300),
                                     (150, 330),
                                     (150, 360),
                                     (150, 390),
                                     (150, 420),
                                     (300, 300),
                                     (300, 330),
                                     (300, 360),
                                     (300, 390),
                                     (300, 420),
                                     (450, 300),
                                     (450, 330),
                                     (450, 360),
                                     (450, 390),
                                     (450, 420),

                                     (50, 90),
                                     (50, 120),
                                     (50, 150),

                                     (200, 90),
                                     (200, 120),
                                     (200, 150),

                                     (350, 90),
                                     (350, 120),
                                     (350, 150),

                                     (500, 60),
                                     (500, 90),
                                     (500, 120),
                                     (500, 150),
                                     (500, 180),
                                     (500, 210),
                                     (500, 240),
                                     ]
        self.node_size = 20
        self.text_offset = [40, 10]

        self.network_frame = None
        self.network_canvas = None
        self.graph_frame = None
        self.button_frame = None
        self.train_button = None
        self.start_button = None
        self.next_button = None
        self.quit_button = None

        self.create_network_frame()
        self.create_graph_frame()
        self.create_button_frame()

        self.selected_node_index = None

    def create_button_frame(self):
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=1, column=0, columnspan=2)
        self.train_button = tk.Button(self.button_frame, text="Train", fg="black", command=self.train)
        self.start_button = tk.Button(self.button_frame, text="Start", fg="black", command=self.start)
        self.next_button = tk.Button(self.button_frame, text="Next", fg="black", command=self.next)
        self.quit_button = tk.Button(self.button_frame, text="Quit", fg="black", command=self.quit_simulation)
        self.train_button.pack(side=tk.LEFT)
        self.start_button.pack(side=tk.LEFT)
        self.next_button.pack(side=tk.LEFT)
        self.quit_button.pack(side=tk.LEFT)

    def create_graph_frame(self):
        self.graph_frame = tk.Frame(self.root, width=self.width*.3, height=self.height, padx=0, pady=0)
        self.graph_frame.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)

    def create_network_frame(self):
        self.network_frame = tk.Frame(self.root, width=self.width*.7, height=self.height, padx=0, pady=0)
        self.network_frame.grid(row=0, column=1)
        self.network_canvas = tk.Canvas(self.network_frame, width=self.width*.7, height=self.height, bg="white")
        self.network_canvas.pack()
        self.update_network_window()

    def train(self):
        self.network.train()

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
        self.network.next()
        self.network_canvas.delete("all")
        self.update_network_window()
        self.time_step += 1
        self.root.title("Semantic Network Time: {}".format(self.time_step))

    def update_network_window(self):

        for i in range(self.network.num_nodes):
            coords = self.node_coordinate_list[i]
            color = self.get_hex_color(self.network.activations[i])

            self.network_canvas.create_oval(coords[0],
                                            coords[1],
                                            coords[0] + self.node_size,
                                            coords[1] + self.node_size,
                                            outline="black", fill=color, width=1, tags=i)
            self.network_canvas.create_text(coords[0] + self.text_offset[0] + 2*len(self.network.label_list[i]),
                                            coords[1] + self.text_offset[1],
                                            text=self.network.label_list[i])

    @staticmethod
    def quit_simulation():
        sys.exit()

    @staticmethod
    def get_hex_color(value):
        abs_value = 1 - abs(value)
        scaled_value = int(round(255*abs_value, 0))
        hex_value = hex(scaled_value)[2:]

        if len(hex_value) == 1:
            hex_value = "0" + hex_value

        if value > 0:
            return '#{}ff{}'.format(hex_value, hex_value)
        elif value < 0:
            return '#ff{}{}'.format(hex_value, hex_value)
        else:
            return "#ffffff"


def main():

    window_size = (500, 900)
    the_network = Network()
    np.set_printoptions(suppress=True, precision=4)
    the_display = Display(window_size, the_network)
    the_display.root.mainloop()


main()

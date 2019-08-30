import tkinter as tk
from tkinter import messagebox
import sys, math, time
import numpy as np

class Network:
    def __init__(self):
        self.selected_activation_amount = 10.0
        self.num_nodes = 5

        self.activations = np.random.uniform(-1, 1, [self.num_nodes])
        self.weight_matrix = np.random.uniform(-1, 1, [self.num_nodes, self.num_nodes])
        self.currently_selected_index = None
        self.label_list = ['lion', 'dog', 'whale', 'bat', 'rabbit']
        self.label_index_dict = {'lion': 0, 'dog': 1, 'whale': 2, 'bat': 3, 'rabbit': 4}
        np.set_printoptions(suppress=True, precision=4)

    def train_network(self):
        pass

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

#
#
class Display:
    def __init__(self, window_size, network):
        self.network = network
        self.height = window_size[0]
        self.width = window_size[1]

        self.root = tk.Tk()
        self.time_step = 0

        self.root.title("Semantic Network Time: {}".format(self.time_step))
        self.running = False

        self.node_coordinate_list = [(20, 20), (20, 420), (420, 20), (220, 220), (420, 420)]
        self.node_size = 20
        self.text_offset = 30

        self.network_frame = None
        self.network_canvas = None
        self.graph_frame = None
        self.button_frame = None

        self.create_network_frame()
        self.create_graph_frame()
        self.create_button_frame()

        self.selected_node_index = None
#
    def create_button_frame(self):
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=1, column=0, columnspan=2)
        self.start_button = tk.Button(self.button_frame, text="Start", fg="black", command=self.start)
        self.next_button = tk.Button(self.button_frame, text="Next", fg="black", command=self.next)
        self.quit_button = tk.Button(self.button_frame, text="Quit", fg="black", command=self.quit_simulation)
        self.start_button.pack(side=tk.LEFT)
        self.next_button.pack(side=tk.LEFT)
        self.quit_button.pack(side=tk.LEFT)

    def create_graph_frame(self):
        self.graph_frame = tk.Frame(self.root, width=self.width*.3, height=self.height, padx=0, pady=0)
        self.graph_frame.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
#
    def create_network_frame(self):
        self.network_frame = tk.Frame(self.root, width=self.width*.7, height=self.height, padx=0, pady=0)
        self.network_frame.grid(row=0, column=1)
        self.network_canvas = tk.Canvas(self.network_frame, width=self.width*.7, height=self.height, bg="white")
        self.network_canvas.pack()
        self.update_network_window()

            # self.network_canvas.tag_bind(i, "<Button-1>", self.onclick)
            # create the click binding for each oval
#
#     def onclick(self, event):
#         # what color should it be? Look call network.on_click to change the value
#         # then look at
#         #self.selected_node_index = i
#         self.network.on_click()
#
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
#
#     def update_graph_window(self):
#         # add a new time point and update the plot of the activation of the three category nodes
#         pass
#
    def update_network_window(self):

        for i in range(self.network.num_nodes):
            coords = self.node_coordinate_list[i]
            color = self.get_hex_color(self.network.activations[i])

            self.network_canvas.create_oval(coords[0], coords[1], coords[0] + self.node_size, coords[1] + self.node_size,
                                            outline="black", fill=color, width=1, tags=i)
            self.network_canvas.create_text(coords[0] + self.text_offset, coords[1] + self.text_offset,
                                            text=self.network.label_list[i])
#
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

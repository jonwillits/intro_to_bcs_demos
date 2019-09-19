import tkinter as tk
import numpy as np
import math


############################################################################################################
############################################################################################################
class NeuralNetwork:
    ############################################################################################################
    def __init__(self, dataset):
        self.dataset = dataset
        self.y_bias = None
        self.y_x = None

        self.init_network()

    ############################################################################################################
    def init_network(self):
        self.y_bias = np.random.normal(0, 0.5, [1, self.dataset.y_size])
        self.y_x = np.random.normal(0, 0.5, [self.dataset.y_size, self.dataset.x_size])

    ############################################################################################################
    def forward(self, x, act_f):
        z = np.dot(x, self.y_x.transpose()) + self.y_bias
        if act_f == 'Sigmoid':
            y = 1 / (1 + np.exp(-z))
        elif act_f == 'Threshold':
            y = np.where(z >= 0.0, 1, 0)
        else:
            y = z
        return y

    ############################################################################################################
    def train(self, x, y, learning_rate, act_f):
        y_predict = self.forward(x, act_f)
        y_cost = y - y_predict

        if act_f == 'Sigmoid':
            sigmoid_prime = 1/(1+np.exp(-y_predict)) * (1 - 1/(1+np.exp(-y_predict)))
            y_delta = y_cost * sigmoid_prime

        elif act_f == 'Threshold':
            y_delta = y_cost
        else:
            y_delta = y_cost

        self.y_bias += y_delta * learning_rate
        self.y_x += (np.dot(y_delta.transpose(), x) * learning_rate)

        return y_predict, y_cost, y_delta


############################################################################################################
############################################################################################################
class Dataset:

    def __init__(self):
        self.items = {"AND": (np.array([[[0, 0]], [[0, 1]], [[1, 0]], [[1, 1]]]),
                                     np.array([[[0]], [[0]], [[0]], [[1]]])),
                      "OR": (np.array([[[0, 0]], [[0, 1]], [[1, 0]], [[1, 1]]]),
                                     np.array([[[0]], [[1]], [[1]], [[1]]])),
                      "XOR": (np.array([[[0, 0]], [[0, 1]], [[1, 0]], [[1, 1]]]),
                                     np.array([[[0]], [[1]], [[1]], [[0]]]))
                      }
        self.n = 4
        self.x_size = 2
        self.y_size = 1


############################################################################################################
############################################################################################################
class Display:

    def __init__(self, network):
        self.network = network
        self.height = 600
        self.width = 800
        self.act_f = 'Sigmoid'
        self.learning_rate = 0.10

        self.root = tk.Tk()

        self.root.title("Neural Network")
        self.init_network_frame()

    def init_network_frame(self):
        self.dataset = 'AND'
        self.current_x = self.network.dataset.items[self.dataset][0][0]
        self.current_y = self.network.dataset.items[self.dataset][1][0]
        self.current_item = 0

        self.node_radius = 40
        self.thickness = 5
        self.y0_pos = (350, 100)
        self.x0_pos = (100, 300)
        self.x1_pos = (250, 500)
        self.x2_pos = (450, 500)

        self.network_frame = tk.Frame(self.root, height=self.height, width=self.width, padx=0, pady=0, bg='white')
        self.network_frame.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)

        self.network_canvas = tk.Canvas(self.network_frame, height=self.height, width=self.width, bg="grey", bd=0,
                                        highlightthickness=0, relief='ridge')
        self.network_canvas.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)

        self.network_canvas.bind("<Button-1>", self.network_click)
        self.draw_weights()
        self.draw_nodes()
        self.draw_items()

    def draw_nodes(self):
        x = self.current_x
        y = self.network.forward(x, self.act_f)
        self.y0 = self.network_canvas.create_oval(self.y0_pos[0]-self.node_radius, self.y0_pos[1]-self.node_radius,
                                                  self.y0_pos[0]+self.node_radius, self.y0_pos[1]+self.node_radius,
                                                  width=self.thickness, fill=self.get_hex_color(y[0][0]))
        self.network_canvas.create_text(self.y0_pos[0], self.y0_pos[1]-self.node_radius*1.5,
                                        text="y".format(y[0][0]), font="Arial 16 bold")
        self.network_canvas.create_text(self.y0_pos[0], self.y0_pos[1],
                                        text="{:0.3f}".format(y[0][0]), font="Arial 16 bold")

        self.x0 = self.network_canvas.create_oval(self.x0_pos[0] - self.node_radius, self.x0_pos[1] - self.node_radius,
                                                  self.x0_pos[0] + self.node_radius, self.x0_pos[1] + self.node_radius,
                                                  width=self.thickness, fill=self.get_hex_color(1))
        self.network_canvas.create_text(self.x0_pos[0], self.x0_pos[1]+self.node_radius*1.5,
                                        text="x0 (bias)", font="Arial 16 bold")
        self.network_canvas.create_text(self.x0_pos[0], self.x0_pos[1],
                                        text="1", font="Arial 16 bold")


        self.x1 = self.network_canvas.create_oval(self.x1_pos[0] - self.node_radius, self.x1_pos[1] - self.node_radius,
                                                  self.x1_pos[0] + self.node_radius, self.x1_pos[1] + self.node_radius,
                                                  width=self.thickness, fill=self.get_hex_color(x[0][0]))
        self.network_canvas.create_text(self.x1_pos[0], self.x1_pos[1]+self.node_radius*1.5,
                                        text="x1", font="Arial 16 bold")
        self.network_canvas.create_text(self.x1_pos[0], self.x1_pos[1],
                                        text="{:0.0f}".format(x[0][0]), font="Arial 16 bold")

        self.x2 = self.network_canvas.create_oval(self.x2_pos[0] - self.node_radius, self.x2_pos[1] - self.node_radius,
                                                  self.x2_pos[0] + self.node_radius, self.x2_pos[1] + self.node_radius,
                                                  width=self.thickness, fill=self.get_hex_color(x[0][1]))
        self.network_canvas.create_text(self.x2_pos[0], self.x2_pos[1]+self.node_radius*1.5,
                                        text="x2", font="Arial 16 bold")
        self.network_canvas.create_text(self.x2_pos[0], self.x2_pos[1],
                                        text="{:0.0f}".format(x[0][1]), font="Arial 16 bold")

    def draw_weights(self):
        b0_x1 = self.x0_pos[0]+(self.node_radius/(2**0.5))
        b0_x2 = self.y0_pos[0]
        b0_y1 = self.x0_pos[1]-(self.node_radius/(2**0.5))
        b0_y2 = self.y0_pos[1]+self.node_radius
        self.b0 = self.network_canvas.create_line(b0_x1, b0_y1, b0_x2, b0_y2,
                                                  width=self.thickness,
                                                  fill=self.get_hex_color(self.network.y_bias[0][0]))
        self.network_canvas.create_text(b0_y1-b0_x1+40, b0_x2-b0_y2-20,
                                        text="b0 = {:0.3f}".format(self.network.y_bias[0][0]),
                                        font="Arial 16 bold", fill="black")

        self.b1 = self.network_canvas.create_line(self.x1_pos[0], self.x1_pos[1]-self.node_radius,
                                                  self.y0_pos[0], self.y0_pos[1]+self.node_radius,
                                                  width=self.thickness, fill=self.get_hex_color(self.network.y_x[0][0]))
        self.network_canvas.create_text(245, 325,
                                        text="b1 = {:0.3f}".format(self.network.y_x[0][0]),
                                        font="Arial 16 bold", fill="black")


        self.b2 = self.network_canvas.create_line(self.x2_pos[0], self.x2_pos[1]-self.node_radius,
                                                  self.y0_pos[0], self.y0_pos[1]+self.node_radius,
                                                  width=self.thickness, fill=self.get_hex_color(self.network.y_x[0][1]))
        self.network_canvas.create_text(455, 325,
                                        text="b2 = {:0.3f}".format(self.network.y_x[0][1]),
                                        font="Arial 16 bold", fill="black")

    def draw_items(self):
        header = "x1     x2        y"
        self.network_canvas.create_text(703, 50, text=header, font="Arial 16 bold", fill="black")
        self.network_canvas.create_line(650, 70, 760, 70,
                                        width=self.thickness, fill="black")
        self.network_canvas.create_line(722, 30, 722, 190,
                                        width=self.thickness, fill="black")
        for i in range(self.network.dataset.n):
            x = self.network.dataset.items[self.dataset][0][i][0]
            y = self.network.dataset.items[self.dataset][1][i][0]
            items = "{:0.0f}       {:0.0f}        {:0.0f}".format(x[0], x[1], y[0])
            self.network_canvas.create_text(705, 55+(i+1)*30, text=items, font="Arial 16 bold", fill="black", tags=i)

    @staticmethod
    def network_click(event):
        print(event)

    @staticmethod
    def get_hex_color(value):
        if value > 1:
            value = 1
        if value < -1:
            value = -1

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

############################################################################################################
############################################################################################################
def main():
    the_datasets = Dataset()
    the_network = NeuralNetwork(the_datasets)
    np.set_printoptions(suppress=True, precision=3)
    the_display = Display(the_network)
    the_display.root.mainloop()


main()

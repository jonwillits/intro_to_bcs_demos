import tkinter as tk
from tkinter import ttk
import numpy as np
import sys
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
    def net_input(self, x):
        z = np.dot(x, self.y_x.transpose()) + self.y_bias
        return z

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

        y_predict = None
        y_cost = None
        y_delta = None

        for i in range(x.shape[0]):
            xi = x[i]
            yi = y[i]

            y_predict = self.forward(xi, act_f)
            y_cost = yi - y_predict

            if act_f == 'Sigmoid':
                sigmoid_prime = 1/(1+np.exp(-y_predict)) * (1 - 1/(1+np.exp(-y_predict)))
                y_delta = y_cost * sigmoid_prime

            elif act_f == 'Threshold':
                y_delta = y_cost
            else:
                y_delta = y_cost

            self.y_bias += y_delta * learning_rate
            self.y_x += y_delta.transpose() * xi * learning_rate

        return y_predict, y_cost, y_delta


############################################################################################################
############################################################################################################
class Dataset:
    def __init__(self):
        self.items = {"AND": (np.array([[0, 0], [0, 1], [1, 0], [1, 1]]),
                              np.array([[0], [0], [0], [1]])),
                      "OR": (np.array([[0, 0], [0, 1], [1, 0], [1, 1]]),
                              np.array([[0], [1], [1], [1]])),
                      "XOR": (np.array([[0, 0], [0, 1], [1, 0], [1, 1]]),
                              np.array([[0], [1], [1], [0]])),
                      "x1": (np.array([[0, 0], [0, 1], [1, 0], [1, 1]]),
                              np.array([[0], [0], [1], [1]])),
                      "x2": (np.array([[0, 0], [0, 1], [1, 0], [1, 1]]),
                              np.array([[0], [1], [0], [1]]))
                      }
        self.n = 4
        self.x_size = 2
        self.y_size = 1


############################################################################################################
############################################################################################################
class Display:
    def __init__(self, network):
        self.network = network
        self.height = 580
        self.width = 800
        self.act_f = 'Sigmoid'
        self.learning_rate = 0.10

        self.dataset = 'AND'
        self.current_item_index = 0
        self.current_x = self.network.dataset.items[self.dataset][0][self.current_item_index]
        self.current_y = self.network.dataset.items[self.dataset][1][self.current_item_index]

        self.node_radius = 30
        self.thickness = 3
        self.y0_pos = (350, 200)
        self.x0_pos = (100, 350)
        self.x1_pos = (250, 500)
        self.x2_pos = (450, 500)

        self.root = tk.Tk()

        self.root.title("Neural Network")
        self.init_display()
        self.draw_network_frame()
        self.weight_window = None

    def init_display(self):
        self.network_frame = tk.Frame(self.root, height=self.height-30, width=self.width, padx=0, pady=0)
        self.network_frame.pack()
        self.network_canvas = tk.Canvas(self.network_frame, height=self.height, width=self.width, bg="grey", bd=0,
                                        highlightthickness=0, relief='ridge')
        self.network_canvas.pack()
        self.network_canvas.bind("<Button-1>", self.network_click)

        self.button_frame = tk.Frame(self.root, height=30, width=self.width, padx=0, pady=0)
        self.button_frame.pack()
        ttk.Style().configure("TButton", padding=4, relief="flat", background="red")
        ttk.Button(self.button_frame, text="Train 1x", command=self.train1).pack(side=tk.LEFT)
        ttk.Button(self.button_frame, text="Train 10x", command=self.train10).pack(side=tk.LEFT)
        ttk.Button(self.button_frame, text="Train 100x", command=self.train100).pack(side=tk.LEFT)
        ttk.Button(self.button_frame, text="Reset", command=self.reset).pack(side=tk.LEFT)
        ttk.Button(self.button_frame, text="Quit", command=self.quit).pack(side=tk.LEFT)

    def train(self):
        x = self.network.dataset.items[self.dataset][0]
        y = self.network.dataset.items[self.dataset][1]

        self.network.train(x, y, self.learning_rate, self.act_f)

    def train10(self):
        for i in range(10):
            self.train()
        self.draw_network_frame()

    def train100(self):
        for i in range(100):
            self.train()
        self.draw_network_frame()

    def train1(self):
        self.train()
        self.draw_network_frame()

    def reset(self):
        self.network.init_network()
        self.draw_network_frame()
        self.root.update()

    @staticmethod
    def quit():
        sys.exit()

    def draw_network_frame(self):
        self.network_canvas.delete("all")
        self.draw_weights()
        self.draw_nodes()
        self.draw_items()
        self.draw_boundary()
        self.draw_activation_functions()
        self.root.update()

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
                                                  width=self.thickness, fill=self.get_hex_color(x[0]))
        self.network_canvas.create_text(self.x1_pos[0], self.x1_pos[1]+self.node_radius*1.5,
                                        text="x1", font="Arial 16 bold")
        self.network_canvas.create_text(self.x1_pos[0], self.x1_pos[1],
                                        text="{:0.0f}".format(x[0]), font="Arial 16 bold")

        self.x2 = self.network_canvas.create_oval(self.x2_pos[0] - self.node_radius, self.x2_pos[1] - self.node_radius,
                                                  self.x2_pos[0] + self.node_radius, self.x2_pos[1] + self.node_radius,
                                                  width=self.thickness, fill=self.get_hex_color(x[1]))
        self.network_canvas.create_text(self.x2_pos[0], self.x2_pos[1]+self.node_radius*1.5,
                                        text="x2", font="Arial 16 bold")
        self.network_canvas.create_text(self.x2_pos[0], self.x2_pos[1],
                                        text="{:0.0f}".format(x[1]), font="Arial 16 bold")

    def draw_weights(self):
        b0_x1 = self.x0_pos[0]+(self.node_radius/(2**0.5))
        b0_x2 = self.y0_pos[0]
        b0_y1 = self.x0_pos[1]-(self.node_radius/(2**0.5))
        b0_y2 = self.y0_pos[1]+self.node_radius
        self.b0 = self.network_canvas.create_line(b0_x1, b0_y1, b0_x2, b0_y2,
                                                  width=self.thickness,
                                                  fill=self.get_hex_color(self.network.y_bias[0][0]))

        self.network_canvas.create_text(self.y0_pos[0]-160, self.y0_pos[1]+80,
                                        text="b0 = {:0.3f}".format(self.network.y_bias[0][0]),
                                        font="Arial 16 bold", fill="black", tags='b0')

        self.b1 = self.network_canvas.create_line(self.x1_pos[0], self.x1_pos[1]-self.node_radius,
                                                  self.y0_pos[0], self.y0_pos[1]+self.node_radius,
                                                  width=self.thickness, fill=self.get_hex_color(self.network.y_x[0][0]))
        self.network_canvas.create_text(self.y0_pos[0]-80, self.y0_pos[1]+150,
                                        text="b1 = {:0.3f}".format(self.network.y_x[0][0]),
                                        font="Arial 16 bold", fill="black", tags='b1')


        self.b2 = self.network_canvas.create_line(self.x2_pos[0], self.x2_pos[1]-self.node_radius,
                                                  self.y0_pos[0], self.y0_pos[1]+self.node_radius,
                                                  width=self.thickness, fill=self.get_hex_color(self.network.y_x[0][1]))
        self.network_canvas.create_text(self.y0_pos[0]+80, self.y0_pos[1]+150,
                                        text="b2 = {:0.3f}".format(self.network.y_x[0][1]),
                                        font="Arial 16 bold", fill="black", tags='b2')

    def draw_items(self):
        start_x = 645
        start_y = 50
        button_height = 32
        button_width = 60

        self.network_canvas.create_text(start_x, start_y, text="Dataset:", font="Arial 20 bold", fill="#000000")
        self.network_canvas.create_rectangle(start_x+50, start_y-10, start_x+button_width+50, button_height+button_height, fill="#AAAAAA", activefill="black", tags='dataset_button')
        self.network_canvas.create_text(start_x + 80, start_y+2, text=self.dataset, font="Arial 16 bold", fill="#444444", tags='dataset_button')

        header = "x1     x2        y    prediction"
        self.network_canvas.create_text(start_x + 50, start_y+35, text=header, font="Arial 16 bold", fill="black")
        self.network_canvas.create_line(start_x-70, start_y+50, start_x+145, start_y+50,
                                        width=self.thickness, fill="black")
        self.network_canvas.create_line(start_x+30, start_y+30, start_x+30, start_y+170,
                                        width=self.thickness, fill="black")
        for i in range(self.network.dataset.n):
            x = self.network.dataset.items[self.dataset][0][i]
            y = self.network.dataset.items[self.dataset][1][i][0]
            y_predict = self.network.forward(x, self.act_f)
            items = "{:0.0f}       {:0.0f}         {:0.0f}     {:0.3f}".format(x[0], x[1], y, y_predict[0,0])
            tag = "item" + str(i)
            self.network_canvas.create_text(start_x+40, start_y+35+(i+1)*30, text=items, font="Arial 16 bold", fill="black", tags=tag)

    def draw_boundary(self):

        self.network_canvas.create_text(665, 350, text="Decision Boundary", font="Arial 20 bold", fill="#000000")
        precision = 0.01
        y1 = -100
        n = 100
        y1_predict = 0
        while abs(y1_predict - 0.50) > precision:
            y1_predict = self.network.forward([0, y1], self.act_f)[0, 0]
            y1 += 1/n
            if y1 > 100:
                break
        y2 = -100
        n = 100
        y2_predict = 0
        while abs(y2_predict - 0.50) > precision:
            y2_predict = self.network.forward([1, y2], self.act_f)[0, 0]
            y2 += 1/n
            if y2 > 100:
                break
        m = (y2-y1)
        b = y1
        equation = "y = {:0.3f}x + {:0.3f}".format(m, b)
        self.network_canvas.create_text(665, 380, text=equation, font="Arial 14 bold", fill="#000000")
        x_is_0 = 620
        y_is_0 = 540
        scale = 100

        coord_list = []
        x = -1
        for i in range(300):
            y = m * x + b
            if -1 <= y <= 2:
                coord_list.append((x, y))
            x += 0.01

        self.network_canvas.create_line(x_is_0, y_is_0, x_is_0+scale, y_is_0, width=self.thickness)
        self.network_canvas.create_line(x_is_0, y_is_0, x_is_0, y_is_0-scale, width=self.thickness)
        self.network_canvas.create_line(x_is_0, y_is_0-scale, x_is_0 + scale, y_is_0-scale, width=self.thickness)
        self.network_canvas.create_line(x_is_0+scale, y_is_0, x_is_0 + scale, y_is_0-scale, width=self.thickness)

        if len(coord_list) > 1:
            self.network_canvas.create_line(x_is_0+coord_list[0][0]*scale,
                                            y_is_0-coord_list[0][1]*scale,
                                            x_is_0 + coord_list[-1][0] * scale,
                                            y_is_0 - coord_list[-1][1] * scale,
                                            width=self.thickness, fill='yellow')

        x_is_0 = 620
        y_is_0 = 440
        scale = 100
        node_radius = 4
        for i in range(self.network.dataset.n):
            x1 = self.network.dataset.items[self.dataset][0][i][0]
            x2 = self.network.dataset.items[self.dataset][0][i][1]
            y = self.network.dataset.items[self.dataset][1][i][0]
            if y == 1:
                color = 'green'
            else:
                color = 'red'
            self.network_canvas.create_oval(x_is_0 + scale * x1 - node_radius,
                                            y_is_0 + scale * abs(x2 - 1) - node_radius,
                                            x_is_0 + scale * x1 + node_radius,
                                            y_is_0 + scale * abs(x2 - 1) + node_radius,
                                            fill=color)
            label = "({},{})".format(x1, x2)
            self.network_canvas.create_text(590 + 150 * x1, 420 + 140 * abs(x2 - 1), text=label, font="Arial 14 bold",
                                            fill="#000000")

    def draw_activation_functions(self):
        x_is_min = 40
        y_is_0 = 140
        x_scale = 200
        y_scale = 100

        intervals = np.linspace(-5, 5, 100)
        curve_list = []
        for z in intervals:
            y = 1 / (1 + math.exp(-z))
            curve_list.append((z, y))
            print(z, y)
        for i in range(len(intervals)-1):
            x1 = x_is_min + (x_scale * (curve_list[i][0] + 5)) / 10
            y1 = y_is_0 - curve_list[i][1] * y_scale
            x2 = x_is_min + (x_scale * (curve_list[i+1][0] + 5)) / 10
            y2 = y_is_0 - curve_list[i+1][1] * y_scale
            self.network_canvas.create_line(x1, y1, x2, y2, width=self.thickness, fill='yellow')

        x = self.current_x
        z = self.network.net_input(x)[0,0]
        y = self.network.forward(x, self.act_f)[0,0]
        print(x, z, y)
        print('x1={} + {}*({}+5)'.format(x_is_min, x_scale, z))
        x1 = x_is_min + (x_scale*(z+5))/10
        y1 = y_is_0 - y*y_scale
        x2 = x_is_min + (x_scale*(z+5))/10
        y2 = y_is_0 - y*y_scale
        print((x1, y1), (x2, y2))
        self.network_canvas.create_line(x1, y_is_0, x2, y_is_0-y_scale, width=self.thickness, fill='orange')
        self.network_canvas.create_line(x_is_min, y1, x_is_min+x_scale, y2, width=self.thickness, fill='orange')

        self.network_canvas.create_text(x_is_min+x_scale*0.5, y_is_0-y_scale-30, text="y Activation Function", font="Arial 14 bold", fill="#000000")
        self.network_canvas.create_text(x_is_min+x_scale*0.5, y_is_0-y_scale-15, text="y = 1 / (1 + e^-z)", font="Arial 12 bold",
                                        fill="#000000")
        self.network_canvas.create_text(x_is_min+x_scale*0.5, y_is_0+10, text="z = 0", font="Arial 11 bold", fill="#000000")
        self.network_canvas.create_text(x_is_min+x_scale, y_is_0+10, text="z = +5", font="Arial 11 bold", fill="#000000")
        self.network_canvas.create_text(x_is_min, y_is_0+10, text="z = -5", font="Arial 11 bold", fill="#000000")
        self.network_canvas.create_text(x_is_min+x_scale*0.5-13, y_is_0-10, text="y=0", font="Arial 11 bold", fill="#000000")
        self.network_canvas.create_text(x_is_min+x_scale*0.5 - 16, y_is_0 - 0.5*y_scale, text="y=0.5", font="Arial 11 bold", fill="#000000")
        self.network_canvas.create_text(x_is_min+x_scale*0.5 - 13, y_is_0 - y_scale, text="y=1", font="Arial 11 bold", fill="#000000")
        self.network_canvas.create_text(x_is_min+x_scale*0.5, y_is_0 + 25, text="z = b0*1 + b1*x1 + b2*x2", font="Arial 11 bold",
                                        fill="#000000")

        b0 = self.network.y_bias[0, 0]
        b1 = self.network.y_x[0, 0]
        b2 = self.network.y_x[0, 1]
        self.network_canvas.create_text(x_is_min+x_scale*0.5, y_is_0 + 40,
                                        text="z = {:0.2f} + {:0.2f} + {:0.2f} = {:0.2f}".format(b0, b1*x[0], b2*x[1], z),
                                        font="Arial 11 bold",
                                        fill="#000000")

        self.network_canvas.create_line(x_is_min+x_scale*0.5, y_is_0, x_is_min+x_scale*0.5, y_is_0-y_scale, width=self.thickness)
        self.network_canvas.create_line(x_is_min, y_is_0, x_is_min+x_scale, y_is_0, width=self.thickness)

    def network_click(self, event):
        x, y = event.x, event.y
        ids = self.network_canvas.find_overlapping(x-5, y-5, x+5, y+5)
        if len(ids) > 0:
            the_tag = self.network_canvas.itemcget(ids[0], "tags").split()[0]
            if the_tag in ['item0', 'item1', 'item2', 'item3']:
                self.current_item_index = int(the_tag[-1])
                self.current_x = self.network.dataset.items[self.dataset][0][self.current_item_index]
                self.current_y = self.network.dataset.items[self.dataset][1][self.current_item_index]
                self.draw_network_frame()
            elif the_tag == 'dataset_button':
                if self.dataset == 'AND':
                    self.dataset = 'OR'
                elif self.dataset == 'OR':
                    self.dataset = 'XOR'
                elif self.dataset == 'XOR':
                    self.dataset = 'x1'
                elif self.dataset == 'x1':
                    self.dataset = 'x2'
                elif self.dataset == 'x2':
                    self.dataset = 'AND'
                self.draw_network_frame()
            elif the_tag in ['b0', 'b1', 'b2']:
                tk.Message(text='Change Weight?')
                d = GetWeightDialog(self, the_tag)
                self.root.wait_window(d.top)
                self.draw_network_frame()

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
class GetWeightDialog:
    def __init__(self, display, the_tag):
        self.display = display
        top = self.top = tk.Toplevel(display.root)
        self.the_tag = the_tag
        tk.Label(top, text="Value").pack()
        self.e = tk.Entry(top)
        self.e.pack(padx=5)
        b = ttk.Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        value = self.e.get()
        if self.the_tag == 'b0':
            self.display.network.y_bias[0, 0] = float(value)
        if self.the_tag == 'b1':
            self.display.network.y_x[0,0] = float(value)
        if self.the_tag == 'b2':
            self.display.network.y_x[0,1] = float(value)
        self.top.destroy()



############################################################################################################
############################################################################################################
def main():
    the_datasets = Dataset()
    the_network = NeuralNetwork(the_datasets)
    np.set_printoptions(suppress=True, precision=3)
    the_display = Display(the_network)
    the_display.root.mainloop()


main()

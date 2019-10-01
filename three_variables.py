import tkinter as tk
from tkinter import messagebox
import sys, math


class Agent:

    def __init__(self):
        self.variable_list = [1, 8, 0]
        self.variable_label_list = ['Exercise (hrs.)', 'Sleep (hrs.)', 'Happiness']
        self.variable_minmax_list = [(0, 8), (0, 16), (-1, 1)]
        self.history_matrix = []

    def next(self):
        self.history_matrix.append(self.variable_list.copy())

        # assume that variable_list[0] represents amount of exercise, in (0, 8) hours
        # assume that variable_list[1] represents amount of sleep, in (0, 16) hours
        # assume that variable_list[2] represents amount of happiness, in (-1, 1) undefined mental state units        ​
        # parameters should be tweaked to changed behavior of system/find something that makes visual sense
        # parameters are defined by matrix whose entries are the coefficients of E, S, and H (in that order within rows),
        # where the rows are dE/dt, dS/dt, and dH/dt (in that order)
        coeff_matrix = [[0, 1, 1], [1, 1, 1], [1, 1, 1]]

        delta_exercise = -coeff_matrix[0][1] * self.variable_list[1] + coeff_matrix[0][2] * self.variable_list[2]
        delta_sleep = coeff_matrix[1][0] * self.variable_list[0] - coeff_matrix[1][1] * self.variable_list[1] - \
                      coeff_matrix[1][2] * self.variable_list[2]
        delta_happiness = coeff_matrix[2][0] * self.variable_list[0] + coeff_matrix[2][1] * self.variable_list[1] - \
                          coeff_matrix[2][2] * self.variable_list[2]
        # interim variables representing next timestep values before rescaling to appropriate ranges
        interim_exercise = self.variable_list[0] + delta_exercise
        interim_sleep = self.variable_list[1] + delta_sleep
        interim_happiness = self.variable_list[2] + delta_happiness
        # rescaling interim variables into appropriate ranges and reassigning values of {exercise, sleep, happiness} at next time step
        # note that this rescaling is very crude and sort of becomes a parameter itself.
        # it will cause exercise and sleep to be skewed higher because the input exercise and sleep values were positive
        self.variable_list[0] = 4 + 4 * (2 / math.pi) * math.atan(interim_exercise)
        self.variable_list[1] = 8 + 8 * (2 / math.pi) * math.atan(interim_sleep)
        self.variable_list[2] = (2 / math.pi) * math.atan(interim_happiness)


class Display:

    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Three Variable Simulation")
        self.running = False
        self.day = 0
        self.last_2D = None

        self.agent = Agent()

        self.create_single_var_windows()
        self.create_all_var_window()
        self.create_data_window()
        self.create_buttons()

    def create_single_var_windows(self):
        self.single_var_frame = tk.Frame(self.root, width=350, height=700, padx=0, pady=0)
        self.single_var_frame.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        self.single_variable_canvas_list = []

        for i in range(3):
            new_canvas = tk.Canvas(self.single_var_frame, width=350, height=232, bg='white')
            new_canvas.pack()
            self.single_variable_canvas_list.append(new_canvas)
            new_canvas.create_line(20, 210, 340, 210, fill='black', width=2)
            new_canvas.create_line(20, 210, 20, 20, fill='black', width=2)
            try:
                new_canvas.create_text(5, 150, anchor="nw", angle=90, text=self.agent.variable_label_list[i])
            except:
                new_canvas.create_text(5, 150, text=self.agent.variable_label_list[i])
            new_canvas.create_text(175, 220, text="Day")

    def create_all_var_window(self):
        self.all_vars_frame = tk.Frame(self.root, width=730, height=700, padx=0, pady=0)
        self.all_vars_frame.grid(row=0, column=1)
        self.all_vars_canvas = tk.Canvas(self.all_vars_frame, width=730, height=700, bg="white")
        self.all_vars_canvas.pack()

        self.all_vars_canvas.create_line(350, 350, 715, 350, fill='black', width=2)
        self.all_vars_canvas.create_text(700, 375, text="Sleep(hrs.)")
        self.all_vars_canvas.create_line(350, 350, 350, 10, fill='black', width=2)
        self.all_vars_canvas.create_text(390, 10, text="Happiness")
        self.all_vars_canvas.create_line(350, 350, 100, 570, fill='black', width=2)
        self.all_vars_canvas.create_text(100, 590, text="Exercise(min.)")

    def create_data_window(self):
        self.data_frame = tk.Frame(self.root, width=300, height=700, padx=0, pady=0)
        self.data_frame.grid(row=0, column=2)
        self.data_canvas = tk.Canvas(self.data_frame, width=300, height=700, bg='white')
        self.data_canvas.pack()
        self.entry_list = []

        for i in range(3):
            new_label = tk.Label(self.data_canvas, text=self.agent.variable_label_list[i], font=("Helvetica", 9),
                                 bg='white')
            new_label.place(x=50 + 80 * i, y=10)
            v = tk.StringVar(self.data_canvas, value=str(self.agent.variable_list[i]))
            new_entry = tk.Entry(self.data_canvas, width=5, textvariable=v)
            new_entry.place(x=50 + 80 * i, y=30)
            self.entry_list.append(new_entry)

    def create_buttons(self):
        self.button_frame = tk.Frame(self.root, width=1280, height=20, padx=0, pady=0)
        self.button_frame.grid(row=3, column=0, columnspan=3)
        self.next_button = tk.Button(self.button_frame, text="Next", fg="black", command=self.next, width=10)
        self.next_button.pack(side=tk.LEFT)
        self.quit_button = tk.Button(self.button_frame, text="Quit", fg="black", command=self.quit_simulation, width=10)
        self.quit_button.pack(side=tk.LEFT)

    def process_entry_input(self):
        all_ok = True

        for i in range(3):
            try:
                value = float(self.entry_list[i].get())
            except:
                messagebox.showerror("Error", "{} Value must be a number".format(self.agent.variable_label_list[i]))
                return False

            if self.agent.variable_minmax_list[i][0] <= value <= self.agent.variable_minmax_list[i][1]:
                self.agent.variable_list[i] = value
            else:
                all_ok = False
                messagebox.showerror("Error", "{} Value must be between {}-{}".format(self.agent.variable_label_list[i],
                                                                                      self.agent.variable_minmax_list[
                                                                                          i][0],
                                                                                      self.agent.variable_minmax_list[
                                                                                          i][1]))

        if all_ok:
            for i in range(3):
                self.entry_list[i].configure(state='disabled')

        return all_ok

    def next(self):

        if self.day == 0:
            all_ok = self.process_entry_input()
        else:
            all_ok = True

        if all_ok:
            print("Time: {}   {}: {:0.3f}  {}: {:0.3f}  {}: {:0.3f}".format(self.day,
                                                                            self.agent.variable_label_list[0],
                                                                            self.agent.variable_list[0],
                                                                            self.agent.variable_label_list[1],
                                                                            self.agent.variable_list[1],
                                                                            self.agent.variable_label_list[2],
                                                                            self.agent.variable_list[2]))
            self.update_data_frame()
            self.update_single_var_plots()
            self.update_all_var_plots()
            self.day += 1
            self.agent.next()

    def update_data_frame(self):
        new_label = tk.Label(self.data_canvas, text="day: {}".format(self.day), font=("Helvetica", 8), bg='white')
        new_label.place(x=5, y=60 + 20 * self.day)
        for i in range(3):
            value = "{:0.2f}".format(self.agent.variable_list[i])
            new_label = tk.Label(self.data_canvas, text=value, font=("Helvetica", 8), bg='white')
            new_label.place(x=50 + 80 * i, y=60 + 20 * self.day)

    def update_single_var_plots(self):
        pixel_x = []
        pixel_y = []
        for i in range(3):
            self.single_variable_canvas_list[i].delete("all")
            self.single_variable_canvas_list[i].create_line(20, 210, 340, 210, fill='black', width=2)
            self.single_variable_canvas_list[i].create_line(20, 210, 20, 20, fill='black', width=2)
            self.single_variable_canvas_list[i].create_text(5, 150, anchor="nw", angle=90,
                                                            text=self.agent.variable_label_list[i])
            self.single_variable_canvas_list[i].create_text(175, 220, text="Day")

            if len(self.agent.history_matrix) != 0:
                y_max = self.agent.history_matrix[0][i]
                y_min = self.agent.history_matrix[0][i]
                for j in range(1, len(self.agent.history_matrix)):
                    if y_max < self.agent.history_matrix[j][i]:
                        y_max = self.agent.history_matrix[j][i]
                    if y_min > self.agent.history_matrix[j][i]:
                        y_min = self.agent.history_matrix[j][i]
                y_range = y_max - y_min
                x_range = len(self.agent.history_matrix)
                if y_range == 0:
                    for j in range(1, len(self.agent.history_matrix)):
                        pixel_y.append(self.agent.history_matrix[j][i] * 190)
                else:
                    y_distance = 19 / y_range
                    pixel_y.append((self.agent.history_matrix[0][i] - y_min) * y_distance)
                    for j in range(1, len(self.agent.history_matrix)):
                        pixel_y.append(
                            15 + (self.agent.history_matrix[j][i] - self.agent.history_matrix[j - 1][i]) * y_distance)
                x_distance = 320 / x_range
                for j in range(0, len(self.agent.history_matrix)):
                    pixel_x.append(5 + j * x_distance)
                for j in range(1, len(self.agent.history_matrix)):
                    self.single_variable_canvas_list[i].create_line(pixel_x[j - 1] * 5, 15 + pixel_y[j - 1] * 5,
                                                                    pixel_x[j] * 5, 15 + pixel_y[j] * 5)

    def update_all_var_plots(self):

        x = self.agent.history_matrix[-1][1]
        y = self.agent.history_matrix[-1][0]
        z = self.agent.history_matrix[-1][2]
        x2D = x - 100 * z * math.cos(math.radians(45))
        y2D = y - 100 * z * math.sin(math.radians(45))

        print(x, y, z, x2D, y2D)
        self.last_2D = [x2D, y2D]

        if self.day > 0:
            self.all_vars_canvas.create_line(350 + self.last_2D[0] * 30, 350 + self.last_2D[1] * 30, 350 + x2D * 30,
                                             350 + y2D * 30)

    @staticmethod
    def quit_simulation():
        sys.exit()


def main():
    the_display = Display()
    the_display.root.mainloop()


main()

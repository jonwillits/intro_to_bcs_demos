import tkinter as tk
from turtle import RawTurtle, TurtleScreen
import random
import math
import sys
import time


###################################################################################################################
###################################################################################################################
class HeatSource:
    ###############################################################################################################
    def __init__(self, turtle_window, id_number):
        self.turtle_window = turtle_window
        self.id_number = id_number
        self.heat_source = RawTurtle(self.turtle_window.wn)
        self.heat_source.hideturtle()
        self.heat_source.shape('circle')
        self.heat_source.penup()
        self.heat_source.color("orange")
        self.heat_source.showturtle()
        self.heat_source.goto(random.randint(-290, 290), random.randint(-290, 290))
        self.onclick_event(self.heat_source)

    ###############################################################################################################
    def onclick_event(self, source):
        def onclick_hit(x, y):
            source.goto(x, y)
            return
        self.turtle_window.wn.onclick(onclick_hit)


###################################################################################################################
###################################################################################################################
class Vehicle:
    ###############################################################################################################
    def __init__(self, turtle_window, id_number):
        self.speed_parameters = [20, 0.2, 6]
        self.turn_parameters = [20]
        self.turtle_window = turtle_window

        self.vehicle = RawTurtle(self.turtle_window.wn)
        self.vehicle.hideturtle()
        self.id_number = id_number
        self.type = random.choice(["crossed", "direct"])
        self.vehicle.shape('turtle')
        self.vehicle.turtlesize(1)
        self.vehicle.penup()
        if self.type == 'crossed':
            self.vehicle.color("red", (1, 0.85, 0.85))
        else:
            self.vehicle.color("blue", (0.85, 0.85, 1))
        self.vehicle.goto(random.randint(-290, 290), random.randint(-290, 290))
        self.vehicle.right(random.randint(0, 360))
        self.vehicle.showturtle()
        self.onclick_event(self.vehicle)

    ###############################################################################################################
    def move(self):
        cumulative_speed = 0
        cumulative_turn_amount = 0
        for heat_source in self.turtle_window.heat_source_list:
            input_distance = self.vehicle.distance(heat_source.heat_source.pos())
            input_angle = self.vehicle.heading() - self.vehicle.towards(heat_source.heat_source.pos())
            sin_angle = math.sin(math.radians(input_angle))
            left_sensor_distance = input_distance - sin_angle
            right_sensor_distance = input_distance + sin_angle
            left_speed, right_speed, combined_speed = self.compute_speed(left_sensor_distance, right_sensor_distance)
            turn_amount = self.turn_parameters[0] * (right_speed - left_speed)
            cumulative_speed += combined_speed
            cumulative_turn_amount += turn_amount

        self.vehicle.right(cumulative_turn_amount)
        self.vehicle.forward(cumulative_speed)
        self.check_border_collision()

    def check_border_collision(self):
        if self.vehicle.ycor() <= -330:
            if 0 <= self.vehicle.heading() <= 180:
                turn_angle = 180 - self.vehicle.heading()
                self.vehicle.setheading(turn_angle)
            else:
                turn_angle = abs(360 - self.vehicle.heading())
                self.vehicle.setheading(turn_angle)

        if self.vehicle.ycor() >= 330:
            if 0 <= self.vehicle.heading() <= 180:
                turn_angle = 360 - self.vehicle.heading()
                self.vehicle.setheading(turn_angle)
            else:
                turn_angle = 360 - (self.vehicle.heading() - 180)
                self.vehicle.setheading(turn_angle)

        if self.vehicle.xcor() <= -330:
            if 0 <= self.vehicle.heading() <= 90:
                turn_angle = 360 - self.vehicle.heading()
                self.vehicle.setheading(turn_angle)
            if 270 < self.vehicle.heading() <= 360:
                turn_angle = 360 - self.vehicle.heading()
                self.vehicle.setheading(turn_angle)
            if 90 < self.vehicle.heading() < 180:
                turn_angle = self.vehicle.heading() - 90
                self.vehicle.setheading(turn_angle)
            if 180 <= self.vehicle.heading() <= 360:
                turn_angle = self.vehicle.heading() + 90
                self.vehicle.setheading(turn_angle)

        if self.vehicle.xcor() >= 330:
            if 0 <= self.vehicle.heading() <= 180:
                turn_angle = self.vehicle.heading() + 90
                self.vehicle.setheading(turn_angle)
            else:
                turn_angle = self.vehicle.heading() - 90
                self.vehicle.setheading(turn_angle)

    ###############################################################################################################
    def compute_speed(self, left_distance, right_distance):
        if self.type == 'crossed':
            left_speed = (self.speed_parameters[0] / (right_distance ** self.speed_parameters[1])) - self.speed_parameters[2]
            right_speed = (self.speed_parameters[0] / (left_distance ** self.speed_parameters[1])) - self.speed_parameters[2]
        else:
            left_speed = (self.speed_parameters[0] / (left_distance ** self.speed_parameters[1])) - self.speed_parameters[2]
            right_speed = (self.speed_parameters[0] / (right_distance ** self.speed_parameters[1])) - self.speed_parameters[2]
        combined_speed = (left_speed + right_speed) / 2
        return left_speed, right_speed, combined_speed

    ###############################################################################################################
    def onclick_event(self, source):
        def onclick_hit(x, y):
            source.goto(x, y)
        self.turtle_window.wn.onclick(onclick_hit)


###################################################################################################################
###################################################################################################################
class TurtleWindow:
    ###############################################################################################################
    def __init__(self, num_vehicles, num_heat_sources):
        self.root = None
        self.canvas = None
        self.wn = None
        self.button_frame = None
        self.start_button = None
        self.stop_button = None
        self.reset_button = None
        self.quit_button = None

        self.num_heat_sources = num_heat_sources
        self.heat_source_list = []

        self.num_vehicles = num_vehicles
        self.vehicle_list = []

        self.running = False

        self.create_window()
        self.wn.tracer(0, 0)
        self.create_heat_sources()
        self.create_vehicles()
        self.wn.update()

    ###############################################################################################################
    def create_window(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=700, height=700)
        self.canvas.pack()
        self.wn = TurtleScreen(self.canvas)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.start_button = tk.Button(self.button_frame, text="Start", fg="black", command=self.start_stop)
        self.reset_button = tk.Button(self.button_frame, text="Reset", fg="black", command=self.reset)
        self.quit_button = tk.Button(self.button_frame, text="Quit", fg="black", command=self.quit)
        self.start_button.pack(side=tk.LEFT)
        self.reset_button.pack(side=tk.LEFT)
        self.quit_button.pack(side=tk.LEFT)

    ###############################################################################################################
    def create_heat_sources(self):
        for i in range(self.num_heat_sources):
            self.heat_source_list.append(HeatSource(self, i))

    ###############################################################################################################
    def create_vehicles(self):
        for i in range(self.num_vehicles):
            self.vehicle_list.append(Vehicle(self, i))

    ###############################################################################################################
    def start_stop(self):
        if self.running:
            self.running = False
            self.start_button.config(text="Start")
        else:
            self.running = True
            self.start_button.config(text="Pause")

        while self.running:
            for i in range(self.num_vehicles):
                self.vehicle_list[i].move()
            self.wn.update()
            time.sleep(0.01)

    ###############################################################################################################
    def reset(self):
        self.vehicle_list.pop(0)
        self.wn.clear()
        self.wn.tracer(0, 0)
        self.create_heat_sources()
        self.create_vehicles()
        self.wn.update()

    ###############################################################################################################
    def quit(self):
        sys.exit()

    ###############################################################################################################
    def onclick_event(self, source):
        def onclick_hit(x, y):
            source.goto(x, y)
        self.wn.onclick(onclick_hit)
        self.wn.update()


###################################################################################################################
###################################################################################################################
###################################################################################################################
###################################################################################################################
NUM_TURTLES = 3
NUM_HEAT_SOURCES = 3


def main():
    turtle_window = TurtleWindow(NUM_TURTLES, NUM_HEAT_SOURCES)
    turtle_window.wn.mainloop()


main()
from . import objects
from . import body_components
from .. import params
import numpy as np


class Agent(objects.SimulationObject):

    def __init__(self, main_window):
        """
        Initializes a Vehicle object, representing a mobile turtle object that reacts to heat sources
        on the turtle screen.

        Args:
            main_window (TurtleWindow): A reference to the TurtleWindow instance managing the simulation.

        """
        super().__init__(main_window)

        self.object_type = "Agent"

        self.sensor_list = None
        self.current_sense_array = None
        self.actuator_list = None
        self.current_actuator_array = None
        self.nervous_system = None

        self.init_sensors()
        self.init_body()
        self.init_nervous_system()
        self.init_actuators()

    def init_sensors(self):
        self.sensor_list = [body_components.HeatSensor(self, anchor_position="ne"),
                            body_components.HeatSensor(self, anchor_position="nw")]

    def init_body(self):
        pass

    def init_nervous_system(self):
        pass

    def init_actuators(self):
        pass

    def update_sensors(self):
        current_sensor_data_list = []
        for sensor in self.sensor_list:
            object_list = self.main_window.object_list_dict[sensor.input_type]
            current_sensor_data_list.append(sensor.update(object_list))
        self.current_sense_array = np.array(current_sensor_data_list)

    def update(self):
        """
        Updates the screen only if an update is required.
        """
        self.update_required = True
        self.update_sensors()
        self.move()
        print(self.current_sense_array)

        if self.update_required:
            self.main_window.wn.update()  # Update the screen with the new position
            self.update_required = False  # Reset the flag

    def move(self):
        """
        Calculates the movement of the vehicle based on the distance and angle to heat sources.
        The vehicle moves towards or away from heat sources depending on its type.
        """
        cumulative_speed = 0  # Initialize cumulative speed
        cumulative_turn_amount = 0  # Initialize cumulative turn amount
#
#         # Iterate through all heat sources to calculate the movement
#         for heat_source in self.turtle_window.heat_source_list:
#             input_distance = self.turtle.distance(heat_source.heat_source.pos())  # Distance to the heat source
#             input_angle = self.turtle.heading() - self.turtle.towards(
#                 heat_source.heat_source.pos())  # Angle to the heat source
#             sin_angle = math.sin(math.radians(input_angle))  # Sine of the angle
#             left_sensor_distance = input_distance - sin_angle  # Distance to the left sensor
#             right_sensor_distance = input_distance + sin_angle  # Distance to the right sensor
#
#             left_speed, right_speed, combined_speed = self.compute_speed()  # Compute speeds
#             turn_amount = self.turn_parameters[0] * (right_speed - left_speed)  # Calculate the turn amount
#             cumulative_speed += combined_speed  # Accumulate the speed
#             cumulative_turn_amount += turn_amount  # Accumulate the turn amount
#
#         # Handle potential complex numbers and negative speeds
#         if isinstance(cumulative_turn_amount, complex):
#             cumulative_turn_amount = 0
#
#         if cumulative_speed < 0:
#             cumulative_speed = 0
#
#         self.turtle.right(cumulative_turn_amount)  # Apply the turning
#         self.turtle.forward(cumulative_speed)  # Move the vehicle forward
#         self.check_border_collision()  # Check and handle border collisions

    def check_border_collision(self):
        """
        Checks if the vehicle has collided with the border and corrects its position and heading.
        """
        x, y = self.turtle.xcor(), self.turtle.ycor()  # Get the current position

        # Check horizontal borders
        if abs(x) > self.main_window.max_width:
            x = max(min(x, self.main_window.max_width), -self.main_window.max_width)  # Correct the x position
            self.turtle.goto(x, y)  # Move the vehicle to the corrected position
            self.turtle.setheading(180 - self.turtle.heading())  # Adjust the heading

        # Check vertical borders
        if abs(y) > self.main_window.max_height:
            y = max(min(y, self.main_window.max_height), -self.main_window.max_height)  # Correct the y position
            self.turtle.goto(x, y)  # Move the vehicle to the corrected position
            self.turtle.setheading(-self.turtle.heading())  # Adjust the heading

    def compute_speed(self, left_distance, right_distance):
        """
        Computes the speed of the vehicle based on the distances from the left and right sensors
        to the heat source. The behavior depends on the vehicle type.

        Args:
            left_distance (float): The distance to the heat source from the left sensor.
            right_distance (float): The distance to the heat source from the right sensor.

        Returns:
            tuple: A tuple containing the left speed, right speed, and combined speed.
        """
        # if self.type == 'crossed':
        #     left_distance, right_distance = right_distance, left_distance  # Swap distances for crossed type

        # Calculate left speed
        left_speed = (self.speed_params[0] / (left_distance ** self.speed_params[1])) - self.speed_params[2]
        # Calculate right speed
        right_speed = (self.speed_params[0] / (right_distance ** self.speed_params[1])) - self.speed_params[2]
        combined_speed = (left_speed + right_speed) / 2  # Calculate the combined speed
        return left_speed, right_speed, combined_speed  # Return the computed speeds
#
#
# class BlueVehicle(Vehicle):
#
#     def __init__(self, turtle_window):
#         super().__init__(turtle_window)
#         self.turtle.color("black", "blue")
#
#     def compute_speed(self, left_input, right_input):
#         """
#         Computes the speed of the vehicle based on the distances from the left and right sensors
#         to the heat source. The behavior depends on the vehicle type.
#
#         Args:
#             left_input (float): The distance to the heat source from the left sensor.
#             right_input (float): The distance to the heat source from the right sensor.
#
#         Returns:
#             tuple: A tuple containing the left speed, right speed, and combined speed.
#         """
#
#         # Calculate left speed
#         left_speed = (self.speed_params[0] / (left_input ** self.speed_params[1])) - self.speed_params[2]
#         # Calculate right speed
#         right_speed = (self.speed_params[0] / (right_input ** self.speed_params[1])) - self.speed_params[2]
#         combined_speed = (left_speed + right_speed) / 2  # Calculate the combined speed
#         return left_speed, right_speed, combined_speed  # Return the computed speeds
#
#
# class RedVehicle(Vehicle):
#
#     def __init__(self, turtle_window):
#         super().__init__(turtle_window)
#         self.turtle.color("black", "red")
#
#     def compute_speed(self, left_distance, right_distance):
#         """
#         Computes the speed of the vehicle based on the distances from the left and right sensors
#         to the heat source. The behavior depends on the vehicle type.
#
#         Args:
#             left_distance (float): The distance to the heat source from the left sensor.
#             right_distance (float): The distance to the heat source from the right sensor.
#
#         Returns:
#             tuple: A tuple containing the left speed, right speed, and combined speed.
#         """
#         left_distance, right_distance = right_distance, left_distance  # Swap distances for crossed type
#
#         # Calculate left speed
#         left_speed = (self.speed_params[0] / (left_distance ** self.speed_params[1])) - self.speed_params[2]
#         # Calculate right speed
#         right_speed = (self.speed_params[0] / (right_distance ** self.speed_params[1])) - self.speed_params[2]
#         combined_speed = (left_speed + right_speed) / 2  # Calculate the combined speed
#         return left_speed, right_speed, combined_speed  # Return the computed speeds
import tkinter as tk
from turtle import RawTurtle, TurtleScreen
import random, math, sys, time


###################################################################################################################
###################################################################################################################
class HeatSource:
    ###############################################################################################################
    def __init__(self, turtle_window, id_number):
        """
        Initializes a HeatSource object, representing a heat source on the turtle screen.

        Args:
            turtle_window (TurtleWindow): A reference to the TurtleWindow instance managing the simulation.
            id_number (int): A unique identifier for this heat source.

        Attributes:
            turtle_window (TurtleWindow): The TurtleWindow instance to which this heat source belongs.
            id_number (int): The unique identifier for this heat source.
            heat_source (RawTurtle): The turtle object representing the heat source on the screen.
        """
        self.turtle_window = turtle_window  # Reference to the TurtleWindow instance
        self.id_number = id_number  # Unique identifier for the heat source
        self.heat_source = RawTurtle(self.turtle_window.wn)  # Create a turtle object for the heat source
        self.heat_source.hideturtle()  # Hide the turtle until it is placed
        self.heat_source.shape('circle')  # Set the turtle shape to a circle
        self.heat_source.penup()  # Prevent drawing lines when the turtle moves
        self.heat_source.color("orange")  # Set the color of the heat source to orange
        self.place()  # Place the heat source randomly on the screen
        self.heat_source.showturtle()  # Show the heat source on the screen

        self.heat_source.ondrag(self.drag_heat_source)  # Allow the heat source to be draggable

    ###############################################################################################################
    def place(self):
        """
        Places the heat source at a random position on the screen within the screen bounds.
        """
        max_width = self.turtle_window.screen_size[0] / 2 - 10  # Calculate the maximum horizontal position
        max_height = self.turtle_window.screen_size[1] / 2 - 10  # Calculate the maximum vertical position
        self.heat_source.goto(random.randint(-max_width, max_width),
                              random.randint(-max_height, max_height))  # Move the heat source to a random position

    ###############################################################################################################
    def drag_heat_source(self, x, y):
        """
        Handles the dragging of the heat source by updating its position and continuing the simulation.

        Args:
            x (float): The x-coordinate where the heat source is being dragged.
            y (float): The y-coordinate where the heat source is being dragged.
        """
        self.heat_source.goto(x, y)  # Move the heat source to the dragged position
        self.turtle_window.wn.update()  # Update the screen to reflect the new position
        self.turtle_window.run_simulation()  # Continue running the simulation during dragging
        self.turtle_window.root.after(10, self.drag_heat_source, x,
                                      y)  # Schedule another update to keep the simulation running


###################################################################################################################
###################################################################################################################
class Vehicle:
    ###############################################################################################################
    def __init__(self, turtle_window, id_number):
        """
        Initializes a Vehicle object, representing a mobile turtle object that reacts to heat sources
        on the turtle screen.

        Args:
            turtle_window (TurtleWindow): A reference to the TurtleWindow instance managing the simulation.
            id_number (int): A unique identifier for this vehicle.

        Attributes:
            speed_params (list): A list of parameters affecting the speed of the vehicle.
            turn_parameters (list): A list of parameters affecting the turning behavior of the vehicle.
            turtle_window (TurtleWindow): The TurtleWindow instance to which this vehicle belongs.
            max_width (float): The maximum horizontal coordinate the vehicle can occupy on the screen.
            max_height (float): The maximum vertical coordinate the vehicle can occupy on the screen.
            vehicle (RawTurtle): The turtle object representing the vehicle on the screen.
            id_number (int): The unique identifier for this vehicle.
            type (str): The type of vehicle, either 'crossed' or 'direct', affecting its movement behavior.
        """
        self.speed_params = [20, 0.2, 6]  # Speed parameters used to calculate movement
        self.turn_parameters = [20]  # Turning parameter
        self.turtle_window = turtle_window  # Reference to the TurtleWindow instance
        self.max_width = self.turtle_window.screen_size[0] / 2 - 10  # Calculate the maximum horizontal position
        self.max_height = self.turtle_window.screen_size[1] / 2 - 10  # Calculate the maximum vertical position
        self.vehicle = RawTurtle(self.turtle_window.wn)  # Create a turtle object for the vehicle
        self.vehicle.hideturtle()  # Hide the turtle until it is placed
        self.id_number = id_number  # Unique identifier for the vehicle
        self.type = random.choice(["crossed", "direct"])  # Randomly choose the vehicle type

        # Set the turtle shape and color based on the vehicle type
        self.vehicle.shape('turtle')  # Set the turtle shape
        self.vehicle.turtlesize(1)  # Set the size of the turtle
        self.vehicle.penup()  # Prevent drawing lines when the turtle moves
        if self.type == 'crossed':
            self.vehicle.color("red", (1, 0.85, 0.85))  # Color for 'crossed' type
        else:
            self.vehicle.color("blue", (0.85, 0.85, 1))  # Color for 'direct' type

        self.place()  # Place the vehicle randomly on the screen
        self.vehicle.showturtle()  # Show the turtle once it is placed

    ###############################################################################################################
    def place(self):
        """
        Places the vehicle at a random position and orientation on the screen.
        """
        # Move the vehicle to a random position within the screen bounds
        self.vehicle.goto(random.randint(-self.max_width, self.max_width),
                          random.randint(-self.max_height, self.max_height))
        self.vehicle.right(random.randint(0, 360))  # Rotate the vehicle to a random direction

    ###############################################################################################################
    def move(self):
        """
        Calculates the movement of the vehicle based on the distance and angle to heat sources.
        The vehicle moves towards or away from heat sources depending on its type.
        """
        cumulative_speed = 0  # Initialize cumulative speed
        cumulative_turn_amount = 0  # Initialize cumulative turn amount

        # Iterate through all heat sources to calculate the movement
        for heat_source in self.turtle_window.heat_source_list:
            input_distance = self.vehicle.distance(heat_source.heat_source.pos())  # Distance to the heat source
            input_angle = self.vehicle.heading() - self.vehicle.towards(
                heat_source.heat_source.pos())  # Angle to the heat source
            sin_angle = math.sin(math.radians(input_angle))  # Sine of the angle
            left_sensor_distance = input_distance - sin_angle  # Distance to the left sensor
            right_sensor_distance = input_distance + sin_angle  # Distance to the right sensor
            left_speed, right_speed, combined_speed = self.compute_speed(left_sensor_distance,
                                                                         right_sensor_distance)  # Compute speeds
            turn_amount = self.turn_parameters[0] * (right_speed - left_speed)  # Calculate the turn amount
            cumulative_speed += combined_speed  # Accumulate the speed
            cumulative_turn_amount += turn_amount  # Accumulate the turn amount

        # Handle potential complex numbers and negative speeds
        if isinstance(cumulative_turn_amount, complex):
            cumulative_turn_amount = 0

        if cumulative_speed < 0:
            cumulative_speed = 0

        self.vehicle.right(cumulative_turn_amount)  # Apply the turning
        self.vehicle.forward(cumulative_speed)  # Move the vehicle forward
        self.check_border_collision()  # Check and handle border collisions

    ###############################################################################################################
    def check_border_collision(self):
        """
        Checks if the vehicle has collided with the border and corrects its position and heading.
        """
        x, y = self.vehicle.xcor(), self.vehicle.ycor()  # Get the current position

        # Check horizontal borders
        if abs(x) > self.max_width:
            x = max(min(x, self.max_width), -self.max_width)  # Correct the x position
            self.vehicle.goto(x, y)  # Move the vehicle to the corrected position
            self.vehicle.setheading(180 - self.vehicle.heading())  # Adjust the heading

        # Check vertical borders
        if abs(y) > self.max_height:
            y = max(min(y, self.max_height), -self.max_height)  # Correct the y position
            self.vehicle.goto(x, y)  # Move the vehicle to the corrected position
            self.vehicle.setheading(-self.vehicle.heading())  # Adjust the heading

    ###############################################################################################################
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
        if self.type == 'crossed':
            left_distance, right_distance = right_distance, left_distance  # Swap distances for crossed type
        left_speed = (self.speed_params[0] / (left_distance ** self.speed_params[1])) - self.speed_params[
            2]  # Calculate left speed
        right_speed = (self.speed_params[0] / (right_distance ** self.speed_params[1])) - self.speed_params[
            2]  # Calculate right speed
        combined_speed = (left_speed + right_speed) / 2  # Calculate the combined speed
        return left_speed, right_speed, combined_speed  # Return the computed speeds


###################################################################################################################
###################################################################################################################
class TurtleWindow:
    ###############################################################################################################
    def __init__(self, num_vehicles, num_heat_sources, screen_size):
        """
        Initializes the TurtleWindow, which manages the simulation window, including the vehicles, heat sources,
        and control buttons.

        Args:
            num_vehicles (int): The number of vehicles to create in the simulation.
            num_heat_sources (int): The number of heat sources to create in the simulation.
            screen_size (tuple): The size of the turtle screen as (width, height).

        Attributes:
            root (tk.Tk): The main window object.
            canvas (tk.Canvas): The canvas where the turtle graphics are drawn.
            wn (TurtleScreen): The turtle screen object for managing turtle graphics.
            button_frame (tk.Frame): The frame that holds the control buttons.
            start_button (tk.Button): Button to start or pause the simulation.
            reset_button (tk.Button): Button to reset the simulation.
            quit_button (tk.Button): Button to quit the application.
            screen_size (tuple): The size of the turtle screen.
            num_heat_sources (int): Number of heat sources in the simulation.
            heat_source_list (list): A list of HeatSource objects.
            num_vehicles (int): Number of vehicles in the simulation.
            vehicle_list (list): A list of Vehicle objects.
            running (bool): A flag indicating whether the simulation is running.
        """
        self.root = None  # The main window
        self.canvas = None  # The canvas for drawing
        self.wn = None  # The turtle screen
        self.button_frame = None  # Frame for holding the buttons
        self.start_button = None  # Start button
        self.stop_button = None  # Stop button (not used in the current implementation)
        self.reset_button = None  # Reset button
        self.quit_button = None  # Quit button

        self.screen_size = screen_size  # The size of the turtle screen

        self.num_heat_sources = num_heat_sources  # Number of heat sources
        self.heat_source_list = []  # List to store the heat sources

        self.num_vehicles = num_vehicles  # Number of vehicles
        self.vehicle_list = []  # List to store the vehicles

        self.running = False  # Simulation running state

        self.create_window()  # Create the window and GUI elements
        self.wn.tracer(0, 0)  # Disable animation for faster drawing
        self.create_heat_sources()  # Create the heat sources
        self.create_vehicles()  # Create the vehicles
        self.wn.update()  # Update the screen with the initial setup

    ###############################################################################################################
    def create_window(self):
        """
        Creates the main window, canvas, turtle screen, and control buttons.
        """
        self.root = tk.Tk()  # Initialize the main Tkinter window
        self.canvas = tk.Canvas(self.root, width=self.screen_size[0],
                                height=self.screen_size[1])  # Create a canvas for turtle graphics
        self.canvas.pack()  # Add the canvas to the window
        self.wn = TurtleScreen(self.canvas)  # Initialize the turtle screen with the canvas
        self.root.title("Braitenberg's Vehicle #2")  # Set the window title
        self.wn.onkey(self.start_stop, "space")  # Bind the spacebar to start/stop the simulation
        self.wn.listen()  # Listen for keyboard events

        self.button_frame = tk.Frame(self.root)  # Create a frame for the control buttons
        self.button_frame.pack()  # Add the button frame to the window

        # Create and pack the control buttons
        self.start_button = tk.Button(self.button_frame, text="Start", fg="black", command=self.start_stop)
        self.reset_button = tk.Button(self.button_frame, text="Reset", fg="black", command=self.reset)
        self.quit_button = tk.Button(self.button_frame, text="Quit", fg="black", command=self.quit)
        self.start_button.pack(side=tk.LEFT)  # Add the start button to the frame
        self.reset_button.pack(side=tk.LEFT)  # Add the reset button to the frame
        self.quit_button.pack(side=tk.LEFT)  # Add the quit button to the frame

    ###############################################################################################################
    def create_heat_sources(self):
        """
        Creates the specified number of heat sources and adds them to the heat_source_list.
        """
        for i in range(self.num_heat_sources):
            self.heat_source_list.append(HeatSource(self, i))  # Create a heat source and add it to the list

    ###############################################################################################################
    def create_vehicles(self):
        """
        Creates the specified number of vehicles and adds them to the vehicle_list.
        """
        for i in range(self.num_vehicles):
            self.vehicle_list.append(Vehicle(self, i))  # Create a vehicle and add it to the list

    ###############################################################################################################
    def start_stop(self):
        """
        Starts or pauses the simulation depending on the current state.
        """
        if self.running:
            self.running = False  # Pause the simulation
            self.start_button.config(text="Start")  # Change the button text to "Start"
        else:
            self.running = True  # Start the simulation
            self.start_button.config(text="Pause")  # Change the button text to "Pause"
            self.run_simulation()  # Start running the simulation

    ###############################################################################################################
    def run_simulation(self):
        """
        Runs the simulation by moving all vehicles and updating the screen.
        This method continues to call itself recursively while the simulation is running.
        """
        if not self.running:
            return  # Exit if the simulation is paused
        for i in range(self.num_vehicles):
            self.vehicle_list[i].move()  # Move each vehicle
        self.wn.update()  # Update the screen with the new positions
        self.root.after(10, self.run_simulation)  # Schedule the next update in 10 milliseconds

    ###############################################################################################################
    def reset(self):
        """
        Resets the simulation by clearing the screen, recreating the heat sources and vehicles,
        and updating the screen.
        """
        self.vehicle_list = []  # Clear the list of vehicles
        self.heat_source_list = []  # Clear the list of heat sources

        self.wn.clear()  # Clear the turtle screen
        self.wn.tracer(0, 0)  # Disable animation for faster drawing
        self.create_heat_sources()  # Recreate the heat sources
        self.create_vehicles()  # Recreate the vehicles
        self.wn.update()  # Update the screen with the new setup

    ###############################################################################################################
    @staticmethod
    def quit():
        """
        Exits the application.
        """
        sys.exit()  # Exit the program


###################################################################################################################
###################################################################################################################
###################################################################################################################
###################################################################################################################

def main():
    num_turtles = 3
    num_heat_sources = 3
    screen_size = (800,600)
    turtle_window = TurtleWindow(num_turtles, num_heat_sources, screen_size)
    turtle_window.wn.mainloop()


main()

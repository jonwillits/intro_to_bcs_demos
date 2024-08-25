from turtle import RawTurtle
import random
import os
from collections import OrderedDict
from . import utils

class SimulationObject:

    def __init__(self, main_window, index, shape=None, height=None, width=None, color=None, starting_orientation=None):
        self.object_type = "Object"
        self.index = index
        self.object_name = f"{self.object_type}_{self.index}"
        self.main_window = main_window  # Reference to the TurtleWindow instance
        self.image_path = "./images/"
        self.image_dictionary = None
        self.shape = shape
        self.height = height
        self.width = width
        self.color = color
        self.starting_orientation = starting_orientation

        self.turtle = RawTurtle(self.main_window.wn)
        self.turtle.hideturtle()  # Hide the turtle until it is placed
        self.turtle.penup()  # Prevent drawing lines when the turtle moves
        self.turtle.ondrag(self.drag_turtle)  # Allow the object to be draggable
        self.update_required = False

        self.init_properties()
        self.place()  # Puts the turtle in its starting position
        self.init_shape()  # Creates the icons of the turtle

        self.turtle.showturtle()  # Show the object on the screen

    def init_properties(self):

        self.color = utils.validate_and_extend_rgb_tuple(self.color)
        self.height = utils.validate_positive_integer(self.height)
        self.width = utils.validate_positive_integer(self.width)
        self.starting_orientation = utils.normalize_angle(self.starting_orientation)

        if self.shape is None:
            self.shape = 'ellipse'
        if self.shape != 'ellipse' and self.shape != 'rectangle':
            raise Exception(f"ERROR: Unrecognized shape {self.shape}")


    def init_shape(self):
        # Set self.image_path to self.image_path + self.object_name in an OS-compatible way
        self.image_path = os.path.join(self.image_path, self.object_name)

        # Create rotated shape images
        utils.create_rotated_shape_images(self.width, self.height, self.shape, self.color, self.image_path, angles=24)

        # Load the full set of images and store them in self.image_dictionary
        self.image_dictionary = OrderedDict()

        for file_name in sorted(os.listdir(self.image_path)):
            if file_name.endswith('.gif'):
                angle = int(file_name.split('_')[-1].split('.')[0])  # Extract the angle from the file name
                self.image_dictionary[angle] = os.path.join(self.image_path, file_name)
                self.main_window.wn.register_shape(self.image_dictionary[angle])

        self.rotate(self.starting_orientation)

    def rotate(self, orientation):
        # Set the turtle's direction to the stated orientation
        self.turtle.setheading(orientation)

        # Find the closest angle match from self.image_dictionary
        closest_angle = min(self.image_dictionary.keys(), key=lambda k: abs(k - orientation))

        # Set the turtle's shape to the corresponding image
        self.turtle.shape(self.image_dictionary[closest_angle])


    def place(self):
        """
        Places the heat source at a random position on the screen within the screen bounds.
        """
        self.turtle.goto(random.randint(-self.main_window.max_width, self.main_window.max_width),
                         random.randint(-self.main_window.max_height, self.main_window.max_height))

    def drag_turtle(self, x, y):
        """
        Handles the dragging of the heat source by updating its position.
        """
        self.turtle.ondrag(None)  # Temporarily disable dragging to prevent event flood
        self.turtle.goto(x, y)  # Move the heat source to the dragged position
        self.main_window.wn.update()  # Immediately update the screen after moving
        self.update_required = True  # Set the flag to true to indicate an update is needed
        self.turtle.ondrag(self.drag_turtle)  # Re-enable dragging after updating the position

    def update(self):
        """
        Updates the screen only if an update is required.
        """
        if self.update_required:
            self.main_window.wn.update()  # Update the screen with the new position
            self.update_required = False  # Reset the flag







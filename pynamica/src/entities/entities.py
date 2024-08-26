from turtle import RawTurtle
import random
import os
from collections import OrderedDict
try:
    from src.display import graphics
except:
    from ..display import graphics
try:
    from src import utils
except:
    from .. import utils

class Entity:

    def __init__(self, main_window, index, entity_type):
        self.entity_type = entity_type
        self.index = index
        self.entity_name = f"{self.entity_type}_{self.index}"
        self.main_window = main_window  # Reference to the TurtleWindow instance
        self.image_path = "../display/images/"
        self.image_dictionary = None
        self.turtle = None
        self.params = None

        self.update_required = False

        self.init_properties()
        self.create_turtle()
        self.place()  # Puts the turtle in its starting position
        self.init_shape()  # Creates the icons of the turtle

        self.turtle.showturtle()  # Show the object on the screen

    def __str__(self):
        # Create the string representation
        return f"{self.entity_type} {self.turtle.position()} {self.turtle.heading()}\n"

    def init_properties(self):

        if self.main_window.param_dict is not None:
            if self.entity_type in self.main_window.param_dict:
                self.params = self.main_window.param_dict[self.entity_type]
                for key in self.params:
                    value = utils.validate_attribute(key, self.params[key])
                    self.params[key] = value

            else:
                raise Exception(f"ERROR: No params class for {self.entity_type}")
        else:
            raise Exception(f"ERROR: Application has no params")

    def create_turtle(self):
        self.turtle = RawTurtle(self.main_window.wn)
        self.turtle.hideturtle()  # Hide the turtle until it is placed
        self.turtle.penup()  # Prevent drawing lines when the turtle moves
        self.turtle.ondrag(self.drag_turtle)  # Allow the object to be draggable

    def init_shape(self):
        # Set self.image_path to self.image_path + self.object_name in an OS-compatible way
        self.image_path = os.path.join(self.image_path, self.entity_type)

        self.params = utils.set_entity_defaults(self.params)

        # Create rotated shape images
        graphics.create_rotated_shape_images(self.image_path,
                                             width=self.params['width'],
                                             height=self.params['height'],
                                             shape=self.params['shape'],
                                             color=self.params['color'],
                                             angles=24)

        # Load the full set of images and store them in self.image_dictionary
        self.image_dictionary = OrderedDict()

        for file_name in sorted(os.listdir(self.image_path)):
            if file_name.endswith('.gif'):
                angle = int(file_name.split('_')[-1].split('.')[0])  # Extract the angle from the file name
                self.image_dictionary[angle] = os.path.join(self.image_path, file_name)
                self.main_window.wn.register_shape(self.image_dictionary[angle])

        self.rotate(self.params['starting_orientation'])

    def rotate(self, orientation):
        # Set the turtle's direction to the stated orientation
        self.turtle.setheading(orientation)

        # Find the closest angle match from self.image_dictionary
        closest_angle = min(self.image_dictionary.keys(), key=lambda k: abs(k - orientation))
        # Set the turtle's shape to the corresponding image
        self.turtle.shape(self.image_dictionary[closest_angle])
        self.turtle.ondrag(self.drag_turtle)


    def place(self):
        """
        Places the heat source at a random position on the screen within the screen bounds.
        """
        self.turtle.goto(random.randint(-self.main_window.max_width, self.main_window.max_width),
                         random.randint(-self.main_window.max_height, self.main_window.max_height))

    def drag_turtle(self, x, y):
        """
        Handles the dragging of the object by updating its position.
        """
        if self.turtle.isvisible():  # Check if the turtle is visible
            self.turtle.ondrag(None)  # Temporarily disable dragging to prevent event flood
            self.turtle.goto(x, y)  # Move the object to the dragged position
            self.update_required = True  # Set the flag to true to indicate an update is needed
            self.main_window.wn.update()  # Immediately update the screen after moving
            self.turtle.ondrag(self.drag_turtle)  # Re-enable dragging after updating the position

    def update(self):
        """
        Updates the screen only if an update is required.
        """
        if self.update_required:
            self.main_window.wn.update()  # Update the screen with the new position
            self.update_required = False  # Reset the flag

    def add_attribute(self, attribute_name, attribute_dict, default_value):
        if self.params is not None:
            if attribute_name in attribute_dict:
                return attribute_dict[attribute_name]
            else:
                return default_value
        else:
            return default_value


class HeatSource(Entity):

    def __init__(self, main_window, index):
        """
        Initializes a HeatSource object, representing a heat source on the turtle screen.
        """
        super().__init__(main_window, index, entity_type="HeatSource")
        self.intensity = 1




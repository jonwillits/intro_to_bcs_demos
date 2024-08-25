from . import objects
from ..params import HeatSource as HeatSourceParams

class HeatSource(objects.SimulationObject):

    def __init__(self, turtle_window, index):
        """
        Initializes a HeatSource object, representing a heat source on the turtle screen.
        """
        shape = HeatSourceParams.shape
        height = HeatSourceParams.shape
        width = HeatSourceParams.shape
        color = HeatSourceParams.shape
        starting_orientation = HeatSourceParams.shape

        super().__init__(turtle_window, index, shape, height, width, color, starting_orientation)

        try:
            self.intensity = HeatSourceParams.intensity
        except:
            self.intensity = 1

        self.object_type = "HeatSource"
        self.turtle.hideturtle()  # Hide the turtle until it is placed
        self.turtle.shape('circle')  # Set the turtle shape to a circle
        self.turtle.color("orange")  # Set the color of the heat source to orange
        self.turtle.turtlesize(2)
        self.turtle.showturtle()  # Show the heat source on the screen
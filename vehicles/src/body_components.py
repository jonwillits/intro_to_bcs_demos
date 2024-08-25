import math

class BodyComponent:
    def __init__(self, parent_object, anchor_position):
        self.parent_object = parent_object
        self.anchor_position = anchor_position
        self.sensor_position = None
        self.sensor_type = None
        self.input_type = None

        self.anchor_offset_dict = {
            "e": (1, 0),
            "w": (-1, 0),
            "n": (0, 1),
            "s": (0, -1),
            "ne": (1, 1),
            "se": (1, -1),
            "nw": (-1, 1),
            "sw": (-1, -1),
        }

        self.update_position()

    def update_position(self):
        turtle_position = self.parent_object.turtle.pos()
        sensor_offset = self.anchor_offset_dict[self.anchor_position]
        self.sensor_position = tuple(a + b for a, b in zip(turtle_position, sensor_offset))

    def update(self):
        self.update_position()

class HeatSensor(BodyComponent):

    def __init__(self, parent_object, anchor_position, sensitivity=1):

        super().__init__(parent_object, anchor_position)

        self.sensitivity = sensitivity
        self.sensor_type = "Heat Sensor"
        self.input_type = "Heat Source"

    # noinspection PyMethodOverriding
    def update(self, heat_source_list):

        super().update()

        self.update_position()

        total_intensity = 0
        epsilon = 1e-5

        for heat_source in heat_source_list:
            heat_source_position = heat_source.turtle.pos()
            distance = math.sqrt((self.sensor_position[0] - heat_source_position[0]) ** 2 +
                                 (self.sensor_position[1] - heat_source_position[1]) ** 2)

            adjusted_distance = max(distance, epsilon)  # Ensure distance is never too small
            total_intensity += heat_source.intensity / (adjusted_distance ** 2)

        return total_intensity

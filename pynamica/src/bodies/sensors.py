import math
from . import body_components

class HeatSensor(body_components.BodyComponent):

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
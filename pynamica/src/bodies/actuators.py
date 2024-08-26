from . import body_components

class Wheel(body_components.BodyComponent):

    def __init__(self, parent_object, anchor_position):

        super().__init__(parent_object, anchor_position)

    # noinspection PyMethodOverriding
    def update(self, wheel_input):

        super().update()

        output = input

        return output
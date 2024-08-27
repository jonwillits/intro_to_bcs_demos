import math

class BodyComponent:
    def __init__(self, parent_object, anchor_position=None):
        self.component_type = "torso"
        self.parent_object = parent_object
        self.anchor_position = anchor_position
        self.position = None

        self.update_position()

    def update_position(self):
        self.position = self.parent_object.turtle.pos()

    def update(self):
        self.update_position()

class Torso(BodyComponent):




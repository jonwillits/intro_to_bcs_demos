import math

class BodyComponent:
    def __init__(self, parent_object, anchor_position):
        self.parent_object = parent_object
        self.anchor_position = anchor_position
        self.position = None

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
        component_offset = self.anchor_offset_dict[self.anchor_position]

        self.position = tuple(a + b for a, b in zip(turtle_position, component_offset))

    def update(self):
        self.update_position()


class Joint:

    def __init__(self, parent_object, component1, component2, component1_anchor_position, component2_anchor):
        self.parent_object = parent_object
        self.component1 = component1
        self.component2 = component2
        self.component1_anchor = component1_anchor_position
        self.component2_anchor = component2_anchor



'''
    stem cell splits and splits and splits and eventually differentiates
        - body cells
        - actuator cells
        - sensor cells
        - absorber cells
        - 
        - neural cells


'''
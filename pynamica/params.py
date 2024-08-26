
class Display:
    width = 1920
    height = 1080

class Entity:
    count = 0
    shape = "ellipse"
    height = 50
    width = 50
    color = (128, 128, 128)
    starting_orientation = 0

class HeatSource:
    count = 1
    mass = 10
    intensity = 1
    shape = "ellipse"
    height = 50
    width = 50
    color = (255, 155, 0)
    starting_orientation = 0

class RedVehicle:
    count = 1
    mass = 10
    max_speed = 10
    shape = "rectangle"
    height = 20
    width = 5
    color = (255, 0, 0)
    starting_orientation = 0

class BlueVehicle:
    count = 1
    mass = 10
    max_speed = 10
    shape = "rectangle"
    height = 20
    width = 5
    color = (0, 0, 255)
    starting_orientation = 0

def get_param_dict():
    param_dict = {}
    for class_name, class_reference in globals().items():
        # Check if the item is a class defined in this module
        if isinstance(class_reference, type):
            # Convert class attributes to a dictionary
            attributes = {key: value for key, value in class_reference.__dict__.items() if not key.startswith('__')}
            param_dict[class_name] = attributes
    return param_dict
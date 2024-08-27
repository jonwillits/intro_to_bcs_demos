
class Display:
    category = "display"
    width = 1920
    height = 1080

class HeatSource:
    category = "entity"
    count = 1
    mass = 1
    intensity = 1
    shape = "ellipse"
    height = 50
    width = 50
    color = (255, 155, 0)

class Torso:
    category = "body_component"
    mass = 1
    shape = "rectangle"
    height = 80
    width = 20

class HeatSensor:
    category = "sensor"
    mass = 1
    shape = "rectangle"
    sensor_type = "HeatSource"
    height = 10
    width = 10
    color = (0, 0, 0)

class Wheel:
    category = "actuator"
    mass = 1
    shape = "rectangle"
    height = 20
    width = 5
    color = (0, 0, 0)

class GreenVehicle:
    category = "entity"
    count = 1

class RedVehicle:
    category = "entity"
    count = 1

class BlueVehicle:
    category = "entity"
    count = 1






def get_param_dict():
    param_dict = {}
    for class_name, class_reference in globals().items():
        # Check if the item is a class defined in this module
        if isinstance(class_reference, type):
            # Convert class attributes to a dictionary
            attributes = {key: value for key, value in class_reference.__dict__.items() if not key.startswith('__')}
            param_dict[class_name] = attributes
    return param_dict
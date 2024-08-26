import os
import ast


def validate_and_extend_rgb_tuple(rgb_tuple):
    # Check if the tuple has exactly three elements
    if len(rgb_tuple) != 3:
        raise ValueError(f"Tuple must have exactly three elements, but {len(rgb_tuple)} elements were provided.")

    # Check if all elements are integers between 0 and 255
    for i, value in enumerate(rgb_tuple):
        if not isinstance(value, int) or not (0 <= value <= 255):
            raise ValueError(f"Element {i} of the tuple ({value}) is not an integer between 0 and 255.")

    # If valid, return the tuple with an added zero at the end
    return rgb_tuple + (0,)


def validate_nonnegative_integer(value):

    # Check if the value is an integer
    if isinstance(value, int):
        if value >= 0:
            return value
        else:
            raise ValueError(f"Value must be a nonzero positive integer, but {value} was provided.")

    # Check if the value is a float
    elif isinstance(value, float):
        if value >= 0:
            return round(value)
        else:
            raise ValueError(f"Value must be a nonzero positive integer or float, but {value} was provided.")

    # If the value is neither an integer nor a float, raise an exception
    else:
        raise ValueError(
            f"Value must be a nonzero positive integer or float, but {type(value).__name__} was provided.")

def validate_positive_integer(value):
    # Check if the value is an integer
    if isinstance(value, int):
        if value > 0:
            return value
        else:
            raise ValueError(f"Value must be a nonzero positive integer, but {value} was provided.")

    # Check if the value is a float
    elif isinstance(value, float):
        if value > 0:
            return round(value)
        else:
            raise ValueError(f"Value must be a nonzero positive integer or float, but {value} was provided.")

    # If the value is neither an integer nor a float, raise an exception
    else:
        raise ValueError(
            f"Value must be a nonzero positive integer or float, but {type(value).__name__} was provided.")

def validate_number(value):
    if isinstance(value, (int, float)):
        return value
    else:
        raise ValueError(f"Value must be a float or int, but {type(value).__name__} was provided.")

def normalize_angle(value):
    # Normalize the value to be within the range [0, 360)
    normalized_value = value % 360
    # Ensure the result is a positive angle between 0 and 360
    return normalized_value if normalized_value >= 0 else normalized_value + 360


def validate_shape(shape):
    if shape is None:
        shape = 'ellipse'
    if shape != 'ellipse' and shape != 'rectangle':
        raise Exception(f"ERROR: Unrecognized shape {shape}")
    return shape

def get_class_names_from_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        tree = ast.parse(content, filename=file_path)

    class_name_list = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    class_name_set = set(class_name_list)
    return class_name_set

def get_class_names_set_from_files(file_names_list):
    class_names_dict = {}

    for file_name in file_names_list:
        with open(file_name, "r") as file:
            file_content = file.read()
            # Parse the content of the file into an AST
            tree = ast.parse(file_content, filename=file_name)

            # Walk the AST and extract class names
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_names_dict[node.name] = file_name

    return class_names_dict

def list_py_files(directory):
    py_files = []
    # Walk through the directory recursively
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                # Append the full path to the file name
                py_files.append(os.path.join(root, file))
    return py_files

def validate_attribute(attribute_type, value):
    if attribute_type == "color":
        return validate_and_extend_rgb_tuple(value)
    elif attribute_type == "count":
        return validate_nonnegative_integer(value)
    elif attribute_type == "height":
        return validate_positive_integer(value)
    elif attribute_type == "width":
        return validate_positive_integer(value)
    elif attribute_type == "starting_orientation":
        angle = validate_number(value)
        return normalize_angle(angle)
    elif attribute_type == "shape":
        return validate_shape(value)
    elif attribute_type == "mass":
        return validate_number(value)

    else:
        print(f"No validation function exists for {attribute_type} attribute.")
        return value

def set_entity_defaults(params):
    if 'width' not in params:
        params['width'] = 50
    if 'height' not in params:
        params['height'] = 50
    if 'shape' not in params:
        params['shape'] = 'ellipse'
    if 'starting_orientation' not in params:
        params['starting_orientation'] = 0
    if 'color' not in params:
        params['color'] = (128, 128, 128)

    return params
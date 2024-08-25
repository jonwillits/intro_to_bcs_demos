import os
import shutil
from PIL import Image, ImageDraw


def create_rotated_shape_images(width, height, shape, color, path, angles=24):
    # Calculate the rotation step based on the number of angles
    step = 360 // angles

    # Create the directory, overwrite if it exists
    if os.path.exists(path):
        shutil.rmtree(path)  # Remove the existing directory
    os.makedirs(path)  # Create a new directory

    # Determine the canvas size and background color
    if shape == "rectangle":
        image_size = (width, height)
        background_color = (255, 255, 255, 255)  # Opaque background for rectangles
    elif shape == "ellipse":
        image_size = (width, height)
        background_color = (255, 255, 255, 0)  # Transparent background for ellipses
    else:
        raise ValueError("Invalid shape parameter. Allowed values are 'ellipse' and 'rectangle'.")

    # Create the base image with the specified background
    base_image = Image.new("RGBA", image_size, background_color)
    draw = ImageDraw.Draw(base_image)

    # Draw the shape
    if shape == "rectangle":
        draw.rectangle([0, 0, width, height], fill=color)
    elif shape == "ellipse":
        draw.ellipse([0, 0, width, height], fill=color)

    # Save rotated images in the directory
    for i in range(angles):
        angle = i * step
        rotated_image = base_image.rotate(angle, expand=True)
        rotated_image.save(os.path.join(path, f"{shape}_{angle}.gif"), 'GIF')

# Example usage:
# create_rotated_shape_images(100, 50, "ellipse", "blue", "./shapes/ellipse", angles=24)
def validate_and_extend_rgb_tuple(rgb_tuple):
    if rgb_tuple is None:
        rgb_tuple = (128, 128, 128)

    # Check if the tuple has exactly three elements
    if len(rgb_tuple) != 3:
        raise ValueError(f"Tuple must have exactly three elements, but {len(rgb_tuple)} elements were provided.")

    # Check if all elements are integers between 0 and 255
    for i, value in enumerate(rgb_tuple):
        if not isinstance(value, int) or not (0 <= value <= 255):
            raise ValueError(f"Element {i} of the tuple ({value}) is not an integer between 0 and 255.")

    # If valid, return the tuple with an added zero at the end
    return rgb_tuple + (0,)


def validate_positive_integer(value):

    if value is None:
        value = 10
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

def normalize_angle(value):
    # Check if the value is a float or an int
    if isinstance(value, (int, float)):
        # Normalize the value to be within the range [0, 360)
        normalized_value = value % 360
        # Ensure the result is a positive angle between 0 and 360
        return normalized_value if normalized_value >= 0 else normalized_value + 360
    else:
        raise ValueError(f"Value must be a float or int, but {type(value).__name__} was provided.")

import os
import shutil
from PIL import Image, ImageDraw

import math

def get_point_on_shape(shape, width, height, xy_position, rotation, direction):
    x, y = xy_position
    rotation_radians = math.radians(rotation)

    # Define direction vectors (normalized)
    direction_vectors = {
        'n': (0, 1),
        's': (0, -1),
        'e': (1, 0),
        'w': (-1, 0),
        'ne': (math.sqrt(2)/2, math.sqrt(2)/2),
        'nw': (-math.sqrt(2)/2, math.sqrt(2)/2),
        'se': (math.sqrt(2)/2, -math.sqrt(2)/2),
        'sw': (-math.sqrt(2)/2, -math.sqrt(2)/2),
    }

    dx, dy = direction_vectors[direction]

    if shape == 'rectangle':
        half_width = width / 2
        half_height = height / 2

        # Rotate the direction vector
        rotated_dx = dx * math.cos(rotation_radians) - dy * math.sin(rotation_radians)
        rotated_dy = dx * math.sin(rotation_radians) + dy * math.cos(rotation_radians)

        # Scale the vector by the rectangle's half-dimensions
        point_x = x + rotated_dx * half_width
        point_y = y + rotated_dy * half_height

    elif shape == 'ellipse':
        # Ellipse requires parametric equations and consideration of rotation
        # Calculate the angle for the direction
        direction_angle = math.atan2(dy, dx)

        # Adjust the direction angle by the rotation of the ellipse
        total_angle = direction_angle + rotation_radians

        # Use the parametric equations for an ellipse
        point_x = x + (width / 2) * math.cos(total_angle)
        point_y = y + (height / 2) * math.sin(total_angle)
    else:
        raise ValueError("Shape must be 'rectangle' or 'ellipse'.")

    return point_x, point_y


def create_rotated_shape_images(path, width=50, height=50, shape="ellipse", color=(128, 128, 128), angles=24):
    print(width, height, shape, color, path, angles)

    # Ensure the color is fully opaque
    color = (*color[:3], 255)  # Ensure the color is RGB + fully opaque alpha

    # Calculate the rotation step based on the number of angles
    step = 360 // angles

    # Create the directory, overwrite if it exists
    if os.path.exists(path):
        shutil.rmtree(path)  # Remove the existing directory
    os.makedirs(path)  # Create a new directory

    # Add padding to avoid clipping during rotation
    padding = max(width, height) // 10
    padded_width = width + 2 * padding
    padded_height = height + 2 * padding

    # Ensure the background is always transparent
    background_color = (255, 255, 255, 255)  # Transparent background

    print(f"Image size with padding: {padded_width}x{padded_height}, Background: Transparent")

    # Create the base image with the specified transparent background
    base_image = Image.new("RGBA", (padded_width, padded_height), background_color)
    draw = ImageDraw.Draw(base_image)

    # Draw the shape with padding
    if shape == "rectangle":
        draw.rectangle([padding, padding, padded_width - padding, padded_height - padding], fill=color)
    elif shape == "ellipse":
        draw.ellipse([padding, padding, padded_width - padding, padded_height - padding], fill=color)
    else:
        raise ValueError("Invalid shape parameter. Allowed values are 'ellipse' and 'rectangle'.")

    # Save the original base image
    base_image.save(os.path.join(path, f"{shape}_0.gif"), 'GIF')

    # Save rotated images in the directory
    for i in range(angles - 1):
        angle = (i + 1) * step
        rotated_image = base_image.rotate(angle, expand=True)

        # Create a new image with a transparent background to fit the rotated shape
        new_size = rotated_image.size
        final_image = Image.new("RGBA", new_size, background_color)
        final_image.paste(rotated_image, (0, 0), rotated_image)

        # Save the rotated image
        final_image.save(os.path.join(path, f"{shape}_{angle}.gif"), 'GIF')
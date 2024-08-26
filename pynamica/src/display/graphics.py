import os
import shutil
from PIL import Image, ImageDraw

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
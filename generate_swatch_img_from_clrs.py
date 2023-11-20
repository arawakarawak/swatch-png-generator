import json
import random
from PIL import Image, ImageDraw

def two_complement_to_hex(n):
    """Convert a negative decimal number to a 6-digit hexadecimal RGB value."""
    return '{:08X}'.format(n & 0xFFFFFFFF)[2:]

def generate_swatch_image(num_swatches=64, num_rows=4, divider_thickness=10, frame_thickness=10, frame_color="#828382", color_file=None):
    # Function to generate a random RGB color
    def random_rgb():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # Load colors from the .clrs file if provided
    colors = []
    if color_file:
        with open(color_file, 'r') as file:
            data = json.load(file)
            for n in data.get("colors", []):
                hex_color = two_complement_to_hex(n)
                rgb_color = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
                colors.append(rgb_color)
        # Limit num_swatches to the number of colors in the file
        num_swatches = len(colors)
    else:
        # Fill in the swatches with random colors
        while len(colors) < num_swatches:
            colors.append(random_rgb())

    # Calculate number of columns and image size
    num_cols = -(-num_swatches // num_rows)  # Ceiling division
    swatch_size = 100
    img_width = num_cols * (swatch_size + divider_thickness) + frame_thickness * 2 - divider_thickness
    img_height = num_rows * (swatch_size + divider_thickness) + frame_thickness * 2 - divider_thickness

    # Create the image
    img = Image.new("RGB", (img_width, img_height), color=frame_color)
    draw = ImageDraw.Draw(img)

    # Draw the swatches
    for row in range(num_rows):
        for col in range(num_cols):
            index = row * num_cols + col
            if index < num_swatches:
                x0 = frame_thickness + col * (swatch_size + divider_thickness)
                y0 = frame_thickness + row * (swatch_size + divider_thickness)
                draw.rectangle([x0, y0, x0 + swatch_size, y0 + swatch_size], fill=colors[index])

    # Save the image
    img.save('palette.png')
    
color_file='./colors.clrs'
# Example usage
# generate_swatch_image()  # This will save the image as 'palette.png' immediately
generate_swatch_image(color_file='colors.clrs')  # This will use colors from the .clrs file and save as 'palette.png'

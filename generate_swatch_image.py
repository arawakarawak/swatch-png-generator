import csv
import random
from PIL import Image, ImageDraw

def generate_swatch_image(num_swatches=64, num_rows=4, divider_thickness=10, frame_thickness=10, frame_color="#828382", color_file=None):
    # Function to generate a random RGB color
    def random_rgb():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # Load colors from the CSV file if provided
    colors = []
    if color_file:
        with open(color_file, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) >= 3:
                    try:
                        colors.append(tuple(map(int, row[:3])))
                    except ValueError:
                        pass  # Skip invalid entries

    # Update num_swatches if there are more colors in the CSV file
    if len(colors) > num_swatches:
        num_swatches = len(colors)
    else:
        # Fill in the remaining swatches with random colors
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

# Example usage
generate_swatch_image()  # This will save the image as 'palette.png' immediately
# generate_swatch_image(color_file='colors.csv')  # This will use colors from the CSV and save as 'palette.png'

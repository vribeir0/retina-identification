from PIL import Image, ImageDraw
import numpy as np
from math import sqrt


def sobel_operator(input_image):
    input_pixels = input_image.load()
    width, height = input_image.size

    output_image = Image.new("RGB", input_image.size)
    draw = ImageDraw.Draw(output_image)

    intensity = to_grayscale(width, height, input_pixels)

    # Compute convolution between intensity and kernels
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            magx = intensity[x + 1, y] - intensity[x - 1, y]
            magy = intensity[x, y + 1] - intensity[x, y - 1]

            # Draw in black and white the magnitude
            color = int(sqrt(magx**2 + magy**2))
            draw.point((x, y), (color, color, color))

    return output_image


def to_grayscale(width, height, input_pixels):
    intensity = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            intensity[x, y] = sum(input_pixels[x, y]) / 3
    return intensity


def main():
    result_folder = "result/edge"

    input_image = Image.open("frames/frame1.jpg")
    output_image = sobel_operator(input_image)

    FolderUtils.create_if_not_exists(result_folder)
    output_image.save(result_folder + "edge.png")


if __name__ == "__main__":
    main()

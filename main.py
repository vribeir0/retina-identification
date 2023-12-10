from PIL import Image, ImageDraw
import numpy as np
from math import sqrt
import cv2
from utils import FolderUtils
import os
import re 

# Ajuste conforme necessário
min_area = 2000
max_area = 5000


# def sobel_operator(input_image):
#     input_pixels = input_image.load()
#     width, height = input_image.size

#     print("width: " + str(width))
#     print("height: " + str(height))

#     output_image = Image.new("RGB", input_image.size)
#     draw = ImageDraw.Draw(output_image)

#     intensity = to_grayscale(width, height, input_pixels)

#     # Compute convolution between intensity and kernels
#     for x in range(1, width - 1):
#         for y in range(1, height - 1):
#             magx = intensity[x + 1, y] - intensity[x - 1, y]
#             magy = intensity[x, y + 1] - intensity[x, y - 1]

#             # Draw in black and white the magnitude
#             color = int(sqrt(magx**2 + magy**2))
#             draw.point((x, y), (color, color, color))

#     return output_image


# def to_grayscale(width, height, input_pixels):
#     intensity = np.zeros((width, height))
#     for x in range(width):
#         for y in range(height):
#             intensity[x, y] = sum(input_pixels[x, y]) / 3
#     return intensity

def canny_edge_detector(input_image):
    numpy_image = np.array(input_image)

    gray_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2GRAY)

    # Blur the image to improve detection
    gray_image = cv2.medianBlur(gray_image, 5)

    # Use HoughCircles to detect circles
    circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 20, param1=110, param2=50)

    area = 0
    image = numpy_image
    # circles[0, :] contains the circles detected
    if circles is not None:
        circles = np.uint16(np.around(circles))

        # Find the circle with the largest radius
        max_radius_i = np.argmax(circles[0, :, 2])
        i = circles[0, max_radius_i]
        
        # Draw the outer circle
        image = cv2.circle(numpy_image, (i[0], i[1]), i[2], (255, 255, 255), 1)

        area = np.pi * (i[2] ** 2)

    return area, image

def calculate_relative_variation(current, previous):
    if previous == 0:
        return 0
    else:
        return (current - previous) / previous
    
def apply_clahe(image):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return clahe.apply(image)

def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

def main():
    result_folder = "result/edge"
    frames_folder = "frames"
    frame_files = [x for x in sorted(os.listdir(frames_folder), key=extract_number) if x.endswith(".jpg")]
    print("frame files: " + str(len(frame_files)))

    FolderUtils.create_if_not_exists(result_folder)
    previous_area = 0
    relative_variation_media = []

    for frame_file in frame_files:
        print("frame: " + frame_file)

        input_image = Image.open(os.path.join(frames_folder, frame_file))
        # input_image = apply_clahe(input_image)
        area, output_image = canny_edge_detector(input_image)
        print("area: " + str(area))

        output_image = Image.fromarray(output_image)    
        output_image.save(os.path.join(result_folder, "edge" + frame_file))

        relative_variation = calculate_relative_variation(area, previous_area)
        print("relative variation: " + str(relative_variation))

        relative_variation_media.append(relative_variation) 

        previous_area = area

    print("percentual relative variation media: " + str(abs(np.mean(relative_variation_media))*100))

    # FolderUtils.create_if_not_exists(result_folder)
    # output_image.save(result_folder + "edge.png")

if __name__ == "__main__":
    main()


    # _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

    # contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # print("contours: " + str(len(contours))) 

    # # Encontre o contorno com base em critérios específicos (ajuste conforme necessário)
    # for contour in contours:
    #     area = cv2.contourArea(contour)
    #     print("area: " + str(area)) 
    #     if area > min_area and area < max_area:
    #        print(area) 

    # # Desenhe os contornos na imagem original
    # cv2.drawContours(numpy_image, contours, -1, (255, 255, 0), 1)
from PIL import Image, ImageDraw
import numpy as np
from math import sqrt
import cv2
from utils import FolderUtils
import os
import re
import matplotlib.pyplot as plt


def edge_detector(input_image):
    # Tranforma a imagem em matriz para poder manipular os pixels
    numpy_image = np.array(input_image)
    gray_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2GRAY)

    # Blur para suavizar as bordas da imagem
    gray_image = cv2.medianBlur(gray_image, 5)

    circles = cv2.HoughCircles(
        gray_image,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=20,
        param1=120,
        param2=40,
        maxRadius=90,
    )

    area = 0
    image = numpy_image

    # Verifica se a função detectou algum círculo
    if circles is not None:
        circles = np.uint16(np.around(circles))

        # Encontra o círculo com maior raio
        max_radius_i = np.argmax(circles[0, :, 2])
        i = circles[0, max_radius_i]
        # print("i: " + str(i))

        # Desenha o círculo branco em volta da pupila, na imagem original
        image = cv2.circle(numpy_image, (i[0], i[1]), i[2], (255, 255, 255), 1)

        # Calcula a área do círculo
        area = np.pi * (i[2] ** 2)

    return area, image


# Função para calcular a variação relativa entre dois valores
def calculate_relative_variation(current, previous):
    if previous == 0:
        return 0
    else:
        return (current - previous) / previous


def apply_clahe(image):
    # O CLAHE é uma extensão do equalizador de histograma que limita a amplificação em áreas de alto contraste,
    # o que é especialmente útil quando há muita variação de luz.
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(image)


# Função para ajudar a ler os frames na sequência.
# Utiliza regex para extrair o número do nome do arquivo
def extract_number(filename):
    match = re.search(r"\d+", filename)
    return int(match.group()) if match else 0


def plot_histogram(relative_variation, nome):
    plt.figure(figsize=(10, 5))
    plt.title(nome + " X Frame")
    plt.plot(relative_variation)
    plt.ylabel(nome)
    plt.xlabel("Frame")
    plt.show()


def main():
    result_folder = "result/edge"
    frames_folder = "frames"
    frame_files = [
        x
        for x in sorted(os.listdir(frames_folder), key=extract_number)
        if x.endswith(".jpg")
    ]
    print("frame files: " + str(len(frame_files)))

    FolderUtils.create_if_not_exists(result_folder)

    previous_area = 0
    relative_variation_media = []
    area_media = []
    for frame_file in frame_files:
        # print("frame: " + frame_file)

        input_image = Image.open(os.path.join(frames_folder, frame_file))

        area, output_image = edge_detector(input_image)

        # print("area: " + str(area))

        output_image = Image.fromarray(output_image)
        output_image.save(os.path.join(result_folder, "edge" + frame_file))

        relative_variation = calculate_relative_variation(area, previous_area)
        # print("relative variation: " + str(relative_variation))

        relative_variation_media.append(relative_variation)
        area_media.append(area)

        previous_area = area

    plot_histogram(relative_variation_media, "Variação relativa")
    plot_histogram(area_media, "Area")

    print(
        "percentual relative variation media: "
        + str(abs(np.mean(relative_variation_media)) * 100)
    )


if __name__ == "__main__":
    main()

from PIL import Image, ImageDraw
import numpy as np
from math import sqrt
import cv2
from utils import FolderUtils
import os
import re
import matplotlib.pyplot as plt

def canny_edge_detector(input_image):
    # Tranforma a imagem em matriz para poder manipular os pixels
    numpy_image = np.array(input_image)

    # Tentativa de melhorar a detecção de bordas, mas não funcionou
    #clahe_image = apply_clahe(numpy_image)

    # Tenta melhorar a detecção de bordas, mas não funcionou
    # equalized_image = cv2.equalizeHist(gray_image)

    # Converte a imagem para escala de cinza
    gray_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2GRAY)

    # Blur the image to improve detection
    gray_image = cv2.medianBlur(gray_image, 5)

    # Função para detectar os círculos na imagem
    circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 20, param1=120, param2=40)

    area = 0
    image = numpy_image

    # Verifica se a função detectou algum círculo
    if circles is not None:
        circles = np.uint16(np.around(circles))

        # Encontra o círculo com maior raio
        max_radius_i = np.argmax(circles[0, :, 2])
        i = circles[0, max_radius_i]

        # Desenha o círculo branco em volta da pupila, na imagem original
        image = cv2.circle(numpy_image, (i[0], i[1]), i[2], (255, 255, 255), 1)
        
        # Preenche o círculo branco de preto, para retirar os reflexos que aparecem, na imagem original
        image = cv2.circle(image, (i[0], i[1]), i[2] - 5, (0, 0, 0), -1)

        # Calcula a área do círculo
        area = np.pi * (i[2] ** 2)

    return area, image

# Função para calcular a variação relativa entre dois valores
def calculate_relative_variation(current, previous):
    if previous == 0:
        return 0
    else:
        return (current - previous) / previous
    
# O CLAHE é uma extensão do equalizador de histograma que limita a amplificação em áreas de alto contraste, 
# o que é especialmente útil quando há muita variação de luz.
def apply_clahe(image):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return clahe.apply(image)

# Função para ajudar a ler os frames na sequência.
# Utiliza regex para extrair o número do nome do arquivo
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

# Função para plotar os histograma de variação relativa e área
def plot_histogram(relative_variation, nome):
    plt.figure(figsize=(10,5))
    plt.title('Histograma ' + nome + ' X Frame')
    plt.plot(relative_variation)
    plt.ylabel(nome)
    plt.xlabel('Frame')
    plt.show()

def main():
    result_folder = "result/edge"
    frames_folder = "frames"
    frame_files = [x for x in sorted(os.listdir(frames_folder), key=extract_number) if x.endswith(".jpg")]

    FolderUtils.create_if_not_exists(result_folder)

    previous_area = 0
    relative_variation_media = []
    area_media = []

    for frame_file in frame_files:
        input_image = Image.open(os.path.join(frames_folder, frame_file))

        area, output_image = canny_edge_detector(input_image)
        
        output_image = Image.fromarray(output_image)    
        output_image.save(os.path.join(result_folder, "edge" + frame_file))

        relative_variation = calculate_relative_variation(area, previous_area)

        # Adiciona a variação relativa e a área na lista para plotar o histograma
        relative_variation_media.append(relative_variation) 
        area_media.append(area)

        previous_area = area

        print('##############################')
        print("Relatório frame: " + frame_file)
        print("Área: " + str(area))
        print("Variação Relativa: " + str(relative_variation))

    plot_histogram(relative_variation_media, 'Variação Relativa')
    plot_histogram(area_media, 'Área')
    
    print("Percentual de Variação Relativa Média: " + str(abs(np.mean(relative_variation_media))*100))

if __name__ == "__main__":
    main()
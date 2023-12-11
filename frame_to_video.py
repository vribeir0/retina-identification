import cv2
import os
import re

# Função para extrair o número do nome do arquivo
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

# Pasta onde os frames estão armazenados
frames_folder = "result/edge"

# Obter a lista de nomes de arquivos de frames
frame_files = [x for x in sorted(os.listdir(frames_folder), key=extract_number) if x.endswith(".jpg")]

# Ler o primeiro frame para obter as dimensões
first_frame = cv2.imread(os.path.join(frames_folder, frame_files[0]))
height, width, layers = first_frame.shape

# Especificar o nome do arquivo de saída, o codec, a taxa de quadros e as dimensões do vídeo
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
video = cv2.VideoWriter('output.mp4', fourcc, 30.0, (width, height))

# Adicionar cada frame ao vídeo
for frame_file in frame_files:
    frame = cv2.imread(os.path.join(frames_folder, frame_file))
    video.write(frame)

# Finalizar o vídeo
video.release()
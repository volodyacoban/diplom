import cv2
import numpy as np
import pandas as pd


# Чтение CSV-файла
csv_path = 'C:/Users/grrra/PycharmProjects/diplom/data_out.csv'
df = pd.read_csv(csv_path)

# Загрузка видео
video_path = 'C:/Users/grrra/PycharmProjects/diplom/output/video_2024-03-28_12-44-29_output.mp4'
cap = cv2.VideoCapture(video_path)

# Получение информации о видео
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Функция добавления PNG-изображения в правый верхний угол кадра
def add_smile_to_frame(frame, smile_image_path):
    target_width = 120
    target_height = 120
    image = cv2.imread(smile_image_path, cv2.IMREAD_UNCHANGED)
    image_resized = cv2.resize(image, (target_width, target_height))

    start_x = width - image_resized.shape[1]
    end_x = width
    start_y = 0
    end_y = image_resized.shape[0]

    frame[start_y:end_y, start_x:end_x] = image_resized[:, :, :3] * (image_resized[:, :, 3:] / 255.0) + frame[start_y:end_y, start_x:end_x] * (1.0 - image_resized[:, :, 3:] / 255.0)

    return frame

# Обработка каждого кадра видео
frames = []
for index, row in df.iterrows():
    ret, frame = cap.read()
    if not ret:
        break

    if row['Column Name'] == 'angry':
        modified_frame = add_smile_to_frame(frame, 'C:/Users/grrra/PycharmProjects/diplom/smiles/angry.png')
    if row['Column Name'] == 'disgust':
        modified_frame = add_smile_to_frame(frame, 'C:/Users/grrra/PycharmProjects/diplom/smiles/disgust.png')
    if row['Column Name'] == 'fear':
        modified_frame = add_smile_to_frame(frame, 'C:/Users/grrra/PycharmProjects/diplom/smiles/fear.png')
    if row['Column Name'] == 'neutral':
        modified_frame = add_smile_to_frame(frame, 'C:/Users/grrra/PycharmProjects/diplom/smiles/neutral.png')
    if row['Column Name'] == 'sad':
        modified_frame = add_smile_to_frame(frame, 'C:/Users/grrra/PycharmProjects/diplom/smiles/sad.png')
    if row['Column Name'] == 'surprise':
        modified_frame = add_smile_to_frame(frame, 'C:/Users/grrra/PycharmProjects/diplom/smiles/surprise.png')
    elif row['Column Name'] == 'happy':
        modified_frame = add_smile_to_frame(frame, 'C:/Users/grrra/PycharmProjects/diplom/smiles/happy.png')
    else:
        modified_frame = frame

    frames.append(modified_frame)

# Сохранение измененного видео
output_path = 'output_video_with_smiles.mp4'
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
for frame in frames:
    out.write(frame)

# Освобождение ресурсов
cap.release()
out.release()
cv2.destroyAllWindows()
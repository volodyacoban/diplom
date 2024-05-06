import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QFileDialog, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from fer import FER
from fer import Video
import pandas as pd
import openpyxl
import os.path
from os import path
import cv2
import os
import csv
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Real emotions')
        self.setGeometry(100, 100, 800, 600)

        # Создание левого верхнего угла с логотипом
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap('C:/Users/grrra/PycharmProjects/diplom/images/logo.png').scaled(int(self.logo_label.width()/3), int(self.logo_label.height()/3)))

        # Создание текстового поля для вывода результатов
        self.result_text = QTextEdit()

        # Создание метки для отображения режима работы программы
        self.mode_label = QLabel('Режим работы: Распознавание эмоций')

        # Создание кнопки переключения режимов
        self.mode_button = QPushButton('Переключить режим')
        self.mode_button.clicked.connect(self.switch_mode)

        # Создание вертикального макета для левой части окна
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.logo_label)
        left_layout.addWidget(self.result_text)
        left_layout.addWidget(self.mode_label)
        left_layout.addWidget(self.mode_button)

        # Создание правой части окна для первого режима работы
        self.first_mode_widget = QWidget()
        self.first_mode_layout = QVBoxLayout()
        self.first_mode_button1 = QPushButton('Распознать эмоции')
        self.first_mode_button1.clicked.connect(self.recognize_emotions)
        self.first_mode_button2 = QPushButton('Выбрать директорию для распознавания')
        self.first_mode_button2.clicked.connect(self.select_directory)
        self.first_mode_layout.addWidget(self.first_mode_button1)
        self.first_mode_layout.addWidget(self.first_mode_button2)
        self.first_mode_widget.setLayout(self.first_mode_layout)

        # Создание правой части окна для второго режима работы
        self.second_mode_widget = QWidget()
        self.second_mode_layout = QVBoxLayout()
        self.second_mode_button1 = QPushButton('Выбрать видео')
        self.second_mode_button1.clicked.connect(self.select_video)
        self.second_mode_button2 = QPushButton('Выбрать директорию')
        self.second_mode_button2.clicked.connect(self.select_directory_for_video)
        self.second_mode_button3 = QPushButton('Обрезать видеоряд')
        self.second_mode_button3.clicked.connect(self.crop_video)
        self.second_mode_layout.addWidget(self.second_mode_button1)
        self.second_mode_layout.addWidget(self.second_mode_button2)
        self.second_mode_layout.addWidget(self.second_mode_button3)
        self.second_mode_widget.setLayout(self.second_mode_layout)

        # Создание горизонтального макета для размещения левой и правой частей окна
        right_layout = QHBoxLayout()
        right_layout.addWidget(self.first_mode_widget)
        right_layout.addWidget(self.second_mode_widget)

        # Создание общего макета для окна
        main_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Создание главного виджета и установка макета
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Скрытие второго режима работы по умолчанию
        self.second_mode_widget.hide()

    def switch_mode(self):
        # Переключение видимости первого и второго режимов работы
        if self.first_mode_widget.isVisible():
            self.first_mode_widget.hide()
            self.second_mode_widget.show()
            self.mode_label.setText('Режим работы: Обработка видео')
        else:
            self.first_mode_widget.show()
            self.second_mode_widget.hide()
            self.mode_label.setText('Режим работы: Распознавание эмоций')

    def recognize_emotions(self):
        emotion_detector = FER(mtcnn=True)
        dir = os.listdir(self.directory)
        dict_name = {1: 'A1', 2: 'B1', 3: 'C1', 4: 'D1', 5: 'F1'}
        dict_result = {1: 'A2', 2: 'B2', 3: 'C2', 4: 'D2', 5: 'F2'}
        i = 1
        input_filename = 'C:/Users/grrra/PycharmProjects/diplom/data.csv'
        output_filename = 'C:/Users/grrra/PycharmProjects/diplom/data_out.csv'
        video_dir = 'C:/Users/grrra/PycharmProjects/diplom/output/'

        for item in dir:
            name = dict_name.get(i)
            res = dict_result.get(i)
            wb = openpyxl.Workbook()
            sheet = wb.active

            path_to_video = self.directory + item
            video = Video(path_to_video)
            result = video.analyze(emotion_detector, display=False)
            # dominant_emotion = emotion_detector.top_emotion(item)
            emotions_df = video.to_pandas(result)
            emotions_df.head()
            positive_emotions = sum(emotions_df.happy) + sum(emotions_df.surprise)
            negative_emotions = sum(emotions_df.angry) + sum(emotions_df.disgust) + sum(emotions_df.fear) + sum(
                emotions_df.sad)
            if positive_emotions > negative_emotions:
                emotions_result = "Positive"
            elif positive_emotions < negative_emotions:
                emotions_result = "Negative"
            else:
                emotions_result = "Neutral"
            sheet[name] = item
            sheet[res] = emotions_result
            wb.save('new_excel_file_result.xlsx')
            i += 1

            with open(input_filename, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)

            # Находим индексы столбцов "А" и "Б"
            index_a = data[0].index('angry0')
            index_b = data[0].index('disgust0')
            index_c = data[0].index('fear0')
            index_d = data[0].index('happy0')
            index_e = data[0].index('neutral0')
            index_f = data[0].index('sad0')
            index_j = data[0].index('surprise0')
            index_h = data[0].index('box0')

            # Удаляем все заголовки столбцов, кроме "А" и "Б"
            new_data = [
                [row[index_a], row[index_b], row[index_c], row[index_d], row[index_e], row[index_f], row[index_j],
                 row[index_h]] for row in data]

            # Открываем csv файл для записи
            with open(output_filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(new_data)

            path = item
            filename = os.path.splitext(os.path.basename(path))[0]
            directory = (video_dir + filename + '_output.mp4')
            data = pd.read_csv(output_filename)
            # Удаление столбца "box0"
            data.drop('box0', axis=1, inplace=True)
            # Сохранение данных без столбца "box0" обратно в csv-файл
            data.to_csv(output_filename, index=False)

            with open(output_filename, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                first_row = rows[0]
                first_row_without_zeros = [cell.replace('0', '') for cell in first_row]

            # Запись отредактированных данных в новый CSV файл
            with open(output_filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows([first_row_without_zeros] + rows[1:])

            # Загрузка данных из CSV-файла
            data = pd.read_csv(output_filename)

            # Функция для нахождения наибольшего числа в строке и записи имени столбца
            def max_value_in_row(row):
                max_value = max(row)
                column_name = data.columns[row.tolist().index(max_value)]
                return (max_value, column_name)

            # Применение функции к каждой строке датафрейма
            data[['Max Value', 'Column Name']] = data.apply(max_value_in_row, axis=1, result_type='expand')

            columns_to_drop = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise', 'Max Value']
            data = data.drop(columns=columns_to_drop)
            # Сохранение данных без столбца "box0" обратно в csv-файл
            data.to_csv(output_filename, index=False)
        self.result_text.append("Эмоции успешно распознаны!")

    def select_directory(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку')
        self.directory = folder_path + "/"
        self.result_text.append('Вы выбрали директорию для распознавания:' + self.directory)
        return (self.directory)


    def select_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getOpenFileName(self, 'Выбрать видео-файл', '', 'Видео файлы (*.mp4 *.avi)',
                                                  options=options)
        self.video_file = fileName
        self.result_text.append('Вы выбрали видео для обработки:' + self.video_file)
        return (self.video_file)

    def crop_video(self):
        # Загрузка каскадного классификатора для обнаружения лиц
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # Загрузка видеофайла
        video = cv2.VideoCapture(self.video_file)
        # Получение FPS (количество кадров в секунду) видео
        fps = video.get(cv2.CAP_PROP_FPS)
        output_video_dir = self.output_directory + '/' + 'new_file.mp4'
        # Создание объекта для записи видео
        output = cv2.VideoWriter(output_video_dir, cv2.VideoWriter_fourcc(*"mp4v"), fps,
                                 (int(video.get(3)), int(video.get(4))))
        while True:
            # Чтение следующего кадра видео
            ret, frame = video.read()
            if not ret:
                break
            # Преобразование кадра в оттенки серого
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Обнаружение лиц на кадре
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) == 0:
                # Если лица не найдены, пропускаем кадр
                continue
            # Запись кадра в выходное видео
            output.write(frame)
        # Освобождение ресурсов
        video.release()
        output.release()
        cv2.destroyAllWindows()
        self.result_text.append('Вы выбрали видео для обработки:' + self.video_file)

    def select_directory_for_video(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку')
        self.output_directory = folder_path
        self.result_text.append('Вы выбрали директорию для обработаных видео:' + self.output_directory)
        return (self.output_directory)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
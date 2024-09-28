import cv2
import numpy as np
from typing import BinaryIO, Optional
import os


def get_first_frame_from_binary(binary_io: BinaryIO) -> Optional[np.ndarray]:
    # Читаем данные из BinaryIO
    binary_io.seek(0)  # Убедимся, что мы находимся в начале файла
    video_data = binary_io.read()

    # Преобразуем бинарные данные в массив numpy
    np_data = np.frombuffer(video_data, np.uint8)

    # Декодируем видео из массива numpy
    # Для этого нам нужно создать временный файл
    temp_file_path = "temp_video.mp4"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(np_data)

    # Открываем временный видеофайл
    cap = cv2.VideoCapture(temp_file_path)
    os.remove("temp_video.mp4")

    # Проверяем, удалось ли открыть видео
    if not cap.isOpened():
        print("Ошибка: Не удалось открыть видео.")
        return None

    # Читаем первый кадр
    ret, frame = cap.read()

    # Освобождаем объект VideoCapture
    cap.release()

    # Проверяем, удалось ли прочитать кадр
    if not ret:
        print("Ошибка: Не удалось прочитать кадр.")
        return None

    return frame


if __name__ == "__main__":
    video_path = "video.MP4"  # Укажите путь к вашему видеофайлу
    with open(video_path, "rb") as f:
        first_frame = get_first_frame_from_binary(f)

    if first_frame is not None:
        # Отображаем первый кадр
        cv2.imshow("Первый кадр", first_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

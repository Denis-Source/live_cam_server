import os
import cv2
import datetime


class CameraUtils:
    @staticmethod
    def put_text(frame, text):
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame = cv2.putText(frame, text, (10, 40), font, 1, (0, 0, 0), 5, cv2.LINE_8)
        frame = cv2.putText(frame, text, (10, 40), font, 1, (255, 255, 255), 4, cv2.LINE_8)
        return frame

    @staticmethod
    def add_timestamp(frame):
        return CameraUtils.put_text(
            frame,
            datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        )

    @staticmethod
    def generate_filename(home_path, folder, file_format):
        filename = f"{datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S-%f')}.{file_format}"
        return os.path.join(os.path.join(home_path, folder), filename)

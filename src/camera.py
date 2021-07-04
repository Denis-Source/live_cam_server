from src.camera_settings import CameraSettings
from src.camera_utils import CameraUtils

import cv2
import time
import threading
import io
import os


class Camera(CameraSettings):
    def __init__(self):
        super().__init__()

        self.to_capture = False
        self.to_search = False

        self.home_path = os.path.abspath(os.getcwd())
        self.frame_pause = 1 / self.framerate
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
        self.no_feed_image = cv2.imread(self.no_feed_image_path, cv2.IMREAD_COLOR)

        self.device = None
        self.last_frame = []
        self.last_stamped_frame = []
        self.last_object_rects = []
        self.last_stream_frame = []

    def capture(self):
        while self.to_capture:
            success, cur_frame = self.device.read()
            if success:
                cur_frame = cv2.resize(cur_frame, self.resolution)
            else:
                cur_frame = self.no_feed_image.copy()
            self.last_frame = cur_frame.copy()
            self.last_stamped_frame = CameraUtils.add_timestamp(cur_frame.copy())
            for (x, y, w, h) in self.last_object_rects:
                cv2.rectangle(self.last_stamped_frame, (x, y), (x + w, y + h), (50, 50, 250), 2)
            ret, buffer = cv2.imencode(".jpg", self.last_stamped_frame, self.encode_param)
            frame_bytes = buffer.tobytes()
            self.last_stream_frame = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'

    def gen_frame(self):
        while True:
            time.sleep(self.frame_pause)
            yield self.last_frame

    def gen_stamped_frame(self):
        while True:
            time.sleep(self.frame_pause)
            yield self.last_stamped_frame

    def gen_stream(self):
        while True:
            time.sleep(self.frame_pause)
            yield self.last_stream_frame

    def search_objects(self):
        self.to_search = True
        cascade = cv2.CascadeClassifier(self.cascade_file)
        while self.to_search:
            try:
                gray = cv2.cvtColor(cv2.UMat(self.last_frame), cv2.COLOR_RGB2GRAY)
                self.last_object_rects = cascade.detectMultiScale(gray, 1.1, 4)
            except cv2.error:
                self.last_object_rects = []
        else:
            self.last_object_rects = []

    def take_photo(self, in_memory=True):
        frame = CameraUtils.add_timestamp(self.last_frame)
        if in_memory:
            ret, buffer = cv2.imencode(f".{self.photo_format}", frame, self.encode_param)
            img_io = io.BytesIO(buffer)
            return img_io
        else:
            filename = CameraUtils.generate_filename(self.home_path, self.folder, self.photo_format)
            cv2.imwrite(filename, frame)
            return filename

    def record(self, seconds):
        file_name = CameraUtils.generate_filename(self.home_path, self.folder, self.video_format)
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        fourcc = cv2.VideoWriter_fourcc(*self.video_codec)
        video_writer = cv2.VideoWriter()
        video_writer.open(file_name, fourcc, self.framerate, self.resolution, True)

        for i in range(seconds * self.framerate):
            try:
                video_writer.write(next(self.gen_stamped_frame()))
            except cv2.error:
                pass
                video_writer.write(self.no_feed_image)
        video_writer.release()
        return file_name

    def start(self):
        self.to_capture = False
        self.stop()
        self.to_capture = True
        self.device = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        threading.Thread(target=self.capture).start()

    def stop(self):
        if self.device:
            self.device.release()

    def start_search(self):
        self.to_search = True
        threading.Thread(target=self.search_objects).start()

    def stop_search(self):
        self.to_search = False

class CameraSettings:
    def __init__(self):
        self.resolution = (640, 480)
        self.quality = 50
        self.framerate = 25
        self.video_format = "mp4"
        self.video_codec = "mp4v"
        self.photo_format = "jpg"
        self.folder = "cam"
        self.no_feed_image_path = "src/no_camera_feed.jpg"
        self.cascade_file = "src/face_cascade.xml"
        self.default_record_time = 30

from flask import Response, send_file
from src.camera import Camera


class CameraControls(Camera):

    # action = request.args.get("action")
    # if action == "snap":
    #     return send_file(cam.take_photo(), mimetype='image/jpeg')
    # elif action == "record":
    #     duration = request.args.get("duration")
    #     if not duration:
    #         duration = 30  # TODO
    #     return cam.record(int(duration))
    # elif action == "snap_and_save":
    #     return cam.take_photo(False)
    # elif action == "start":
    #     cam.start()
    # elif action == "stop":
    #     cam.stop()
    # elif action == "start_search":
    #     cam.start_search()
    # elif action == "stop_search":
    #     cam.stop_search()

    def __init__(self):
        super().__init__()

        self.command_dict = {
            "snap": self.control_snap,
            "record": self.control_record,
            "snap_and_save": self.control_snap_and_save,
            "start_record": self.control_start,
            "stop_record": self.control_stop,
            "start_search": self.control_start_search,
            "stop_search": self.control_stop_search
        }

    def control(self, info):
        action = info["action"]
        return self.command_dict[action]()

    def control_record(self):  # TODO
        file_path = self.record(30)
        return {"info": {
            "file_type": "video",
            "location": file_path
        }
        }

    def control_snap(self):
        return send_file(self.take_photo(), mimetype='image/jpeg')  # TODO

    def control_snap_and_save(self):
        file_path = self.take_photo(False)
        return {"info": {
            "file_type": "image",
            "location": file_path
        }
        }

    def control_start(self):
        self.start()
        return {"info": {
            "activity": "recording",
            "status": True
        }
        }

    def control_stop(self):
        self.stop()
        return {"info": {
            "activity": "recording",
            "status": False
        }
        }

    def control_start_search(self):
        self.start_search()
        return {"info": {
            "activity": "searching",
            "status": True
        }
        }

    def control_stop_search(self):
        self.stop_search()
        return {"info": {
            "activity": "recording",
            "status": False
        }
        }

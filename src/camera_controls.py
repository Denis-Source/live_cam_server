from flask import send_file
from src.camera import Camera
from flask_restful import abort


class CameraControls(Camera):
    def __init__(self):
        super().__init__()

        self.command_dict = {
            "status": self.retrieve_status,
            "snap": self.control_snap,
            "record": self.control_record,
            "snap_and_save": self.control_snap_and_save,
            "start_capture": self.control_start,
            "stop_capture": self.control_stop,
            "start_search": self.control_start_search,
            "stop_search": self.control_stop_search
        }

    def control(self, context):
        action = context["action"]
        try:
            return self.command_dict[action](context)
        except KeyError:
            return {"message": f"Unknown 'action' argument: {action}"}

    def retrieve_status(self, context):
        return {"capturing": self.to_capture,
                "searching": self.to_search
                }

    def control_record(self, context):
        if context["duration"]:
            duration = context["duration"]
        else:
            duration = self.DEFAULT_RECORD_TIME
        file_path = self.record(duration)
        return {"file_type": "video",
                "location": file_path
                }

    def control_snap(self, context):
        return send_file(self.take_photo(), mimetype='image/jpeg')

    def control_snap_and_save(self, context):
        if context["token"] == self.VALID_TOKEN:
            file_path = self.take_photo(False)
            return {"file_type": "image",
                    "location": file_path
                    }
        else:
            return abort(403)

    def control_start(self, context):
        if context["token"] == self.VALID_TOKEN:
            self.start()
            return self.retrieve_status(context)
        else:
            return abort(403)

    def control_stop(self, context):
        if context["token"] == self.VALID_TOKEN:
            self.stop()
            return self.retrieve_status(context)
        else:
            return abort(403)

    def control_start_search(self, context):
        if context["token"] == self.VALID_TOKEN:
            self.start_search()
            return self.retrieve_status(context)
        else:
            return abort(403)

    def control_stop_search(self, context):
        if context["token"] == self.VALID_TOKEN:
            self.stop_search()
            return self.retrieve_status(context)
        else:
            return abort(403)

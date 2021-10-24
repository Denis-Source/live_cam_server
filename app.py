from flask import Flask, Response, render_template, request
from src.camera_controls import CameraControls
from flask_restful import Resource, Api, reqparse
from config import Config

app = Flask(__name__)
api = Api(app)
camera_controls = CameraControls()


@app.route("/video_feed")
def video_feed():
    return Response(camera_controls.gen_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")


class CameraControlApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("action", type=str, help="Action performed by a camera")
        parser.add_argument("duration", type=int, help="Duration of a video in case of recording action")
        arguments = parser.parse_args(strict=True)
        token = request.headers.get("Authorization", default=None)
        if token:
            token = token.split()[-1]
        arguments.update({"token": token})
        return camera_controls.control(arguments)


api.add_resource(CameraControlApi, "/api")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    camera_controls.start()
    app.run(host="0.0.0.0", port=Config.PORT)

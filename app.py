from flask import Flask, Response, render_template, request, send_file
from src.camera import Camera

app = Flask(__name__)
cam = Camera()


@app.route('/video_feed')
def video_feed():
    return Response(cam.gen_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    action = request.args.get("action")
    if action == "snap":
        return send_file(cam.take_photo(), mimetype='image/jpeg')
    elif action == "record":
        duration = request.args.get("duration")
        if not duration:
            duration = 30  # TODO
        return cam.record(int(duration))
    elif action == "snap_and_save":
        return cam.take_photo(False)
    elif action == "start":
        cam.start()
    elif action == "stop":
        cam.stop()
    elif action == "start_search":
        cam.start_search()
    elif action == "stop_search":
        cam.stop_search()
    return render_template("index.html")


if __name__ == '__main__':
    cam.start()
    app.run(host="0.0.0.0", port=5000)

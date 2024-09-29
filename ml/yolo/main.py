import requests, time, os
from scenedetect import detect, ContentDetector
from ultralytics import YOLOv10


def get_non_empty_response(url):
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.json():
                return response.json()
            print("Waiting for non-empty response...")
        except Exception as e: print("error", e)
        time.sleep(2)


def get_data(video_path):
    frame_ranges = []
    scene_list = detect(video_path, ContentDetector())

    for i, scene in enumerate(scene_list):
        frame_ranges.append((scene[0].get_frames(), scene[1].get_frames()))

    def get_top_classes_in_scenes(video_path):
        results = model.predict(source=video_path, save=True, verbose=True)

        a = []
        bbox = []
        for r in results:
            b = []
            for box in r.boxes:
                b.append(r.names[box.cls.item()])
            a.append(b)

        elements = []

        for frame_index, r in enumerate(results):
            objects = []

            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                class_id = int(box.cls)
                class_name = r.names[class_id]
                number_of_classes = 1
                classes = [class_name]

                objects.append({
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "number_of_classes": number_of_classes,
                    "classes": classes
                })

            elements.append({
                "number_of_objects": len(objects),
                "objects": objects
            })

        object_detection = {
            "frames": len(elements),
            "elements": elements
        }

        return object_detection
    return get_top_classes_in_scenes(video_path)


def send_json_back(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("JSON sent successfully!")
        else:
            print("Failed to send JSON:", response.status_code)
    except Exception as e:
        print("Error sending JSON:", e)


def download_video(video_url, save_path='video.mp4'):
    try:
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded video to {save_path}")
            return save_path
        else:
            print("Failed to download video:", response.status_code)
    except Exception as e:
        print("Error downloading video:", e)
        return None


MODEL_NAME = "yolo"
model = YOLOv10.from_pretrained('jameslahm/yolov10x')
POLLING_URL = os.getenv('POLLING_URL', None)
print("model Initialized")


def main():
    polling_url = os.path.join(POLLING_URL, MODEL_NAME)

    while True:
        response_data = get_non_empty_response(polling_url)

        if 'video_url' in response_data:
            video_url = response_data['video_url']
            video_path = download_video(video_url)
            if video_path is None:
                time.sleep(5)
                continue
            processed_data = get_data(video_path)
            return_url = response_data['json_callback_url'] + "/" + MODEL_NAME
            send_json_back(return_url, processed_data)

        time.sleep(5)


if __name__ == "__main__":
    main()
import time

import cv2
import requests
from PIL import Image
from transformers import pipeline


def get_non_empty_response(url):
    while True:
        response = requests.get(url)
        if response.status_code == 200 and response.json():
            return response.json()
        print("Waiting for non-empty response...")
        time.sleep(2)


def get_text_for_each_frame(video_path):
    frames_with_text = {}
    pipe = pipeline(
        "image-to-text",
        model="Salesforce/blip2-opt-2.7b-coco",
        device="cuda:0",
    )
    cap = cv2.VideoCapture(video_path)

    for i in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)

        frames_with_text[i] = pipe(pil_image)[0]["generated_text"]

    cap.release()
    return {"video_frames": frames_with_text}


def send_json_back(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("JSON sent successfully!")
        else:
            print("Failed to send JSON:", response.status_code)
    except Exception as e:
        print("Error sending JSON:", e)


def main():
    polling_url = "http://your-polling-url.com"
    return_url = "http://your-return-url.com"

    while True:
        response_data = get_non_empty_response(polling_url)

        if "video_url" in response_data:
            video_path = response_data["video_url"]
            processed_data = get_text_for_each_frame(video_path)

            send_json_back(return_url, processed_data)

        time.sleep(5)


if __name__ == "__main__":
    main()

import time
import requests
from collections import Counter
import cv2, os
from deepface import DeepFace
from scenedetect import detect, ContentDetector
import statistics


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

    cap = cv2.VideoCapture(video_path)
    frames = {}
    current_frame = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if current_frame % 5 == 0:
            objs = DeepFace.analyze(
                img_path=frame,
                actions=['age', 'emotion', 'gender'],
                enforce_detection=False,
                silent=False
            )
            tmp = []
            for obj in objs:
                tmp.append([obj["age"], obj["dominant_emotion"], obj["dominant_gender"]])
            frames[current_frame] = tmp
        current_frame += 1
    cap.release()

    scene_statistics = []

    for idx, (start_frame, end_frame) in enumerate(frame_ranges):
        relevant_frames = [frame_num for frame_num in frames if start_frame <= frame_num < end_frame]

        ages = []
        emotions = []
        genders = []

        for frame_num in relevant_frames:
            for obj in frames[frame_num]:
                age, emotion, gender = obj
                ages.append(age)
                emotions.append(emotion)
                genders.append(gender)

        if ages and emotions and genders:
            emotion_counter = Counter(emotions)
            most_common_emotion, _ = emotion_counter.most_common(1)[0]

            average_age = statistics.mean(ages)

            gender_counter = Counter(genders)
            most_common_gender, _ = gender_counter.most_common(1)[0]
        else:
            most_common_emotion = None
            average_age = None
            most_common_gender = None

        scene_stats = {
            'scene_index': idx,
            'start_frame': start_frame,
            'end_frame': end_frame,
            'most_common_emotion': most_common_emotion,
            'average_age': average_age,
            'most_common_gender': most_common_gender
        }

        scene_statistics.append(scene_stats)

    emotions = {
        "emotions": {
            "scenes": len(frame_ranges),
            "elements": [],
        }
    }

    for scene in scene_statistics:
        emotions["emotions"]["elements"].append({
            "age": scene["average_age"],
            "emotion": scene["most_common_emotion"],
            "gender": scene["most_common_gender"]
        })

    return emotions


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


POLLING_URL = os.getenv('POLLING_URL', None)
print("model Initialized")
MODEL_NAME = "deepface"


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
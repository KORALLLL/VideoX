from scenedetect import detect, ContentDetector
from transformers import AutoImageProcessor, AutoTokenizer, VisionEncoderDecoderModel
import torch
import numpy as np
import av, os
import time
import requests
from tqdm import tqdm


def get_non_empty_response(url):
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.json(): 
                return response.json()
            print("Waiting for non-empty response...")
        except Exception as e: print("error", e)
        time.sleep(5)


def get_text_for_each_frame(video_path, image_processor, tokenizer, model):
    frame_ranges = []

    scene_list = detect(video_path, ContentDetector())
    for i, scene in enumerate(scene_list):
        frame_ranges.append((scene[0].get_frames(), scene[1].get_frames()))

    captions = []

    container = av.open(video_path)
    stream = container.streams.video[0]

    def extract_frames(container, a, b):
        frames = []
        container.seek(0)
        for i, frame in enumerate(container.decode(video=0)):
            if a <= i < b:
                frames.append(frame.to_ndarray(format="rgb24"))
            elif i >= b:
                break
        return frames

    for idx, (a, b) in enumerate(tqdm(frame_ranges)):

        frames = extract_frames(container, a, b)
        if not frames:
            continue

        clip_len = model.config.encoder.num_frames

        seg_len = len(frames)
        if seg_len < clip_len:
            captions.append('')
            continue

        indices = np.linspace(0, seg_len - 1, num=clip_len, dtype=np.int64)
        selected_frames = [frames[i] for i in indices]

        try:
            pixel_values = image_processor(selected_frames, return_tensors="pt").pixel_values.to(device)
            tokens = model.generate(pixel_values, min_length=10, max_length=20, num_beams=8)
            caption = tokenizer.batch_decode(tokens, skip_special_tokens=True)[0]
            captions.append(caption)
        except Exception as e:
            print(e)
            captions.append('')

    scene_summary = {
        "scene_detection": {
            "count": len(frame_ranges),
            "elements": [{"start": int(start), "end": int(end), "scene": i + 1, "summary": captions[i]} for i, (start, end) in enumerate(frame_ranges)]
        }
    }

    return scene_summary


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


MODEL_NAME = "timesformer-gpt2"
device = "cuda" if torch.cuda.is_available() else "cpu"
POLLING_URL = os.getenv('POLLING_URL', None)


def main():
    polling_url = os.path.join(POLLING_URL, MODEL_NAME)

    image_processor = AutoImageProcessor.from_pretrained("MCG-NJU/videomae-base")
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = VisionEncoderDecoderModel.from_pretrained("Neleac/timesformer-gpt2-video-captioning").to(device)
    print('we are ready')
    while True:
        response_data = get_non_empty_response(polling_url)

        if 'video_url' in response_data:
            video_url = response_data['video_url']
            video_path = download_video(video_url)
            if video_path is None:
                time.sleep(5)
                continue
            processed_data = get_text_for_each_frame(video_path, image_processor, tokenizer, model)
            return_url = response_data['json_callback_url'] + "/" + MODEL_NAME
            send_json_back(return_url, processed_data)

        time.sleep(5)


if __name__ == "__main__":
    main()

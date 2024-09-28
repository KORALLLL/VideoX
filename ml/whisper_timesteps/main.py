import time, json
import requests, os
from moviepy.editor import VideoFileClip


def get_non_empty_response(url):
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.json():
                return response.json()
            print("Waiting for non-empty response...")
        except Exception as e: print("error", e)
        time.sleep(2)


def get_trascribe(video_path):
    audio_file_name = f"output_audio_of_{video_path}.mp3"
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_file_name)

    os.system(f"whisper {audio_file_name} --language Russian --word_timestamps True --output_format json --model large-v3")
    with open(f'{audio_file_name[:-4]}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    elements = []

    for segment in data['segments']:
        for word_info in segment.get('words', []):
            elements.append({
                "start": word_info['start'],
                "end": word_info['end'],
                "word": word_info['word']
            })

    output_data = {
        'transcribation': {
            "elements": elements,
            "count": len(elements)
        }
    }

    os.remove(audio_file_name)
    return output_data


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


MODEL_NAME = "whisper_timestemps"
POLLING_URL = os.getenv('POLLING_URL', None)


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
            processed_data = get_trascribe(video_path)
            return_url = response_data['json_callback_url'] + "/" + MODEL_NAME
            send_json_back(return_url, processed_data)

        time.sleep(5)


if __name__ == "__main__":
    main()
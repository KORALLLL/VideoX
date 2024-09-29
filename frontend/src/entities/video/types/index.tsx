export interface VideoData {
    id: number,
    name: string,
    status: string,
    uploaded_at: string,
    processed_at: string,
    original_video_url: string,
    processed_video_url: string,
    processed: {
        whisper_full: {
            full_transcribation: string
        },
        timesformer_gpt2: {
            scene_detection: {
                count: number,
                elements: Array<Element>
            }
        }
    }
}

interface Element {
    end: number,
    scene: number,
    start: number,
    summary: string
}
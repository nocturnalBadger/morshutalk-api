import io
import tempfile
import os
import ssl
from pathlib import Path
from tempfile import NamedTemporaryFile
from enum import Enum

from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import StreamingResponse
from morshutalk.morshu import Morshu
from pydantic import BaseModel
from pydub import AudioSegment
from moviepy import ImageSequenceClip, AudioArrayClip, AudioFileClip

MAX_SIZE = 1000
FRAME_RATE = 60
SECS_PER_FRAME = (1.0 / FRAME_RATE)

app = FastAPI()

master_video_clip = ImageSequenceClip("./assets", fps=FRAME_RATE)
master_video_frames = [frame for frame in master_video_clip.iter_frames()]


class MorshResponseType(Enum):
    AUDIO = "audio"
    VIDEO = "video"

class MorshingRequest(BaseModel):
    message: str
    response_type: MorshResponseType = MorshResponseType.AUDIO

@app.get("/")
def get_root():
    return "Hello World"

def construct_video(morsher: Morshu, audio: AudioSegment, output_path: str):

    output_frames = []
    output_frame_indices = []
    output_durations = []
    time_offset = 0.0
    millis_per_frame = FRAME_RATE
    while time_offset + SECS_PER_FRAME < audio.duration_seconds:
        frame_idx = morsher.get_frame_idx_from_millis(time_offset * 1000)
        if len(output_frame_indices) == 0:
            output_frame_indices.append(frame_idx)
        if not output_durations:
            output_durations.append(0)
        if frame_idx == output_frame_indices[-1]:
            output_durations[-1] += SECS_PER_FRAME
        else:
            output_frame_indices.append(frame_idx)
            output_durations.append(SECS_PER_FRAME)

        time_offset += SECS_PER_FRAME

    video_length_mismatch = sum(output_durations) - audio.duration_seconds
    output_durations[-1] -= video_length_mismatch

    output_frames = [master_video_frames[i] for i in output_frame_indices]
    output_clip = ImageSequenceClip(output_frames, durations=output_durations)

    with NamedTemporaryFile(suffix=".mp3") as audio_file:
        audio.export(audio_file.name, format="mp3")

        audio_clip = AudioFileClip(audio_file.name, fps=audio.frame_rate)
        output_clip = output_clip.with_audio(audio_clip)

    output_clip.write_videofile(output_path, fps=FRAME_RATE)


@app.post("/morsh")
async def get_morshed(morsh_req: MorshingRequest):

    print(morsh_req)
    if len(morsh_req.message) > MAX_SIZE:
        return HTTPException(status_code=400, detail=f"message cannot be longer than {MAX_SIZE}")

    morsher = Morshu()
    morsh_audio = morsher.load_text(morsh_req.message)
    morsh_audio = morsh_audio.append(AudioSegment.silent(duration=100))

    def stream_audio(audio: AudioSegment):
        with io.BytesIO() as buffer:
            audio.export(buffer, format="mp3")
            yield from buffer

    def stream_video_file(file_path):
        with open(file_path, "rb") as video_file:
            yield from video_file
        os.unlink(file_path)

    if morsh_req.response_type == MorshResponseType.AUDIO:
        return StreamingResponse(stream_audio(morsh_audio), media_type="audio/mp3")
    elif morsh_req.response_type == MorshResponseType.VIDEO:
        video_file = NamedTemporaryFile(suffix=".mp4", delete_on_close=False, delete=False)
        construct_video(morsher, morsh_audio, video_file.name)

        return StreamingResponse(stream_video_file(video_file.name), media_type="video/mp4")
    else:
        return HTTPException(status_code=400, detail=f"response type {morsh_req.response_type} is invalid")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("morshuapi:app", port=8000, host='0.0.0.0', ssl_keyfile=os.environ.get("CERT_KEY_PATH"), ssl_certfile=os.environ.get("CERTFILE_PATH"))

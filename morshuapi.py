from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import StreamingResponse
from morshutalk import morshu
from pydantic import BaseModel
from enum import Enum
import io
import tempfile
import os
import ssl


app = FastAPI()
morsher = morshu.Morshu()

MAX_SIZE = 1000

class MorshResponseType(Enum):
    AUDIO = "audio"
    VIDEO = "video"

class MorshingRequest(BaseModel):
    message: str
    response_type: MorshResponseType = MorshResponseType.AUDIO

@app.get("/")
def get_root():
    return "Hello World"

@app.post("/morsh")
async def get_morshed(morsh_req: MorshingRequest):

    if len(morsh_req.message) > MAX_SIZE:
        return HTTPException(status_code=400, detail=f"message cannot be longer than {MAX_SIZE}")


    def morshify(text: str):
        audio = morsher.load_text(text)
        with io.BytesIO() as buffer:
            audio.export(buffer, format="mp3")
            yield from buffer

    return StreamingResponse(morshify(morsh_req.message), media_type="audio/mp3")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("morshuapi:app", port=8000, host='0.0.0.0', ssl_keyfile=os.environ.get("CERT_KEY_PATH"), ssl_certfile=os.environ.get("CERTFILE_PATH"))

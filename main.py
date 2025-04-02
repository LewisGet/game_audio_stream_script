import sounddevice as sd
import numpy as np

GAIN = 8.0 # rise minimun wavs
MAX_VOLUME = 0.9 # limiting maximum wavs
RATE = 44100
BLOCK_SIZE = 64

sd.default.latency = 'low'

def audio_callback(indata, outdata, frames, time, status):
    if status:
        print(status)

    processed = indata * GAIN
    np.clip(processed, -MAX_VOLUME, MAX_VOLUME, out=processed)

    outdata[:] = processed

input_device_info = sd.default.device[0]
output_device_info = sd.default.device[1]

stream = sd.Stream(
    device=(input_device_info, output_device_info),
    samplerate=RATE,
    blocksize=BLOCK_SIZE,
    channels=2,
    callback=audio_callback,
    dtype='float32'
)

stream.start()

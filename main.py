import sounddevice as sd
import numpy as np

GAIN = 8.0 # rise minimun wavs
MAX_VOLUME = 0.9 # limiting maximum wavs
RATE = 44100
BLOCK_SIZE = 64

sd.default.latency = (0.02, 0.02)

def audio_callback(indata, outdata, frames, time, status):
    processed = indata * GAIN
    np.clip(processed, -MAX_VOLUME, MAX_VOLUME, out=processed)
    outdata[:] = processed


# using `python -m sounddevice` to checkout device index
input_device = sd.default.device[0]
input_info = sd.query_devices(input_device, 'input')
input_channels = input_info['max_input_channels']

output_device = sd.default.device[1]
output_info = sd.query_devices(output_device, 'output')
output_channels = output_info['max_output_channels']

stream = sd.Stream(
    device=(input_device, output_device),
    samplerate=RATE,
    blocksize=BLOCK_SIZE,
    channels=max(input_channels, output_channels),
    callback=audio_callback,
    dtype='float32',
    latency=sd.default.latency,
    prime_output_buffers_using_stream_callback=True
)

stream.start()

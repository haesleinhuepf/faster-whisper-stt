import sounddevice as sd
import numpy as np
import queue
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

audio_queue = queue.Queue()
sample_rate = 16000

def audio_callback(indata, frames, time, status):
    """This function is called by sounddevice during audio recording."""
    audio_queue.put(indata.copy())

def start_recording(b=None):
    """Starts audio recording."""
    audio_queue.queue.clear()  # Clears the queue before recording
    stream.start()

def interrupt_recording(b=None, audio_data=[], my_text=None):
    """Stops audio recording and starts transcription."""
    stream.stop()

    if len(audio_data) > 20:
        audio_data = audio_data[-20:]

    while not audio_queue.empty():
        audio_data.append(audio_queue.get())
    start_recording()
    if audio_data:
        audio_np = np.concatenate(audio_data, axis=0)
        write('output.wav', sample_rate, audio_np.astype(np.int16))  # Writes WAV file
        transcribe_audio('output.wav', my_text)

def transcribe_audio(audio_path, my_text):
    """Transcribes the recorded audio."""
    model = WhisperModel("small", device="cpu")
    segments, _ = model.transcribe(audio_path, language="de", word_timestamps=True)
    transcription = " ".join([segment.text for segment in segments])
    my_text.value = transcription
    
def reset_transcription(b, text_output):
    """Resets the transcription."""
    text_output.value = ""

stream = sd.InputStream(callback=audio_callback, samplerate=sample_rate, channels=1, dtype='int16')

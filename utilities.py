import sounddevice as sd
import numpy as np
import queue
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

class Listener:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.sample_rate = 16000
        self.audio_data = []
        self.stream = sd.InputStream(callback=self.audio_callback, samplerate=self.sample_rate, channels=1, dtype='int16')
        self.model = WhisperModel("small", device="cpu")  # Initialize the model here
    
    def audio_callback(self, indata, frames, time, status):
        """This function is called by sounddevice during audio recording."""
        self.audio_queue.put(indata.copy())
    
    def start_recording(self, b=None):
        """Starts audio recording."""
        self.audio_queue.queue.clear()  # Clears the queue before recording
        self.stream.start()
    
    def interrupt_recording(self, b=None, my_text=None):
        """Stops audio recording and starts transcription."""
        self.stream.stop()
        
        if len(self.audio_data) > 20:
            self.audio_data = self.audio_data[-20:]

        while not self.audio_queue.empty():
            self.audio_data.append(self.audio_queue.get())
        self.start_recording()
        if self.audio_data:
            audio_np = np.concatenate(self.audio_data, axis=0)
            write('output.wav', self.sample_rate, audio_np.astype(np.int16))  # Writes WAV file
            self.transcribe_audio('output.wav', my_text)
    
    def transcribe_audio(self, audio_path, my_text):
        """Transcribes the recorded audio."""
        segments, _ = self.model.transcribe(audio_path, language="de", word_timestamps=True)
        transcription = " ".join([segment.text for segment in segments])
        if my_text is not None:
            my_text.setText(transcription)
    
    def reset_transcription(self, b, text_output):
        """Resets the transcription."""
        text_output.value = ""

    def get_transcribed_text(self, audio_path):
        """Gets the transcribed text from the audio file."""
        segments, _ = self.model.transcribe(audio_path, language="de", word_timestamps=True)
        transcription = " ".join([segment.text for segment in segments])
        return transcription

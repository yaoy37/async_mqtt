import numpy as np
import speech_recognition as sr
from googletrans import Translator
from typing import List, Optional, Tuple

class AudioProcessor:
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.buffer: List[np.ndarray] = []
        self.buffer_size = 0
        self.min_buffer_size = self.sample_rate  # 1 second of audio
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        self.context_buffer = ""  # Stores previous translations for context

    def add_audio_data(self, data: bytes):
        """Add new audio data to buffer"""
        # Convert bytes to numpy array
        audio_array = np.frombuffer(data, dtype=np.int16)
        self.buffer.append(audio_array)
        self.buffer_size += len(audio_array)

    def get_audio_chunk(self) -> Optional[bytes]:
        """Get a chunk of audio data when buffer is full enough"""
        if self.buffer_size >= self.min_buffer_size:
            # Concatenate all buffered audio
            audio_data = np.concatenate(self.buffer)
            # Clear buffer
            self.buffer = []
            self.buffer_size = 0
            return audio_data.tobytes()
        return None

    def process_audio_segment(self, audio_data: bytes) -> Tuple[str, str]:
        """Process audio segment and return (original_text, translated_text)"""
        # Convert bytes to AudioData
        audio = sr.AudioData(audio_data, self.sample_rate, 2)
        
        # Recognize speech with context
        try:
            text = self.recognizer.recognize_google(audio, language="zh-CN")
            # Apply text correction
            corrected_text = self._correct_text(text)
            # Translate with context
            translation = self.translator.translate(
                corrected_text,
                src="zh-CN",
                dest="en",
                context=self.context_buffer
            )
            # Update context buffer
            self.context_buffer = corrected_text[:100]  # Keep last 100 chars
            return corrected_text, translation.text
        except sr.UnknownValueError:
            return "", ""
        except sr.RequestError:
            return "", ""

    def _correct_text(self, text: str) -> str:
        """Apply text correction rules"""
        # Basic text normalization
        text = text.replace(" ", "")  # Remove spaces in Chinese text
        # Add more correction rules as needed
        return text

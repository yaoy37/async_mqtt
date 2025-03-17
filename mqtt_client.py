import paho.mqtt.client as mqtt
from typing import Optional, Dict, Any
import json
from config import Config
from audio_processor import AudioProcessor

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.latest_data: Optional[Dict] = None
        self.audio_processor = AudioProcessor()
        self.translation_buffer: List[str] = []
        
        # Load configuration
        config = Config()
        self.topic = config.MQTT_TOPIC
        self.broker = config.MQTT_BROKER
        self.port = config.MQTT_PORT
        
        # Setup callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        # Subscribe to topic
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        try:
            # Handle audio data
            if msg.topic.endswith('/audio'):
                self.audio_processor.add_audio_data(msg.payload)
                if audio_chunk := self.audio_processor.get_audio_chunk():
                    translation = self.process_audio(audio_chunk)
                    if translation != "Translation failed":
                        self.translation_buffer.append(translation)
                        print(f"New translation: {translation}")
            else:
                # Handle regular JSON data
                self.latest_data = json.loads(msg.payload.decode())
                print(f"Received new data: {self.latest_data}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def process_audio(self, audio_data: bytes) -> str:
        """Process audio data and return translation"""
        original_text, translated_text = self.audio_processor.process_audio_segment(audio_data)
        if not translated_text:
            return "Translation failed"
        return translated_text

    def start(self):
        print("Starting MQTT client...")
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

    def get_latest_data(self):
        return self.latest_data or {"error": "No data received yet"}

class Config:
    # MQTT Configuration
    MQTT_BROKER = "broker.hivemq.com"
    MQTT_PORT = 1883
    MQTT_TOPIC = "sensors/data"
    AUDIO_TOPIC = "sensors/audio"  # Topic for audio data
    
    # Audio Processing Configuration
    SAMPLE_RATE = 441000  # 16kHz
    CHUNK_SIZE = 512 * 16  # 512 samples * 16 bits
    
    # Web Service Configuration
    WEB_HOST = "0.0.0.0"
    WEB_PORT = 8000
    
    # Translation Configuration
    SOURCE_LANGUAGE = "en"  # Source language code
    TARGET_LANGUAGE = "zh"  # Target language code

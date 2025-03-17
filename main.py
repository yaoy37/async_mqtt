from fastapi import FastAPI
from mqtt_client import MQTTClient
import uvicorn
from config import Config

app = FastAPI()
mqtt_client = MQTTClient()
config = Config()

@app.on_event("startup")
async def startup_event():
    mqtt_client.start()

@app.on_event("shutdown")
async def shutdown_event():
    mqtt_client.stop()

@app.get("/")
async def root():
    return {"status": "running"}

@app.get("/data")
async def get_data():
    return mqtt_client.get_latest_data()

@app.get("/translations")
async def get_translations():
    return {
        "translations": mqtt_client.translation_buffer,
        "count": len(mqtt_client.translation_buffer)
    }

if __name__ == "__main__":
    uvicorn.run(app, host=config.WEB_HOST, port=config.WEB_PORT)

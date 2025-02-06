from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import logging
import speech_recognition as sr
import asyncio
import signal
import sys

app = FastAPI(title="SebasTian Assistant")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='sebastian.log'
)
logger = logging.getLogger(__name__)

# Global flag to control voice detection loop
is_listening = False

async def listen_for_wake_word(wake_word="Roy"):
    global is_listening
    recognizer = sr.Recognizer()
    
    logger.info("Starting voice detection...")
    
    while is_listening:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                logger.info("Listening for wake word...")
                
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    text = recognizer.recognize_google(audio).lower()
                    logger.info(f"Heard: {text}")
                    print(f"Heard: {text}")
                    
                    if wake_word in text:
                        logger.info("Wake word detected!")
                        # Here you can trigger your assistant's main functionality
                        await trigger_assistant()
                        
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    logger.error(f"Could not request results: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error in voice detection: {str(e)}")
            await asyncio.sleep(1)
        
        await asyncio.sleep(0.1)

async def trigger_assistant():
    """Function to handle assistant activation"""
    logger.info("Assistant activated!")
    # Add your assistant's main functionality here
    return {"status": "activated", "message": "How can I help you?"}

@app.get("/")
async def root():
    return {"message": "SebasTian Assistant is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/start-voice-detection")
async def start_voice_detection(background_tasks: BackgroundTasks):
    global is_listening
    if not is_listening:
        is_listening = True
        background_tasks.add_task(listen_for_wake_word)
        return {"status": "started", "message": "Voice detection started"}
    return {"status": "already_running", "message": "Voice detection is already running"}

@app.post("/stop-voice-detection")
async def stop_voice_detection():
    global is_listening
    is_listening = False
    return {"status": "stopped", "message": "Voice detection stopped"}

@app.on_event("startup")
async def startup_event():
    logger.info("SebasTian Assistant starting up...")
    # Automatically start voice detection on startup
    global is_listening
    is_listening = True
    asyncio.create_task(listen_for_wake_word())

@app.on_event("shutdown")
async def shutdown_event():
    global is_listening
    is_listening = False
    logger.info("SebasTian Assistant shutting down...")

# Handle graceful shutdown
def signal_handler(sig, frame):
    global is_listening
    is_listening = False
    logger.info("Shutting down voice detection...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


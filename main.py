import threading
import uvicorn
import os
from dotenv import load_dotenv
from grpc_main import serveOCR
from uvircorn_main import app

load_dotenv()
PORT = int(os.getenv("APP_PORT", 7003))
HOST = os.getenv("APP_HOST", "0.0.0.0")

async def server_fastapi():
    config =  uvicorn.Config(
        app,
        host=HOST,
        port=PORT,
        reload=False,
    )
    uvicorn_server = uvicorn.Server(config)
    await uvicorn_server.serve()
    print(f"API server is running on {HOST}:{PORT}\n")

# Run both as concurrently , but one of them didn't start other also failed to start
def main():
    grpc_thread = threading.Thread(
        target=serveOCR,
        daemon=True # hang on even shutdown
    )
    grpc_thread.start()
    server_fastapi()
  
if __name__ == "__main__":
    main()
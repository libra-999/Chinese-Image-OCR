import threading
import uvicorn
import os
from dotenv import load_dotenv
from grpc_main import serveOCR
from uvircorn_main import app
import asyncio


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

def server_grpc():
    try:
        serveOCR()
    except Exception as e:
        print(f"Uvicorn cannot running , msg {e}")
        
async def main():
    grpc_thread = threading.Thread(
        target=server_grpc,
        daemon=True # hang on even shutdown
    )
    grpc_thread.start()
    try:
        await server_fastapi()
    except Exception as e:
        print(f"Uvicorn cannot running , msg {e}")
  
if __name__ == "__main__":
    asyncio.run(main())
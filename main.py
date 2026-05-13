import asyncio
import uvicorn
import os
from dotenv import load_dotenv
from grpc_main import serveOCR

load_dotenv()
PORT = os.getenv("APP_PORT", 7003 )
HOST = os.getenv("APP_HOST", "0.0.0.0")

async def server_fastapi():
    config =  uvicorn.Config(
        "uvicorn_main:app",
        host=HOST,
        port=PORT,
        reload=False,
    )
    uvicorn_server = uvicorn.Server(config)
    await uvicorn_server.serve()
    print(f"API server is running on {HOST}:{PORT}\n")

# Run both as concurrently , but one of them didn't start other also failed to start
async def main():
    await asyncio.gather(
        server_fastapi(),
        serveOCR()
    )
  
if __name__ == "__main__":
    asyncio.run(main())
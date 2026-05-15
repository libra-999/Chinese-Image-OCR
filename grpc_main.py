from concurrent import futures
import grpc
import v1.ocr_image_pb2_grpc as data_pb2_grpc
from rpc_provider.ocr_service import ImageOCRService
import os
from dotenv import load_dotenv

load_dotenv()
WORKER = int(os.getenv("GRPC_WORKER",8))
PORT = int(os.getenv("GRPC_PORT", 50051))

def serveOCR():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=WORKER))
    data_pb2_grpc.add_ImageOCRServiceServicer_to_server(ImageOCRService(), server)
    server.add_insecure_port(f'[::]:{PORT}')
    server.start()

    print(f"GRPC server is running on {PORT}")
    server.wait_for_termination()
    
if __name__ == "__main__":
    serveOCR()
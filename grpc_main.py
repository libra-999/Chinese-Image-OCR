from concurrent import futures
import grpc
import v1.ocr_image_pb2 as data_pb2
import v1.ocr_image_pb2_grpc as data_pb2_grpc
from rpc_provider.ocr_service import ImageOCRService

def serveOCR():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    data_pb2_grpc.add_ImageOCRServiceServicer_to_server(ImageOCRService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    server.wait_for_termination()
    
if __name__ == "__main__":
    serveOCR()
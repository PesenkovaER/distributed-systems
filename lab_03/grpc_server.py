import grpc
from concurrent import futures
import message_service_pb2
import message_service_pb2_grpc
import random
import string

emails = []

class MessageService(message_service_pb2_grpc.MessageServiceServicer):

    def Subscribe(self, request, context):
        print("Получен email:", request.email)

        emails.append(request.email)

        return message_service_pb2.Response(
            result=f"{request.email} добавлен в рассылку"
        )

    def GeneratePassword(self, request, context):
        print("Генерация пароля длиной:", request.length)

        password = ''.join(random.choices(
            string.ascii_letters + string.digits,
            k=request.length
        ))

        return message_service_pb2.Response(result=password)

    def CountVowels(self, request, context):
        print("Подсчёт гласных в:", request.text)

        vowels = "aeiouAEIOUаеёиоуыэюяАЕЁИОУЫЭЮЯ"
        count = sum(1 for c in request.text if c in vowels)

        return message_service_pb2.Response(result=str(count))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_service_pb2_grpc.add_MessageServiceServicer_to_server(
        MessageService(), server
    )

    server.add_insecure_port('[::]:50051')

    print("gRPC сервер запущен на порту 50051")

    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
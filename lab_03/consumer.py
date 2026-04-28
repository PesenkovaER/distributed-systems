import sys
import os

sys.path.append(os.path.abspath("../grpc_sync"))

import pika
import grpc
import message_service_pb2
import message_service_pb2_grpc

def process(message):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = message_service_pb2_grpc.MessageServiceStub(channel)

        if message.startswith("subscribe:"):
            email = message.split(":", 1)[1]
            return stub.Subscribe(
                message_service_pb2.EmailRequest(email=email)
            ).result

        elif message.startswith("pass:"):
            length = int(message.split(":", 1)[1])
            return stub.GeneratePassword(
                message_service_pb2.PasswordRequest(length=length)
            ).result

        elif message.startswith("vowels:"):
            text = message.split(":", 1)[1]
            return stub.CountVowels(
                message_service_pb2.TextRequest(text=text)
            ).result

        return "Ошибка команды"


credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

print("Ожидание сообщений...")

def callback(ch, method, properties, body):
    msg = body.decode()
    print("Получено:", msg)

    result = process(msg)
    print("[✓] Результат:", result)

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
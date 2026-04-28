import pika

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

print("Формат:")
print("subscribe:email")
print("pass:число")
print("vowels:текст")

message = input("Введите сообщение: ")

channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message
)

print("Отправлено:", message)

connection.close()
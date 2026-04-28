import grpc
import message_service_pb2
import message_service_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = message_service_pb2_grpc.MessageServiceStub(channel)

        print("1 - Subscribe")
        print("2 - Password")
        print("3 - Vowels")

        choice = input("Выбор: ")

        if choice == "1":
            email = input("Email: ")
            response = stub.Subscribe(
                message_service_pb2.EmailRequest(email=email)
            )

        elif choice == "2":
            length = int(input("Длина: "))
            response = stub.GeneratePassword(
                message_service_pb2.PasswordRequest(length=length)
            )

        elif choice == "3":
            text = input("Текст: ")
            response = stub.CountVowels(
                message_service_pb2.TextRequest(text=text)
            )

        else:
            print("Ошибка")
            return

        print("Ответ:", response.result)

if __name__ == "__main__":
    run()
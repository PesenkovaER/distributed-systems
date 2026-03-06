import grpc
import survey_pb2
import survey_pb2_grpc


def generate_answers():
    questions = [
        ("Как вам курс?", "Очень нравится"),
        ("Сложная ли лабораторная?", "Немного сложная"),
        ("Будете использовать gRPC?", "Да")
    ]

    for q, a in questions:
        yield survey_pb2.Answer(
            question=q,
            answer=a
        )


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = survey_pb2_grpc.SurveyServiceStub(channel)

        print("Отправка ответов на сервер...")
        response = stub.SubmitAnswers(generate_answers())

        print("\nОтвет сервера:")
        print(f"Всего ответов: {response.total_answers}")
        print(response.message)


if __name__ == '__main__':
    run()

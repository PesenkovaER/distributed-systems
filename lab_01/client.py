import grpc
import survey_pb2
import survey_pb2_grpc


questions = {
    1: "Нравится ли вам программирование?",
    2: "Какой язык программирования вы изучаете?",
    3: "Использовали ли вы раньше gRPC?"
}


def generate_answers():
    for q_id, question in questions.items():
        print(f"{q_id}. {question}")
        answer = input("Ваш ответ: ")

        yield survey_pb2.Answer(
            question=question,
            answer=answer
        )


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = survey_pb2_grpc.SurveyServiceStub(channel)

    print("Опрос начался. Пожалуйста, ответьте на вопросы:\n")

    response = stub.SubmitAnswers(generate_answers())

    print("\nОтвет сервера:", response.message)


if __name__ == "__main__":
    run()

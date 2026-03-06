import grpc
from concurrent import futures
import survey_pb2
import survey_pb2_grpc


class SurveyService(survey_pb2_grpc.SurveyServiceServicer):

    def SubmitAnswers(self, request_iterator, context):
        answers = []

        for answer in request_iterator:
            print(f"Получен ответ на вопрос {answer.question}: {answer.answer}")
            answers.append(answer)

        result_text = f"Сервер получил {len(answers)} ответов на опрос."

        return survey_pb2.SurveyResult(message=result_text)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    survey_pb2_grpc.add_SurveyServiceServicer_to_server(SurveyService(), server)

    server.add_insecure_port('[::]:50051')
    server.start()

    print("Сервер запущен на порту 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()

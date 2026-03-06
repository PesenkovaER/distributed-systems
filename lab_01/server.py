import grpc
from concurrent import futures
import survey_pb2
import survey_pb2_grpc


class SurveyServiceServicer(survey_pb2_grpc.SurveyServiceServicer):

    def SubmitAnswers(self, request_iterator, context):
        print("Получение ответов от клиента...")

        count = 0

        for answer in request_iterator:
            print(f"Вопрос: {answer.question}")
            print(f"Ответ: {answer.answer}")
            print("-----")
            count += 1

        return survey_pb2.SurveyResult(
            total_answers=count,
            message=f"Получено {count} ответов. Спасибо за участие!"
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    survey_pb2_grpc.add_SurveyServiceServicer_to_server(
        SurveyServiceServicer(), server
    )

    server.add_insecure_port('[::]:50051')
    server.start()

    print("Сервер запущен на порту 50051...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

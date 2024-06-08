from rest_framework.response import Response
from rest_framework.views import APIView
from project.tasks import celery_test


class TestCeleryView(APIView):
    def get(self, request):
        celery_test.delay()
        return Response()

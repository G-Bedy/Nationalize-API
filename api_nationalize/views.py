import requests
from django.core.cache import cache
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Person
from .schemas import (delete_person_parameters, get_person_parameters,
                      person_schema)
from .serializers import PersonSerializer

EXTERNAL_API_URL = "https://api.nationalize.io/?name="


def index(request):
    """Отображает главную страницу с пользовательским интерфейсом."""
    return render(request, 'index.html')

class NameService:
    """Класс для работы с БД и внешним API"""
    CACHE_TIMEOUT = 60 * 60

    @staticmethod
    def get_data_from_db(name):
        """
        Получить данные из БД и кэшировать их.

        :param name: Имя пользователя.
        :return: Словарь с данными или None, если запись не найдена.
        """
        try:
            entry = Person.objects.get(name=name)
            data = {
                "name": entry.name,
                "count": entry.count,
                "country": entry.country,
            }
            cache.set(name, data, timeout=NameService.CACHE_TIMEOUT)
            return data
        except Person.DoesNotExist:
            return None

    @staticmethod
    def get_data_from_external_api(name):
        """
        Запросить данные у внешнего API.

        :param name: Имя пользователя.
        :return: JSON-данные от внешнего API или None в случае ошибки.
        """
        response = requests.get(f"{EXTERNAL_API_URL}{name}")
        if response.status_code == 200:
            return response.json()
        return None


class NameAPIView(APIView):
    """
    API для управления данными об именах.

    Операции:
    - GET: Получить данные об имени.
    - POST: Создать новую запись об имени.
    - PUT: Полностью обновить существующую запись.
    - PATCH: Частично обновить существующую запись.
    - DELETE: Удалить запись об имени.
    """

    @swagger_auto_schema(manual_parameters=get_person_parameters)
    def get(self, request):
        """
        Получить данные об имени.

        Пример запроса:
        ```
        GET /api/v1/names/?name=Vadim
        ```

        Возвращает:
        - 200 OK: Данные успешно получены.
        - 400 Bad Request: Отсутствует обязательный параметр `name`.
        - 500 Internal Server Error: Ошибка при запросе к внешнему API.
        """
        name = request.GET.get('name')
        if not name:
            return Response({"error": "Поле 'name' обязательно для заполнения"}, status=status.HTTP_400_BAD_REQUEST)

        cached_data = cache.get(name)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        try:
            entry = Person.objects.get(name=name)
            data = {
                "name": entry.name,
                "count": entry.count,
                "country": entry.country
            }
            cache.set(name, data, timeout=60 * 60)  # Кэшируем на 1 час
            return Response(data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            pass

        response = requests.get(EXTERNAL_API_URL + name)
        if response.status_code != 200:
            return Response({"error": "External API request failed"}, status=response.status_code)

        data = response.json()
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PersonSerializer, responses={201: "Created", 400: "Bad Request"})
    # @swagger_auto_schema(request_body=person_schema, responses={201: "Created", 400: "Bad Request"})
    def post(self, request):
        """
        Создать новую запись об имени.

        Пример запроса:
        ```
        POST /api/v1/names/
        {
            "name": "Vadim",
            "count": 1,
            "country": [{"country_id": "RU", "probability": 0.8}]
        }
        ```

        Возвращает:
        - 201 Created: Запись успешно создана.
        - 400 Bad Request: Неверные входные данные.
        - 500 Internal Server Error: Ошибка при сохранении данных.
        """
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response({"error": "Не удалось сохранить данные."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=person_schema, responses={200: "Updated", 400: "Bad Request", 404: "Not Found"})
    def put(self, request):
        """
        Полностью обновить существующую запись о пользователе.

        Пример запроса:
        ```
        PUT /api/v1/names/
        {
            "name": "Vadim",
            "count": 2,
            "country": [{"country_id": "RU", "probability": 0.9}]
        }
        ```

        Возвращает:
        - 200 OK: Запись успешно обновлена.
        - 400 Bad Request: Неверные входные данные.
        - 404 Not Found: Запись не найдена.
        """
        try:
            name = request.data.get('name')
            if not name:
                return Response({"error": "Значение 'name' обязательно"}, status=status.HTTP_400_BAD_REQUEST)

            instance = Person.objects.get(name=name)
        except Person.DoesNotExist:
            return Response({"error": "Запись не найдена"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonSerializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            cache.delete(name)
            updated_data = {
                "name": serializer.instance.name,
                "count": serializer.instance.count,
                "country": serializer.instance.country,
            }
            cache.set(name, updated_data, timeout=NameService.CACHE_TIMEOUT)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=person_schema, responses={200: "Partially Updated", 400: "Bad Request", 404: "Not Found"})
    def patch(self, request):
        """
        Частично обновить существующую запись о пользователе.

        Пример запроса:
        ```
        PATCH /api/v1/names/
        {
            "name": "Vadim",
            "count": 3
        }
        ```

        Возвращает:
        - 200 OK: Запись успешно обновлена.
        - 400 Bad Request: Неверные входные данные.
        - 404 Not Found: Запись не найдена.
        """
        name = request.data.get("name")
        if not name:
            return Response({"error": "Поле 'name' обязательно для заполнения"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Person.objects.get(name=name)
        except Person.DoesNotExist:
            return Response({"error": "Запись не найдена"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete(name)
            updated_data = {
                "name": serializer.instance.name,
                "count": serializer.instance.count,
                "country": serializer.instance.country,
            }
            cache.set(name, updated_data, timeout=NameService.CACHE_TIMEOUT)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=delete_person_parameters)
    def delete(self, request):
        """
        Удалить запись о пользователе.

        Пример запроса:
        ```
        DELETE /api/v1/names/?name=Vadim
        ```

        Возвращает:
        - 204 No Content: Запись успешно удалена.
        - 400 Bad Request: Отсутствует обязательный параметр `name`.
        - 404 Not Found: Запись не найдена.
        """
        name = request.GET.get('name')

        if not name:
            return Response({"error": "Поле 'name' обязательно для заполнения"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cache.delete(name)
            instance = Person.objects.get(name=name)  # Находим запись по имени
            instance.delete()
            return Response({"message": "Запись удалена"}, status=status.HTTP_204_NO_CONTENT)
        except Person.DoesNotExist:
            return Response({"error": "Запись не найдена"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from spells.models import MaterialComponent


class MaterialComponentSerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели MaterialComponent"""

    class Meta:
        model = MaterialComponent
        fields = ["name", "description", "cost", "is_consumable", "is_focus"]

    def validate_name(self, value):
        """Валидация имени"""
        if len(value) > 49:
            raise serializers.ValidationError("Максимум 49 символов")
        return value

    def validate_cost(self, value):
        """Валидация стоимости"""
        if value and value < 0:
            raise serializers.ValidationError("Стоимость не может быть отрицательной")
        return value


"""API по пути /api/spells/material_component/"""


class MaterialConponentListView(APIView):
    def get(self, request: Request):
        """Получение всех компонент"""
        # Получаем все объекты (READ)
        components = MaterialComponent.objects.all()
        # Настраиваем сериализатор данных
        serializer = MaterialComponentSerializer(components, many=True)
        # Отправляем данные с ответом 200
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        """Создание нового материального компонента"""
        # Десериализация данных, настройка сериализатора
        serializer = MaterialComponentSerializer(data=request.data)
        # Проверка валидности данных, при неправильных данных отправит ошибку
        serializer.is_valid(raise_exception=True)
        # Создание нового компонента в базе
        serializer.save()
        # Отправление ответ с кодом 201 (created) и созданный объект
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

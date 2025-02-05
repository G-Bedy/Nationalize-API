from rest_framework import serializers

from .models import Person


class CountrySerializer(serializers.Serializer):
    country_id = serializers.CharField()
    probability = serializers.FloatField()

class PersonSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True)  # Вложенный сериализатор

    class Meta:
        model = Person
        fields = ['name', 'count', 'country']

    def update(self, instance, validated_data):
        """Обновление только переданных полей, а не перезапись всего списка"""
        if "country" in validated_data:
            new_countries = validated_data.pop("country")  # Берем новые данные
            existing_countries = instance.country  # Достаем текущий список из БД

            # Создаем словарь для быстрого поиска существующих записей
            country_map = {c["country_id"]: c for c in existing_countries}

            # Обновляем существующие записи, не трогая другие
            for new_country in new_countries:
                country_id = new_country["country_id"]
                if country_id in country_map:
                    country_map[country_id].update(new_country)
                else:
                    country_map[country_id] = new_country  # Добавляем новую страну, если ее не было

            instance.country = list(country_map.values())  # Сохраняем обновленный список

        return super().update(instance, validated_data)
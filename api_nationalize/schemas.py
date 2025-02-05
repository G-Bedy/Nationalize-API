from drf_yasg import openapi

person_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["name", "count", "country"],
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Имя"),
        "count": openapi.Schema(type=openapi.TYPE_INTEGER, description="Количество упоминаний"),
        "country": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description="Список стран с вероятностями",
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "country_id": openapi.Schema(type=openapi.TYPE_STRING, description="Код страны"),
                    "probability": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT,
                                                  description="Вероятность")
                }
            )
        )
    }
)

get_person_parameters = [
    openapi.Parameter(
        'name',
        openapi.IN_QUERY,
        description="Имя, по которому выполняется поиск",
        type=openapi.TYPE_STRING,
        required=True
    )
]


delete_person_parameters = [
    openapi.Parameter(
        'name',
        openapi.IN_QUERY,
        description="Имя, которое нужно удалить",
        type=openapi.TYPE_STRING,
        required=True
    )
]
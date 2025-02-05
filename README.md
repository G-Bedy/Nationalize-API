# Nationalize API

## Описание проекта

Проект представляет собой RESTful API для работы с данными об именах и их вероятной национальной принадлежности. Он позволяет:
- Получать данные об имени из базы данных или внешнего API.
- Создавать, обновлять и удалять записи через API.
- Кэшировать результаты запросов для повышения производительности.

API документировано с помощью Swagger/OpenAPI, что позволяет легко тестировать endpoint'ы через интерфейс браузера.

---

## **Содержание**
1. [Запуск проекта](#запуск-проекта)
2. [API Endpoints](#api-endpoints)
3. [Используемые технологии](#используемые-технологии)
4. [Зависимости](#зависимости)
5. [Примеры запросов](#примеры-запросов)

---

## **Запуск проекта**

### 1. Клонируйте репозиторий:
```bash
git clone [https://github.com/yourusername/nationalize-api.git](https://github.com/G-Bedy/Nationalize-API.git)
cd nationalize-api
```

### 2. Создайте виртуальное окружение и активируйте его:

#### Для Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### Для macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установите зависимости:
```bash
pip install -r requirements.txt
```

### 4. Примените миграции:
```bash
python manage.py migrate
```

### 5. Запустите сервер:
```bash
python manage.py runserver
```

API будет доступно по адресу: [http://127.0.0.1:8000/api/v1/names/](http://127.0.0.1:8000/api/v1/names/).

### 6. Документация API:
- Swagger UI: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- ReDoc UI: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

---

## **API Endpoints**

### 1. GET `/api/v1/names/?name=<имя>`

#### Описание:
Возвращает данные о вероятной национальной принадлежности для указанного имени. Если данные отсутствуют в БД, они запрашиваются у внешнего API.

#### Параметры:
| Название | Тип   | Обязательный | Описание               |
|----------|-------|-------------|------------------------|
| `name`   | string| Да          | Имя пользователя       |

#### Ответы:
- **200 OK**: Данные успешно получены.
  ```json
  {
      "name": "Артем",
      "count": 749,
      "country": [
        {
          "country_id": "RU",
          "probability": 0.48747151850296
        },
        {
          "country_id": "KZ",
          "probability": 0.174757725611249
        },
        {
          "country_id": "UA",
          "probability": 0.0313840470957702
        },
        {
          "country_id": "LT",
          "probability": 0.00754926139580072
        },
        {
          "country_id": "MD",
          "probability": 0.00754926139580072
        }
      ]
  }
  ```
- **400 Bad Request**: Отсутствует обязательный параметр `name`.
- **404 Not Found**: Данные не найдены.
- **500 Internal Server Error**: Ошибка при запросе к внешнему API.

---

### 2. POST `/api/v1/names/`

#### Описание:
Создает новую запись в БД с указанными данными.

#### Тело запроса:
```json
{
  "count": 749,
  "name": "Артем",
  "country": [
    {
      "country_id": "RU",
      "probability": 0.48747151850296
    },
    {
      "country_id": "KZ",
      "probability": 0.174757725611249
    },
    {
      "country_id": "UA",
      "probability": 0.0313840470957702
    },
    {
      "country_id": "LT",
      "probability": 0.00754926139580072
    },
    {
      "country_id": "MD",
      "probability": 0.00754926139580072
    }
  ]
}
```

#### Ответы:
- **201 Created**: Запись успешно создана.
- **400 Bad Request**: Неверные входные данные.
- **500 Internal Server Error**: Ошибка сервера при сохранении данных.

---

### 3. PUT `/api/v1/names/`

#### Описание:
Полностью обновляет существующую запись в БД по указанному имени.

#### Тело запроса:
```json
{
  "count": 749,
  "name": "Артем",
  "country": [
    {
      "country_id": "RU",
      "probability": 0.111111
    },
    {
      "country_id": "KZ",
      "probability": 0.222222
    },
    {
      "country_id": "UA",
      "probability": 0.333333
    },
    {
      "country_id": "LT",
      "probability": 0.444444
    },
    {
      "country_id": "MD",
      "probability": 0.5555555
    }
  ]
}
```

#### Ответы:
- **200 OK**: Запись успешно обновлена.
- **400 Bad Request**: Неверные входные данные.
- **404 Not Found**: Запись не найдена.

---

### 4. PATCH `/api/v1/names/`

#### Описание:
Частично обновляет существующую запись в БД по указанному имени.

#### Тело запроса:
```json
{
  "count": 749,
  "name": "Артем",
  "country": [
    {
      "country_id": "RU",
      "probability": 0.123456789
    }
  ]
}
```

#### Ответы:
- **200 OK**: Запись успешно обновлена.
- **400 Bad Request**: Неверные входные данные.
- **404 Not Found**: Запись не найдена.

---

### 5. DELETE `/api/v1/names/?name=<имя>`

#### Описание:
Удаляет запись из БД по указанному имени.

#### Параметры:
| Название | Тип   | Обязательный | Описание               |
|----------|-------|-------------|------------------------|
| `name`   | string| Да          | Имя пользователя       |

#### Ответы:
- **204 No Content**: Запись успешно удалена.
- **400 Bad Request**: Отсутствует обязательный параметр `name`.
- **404 Not Found**: Запись не найдена.

---

## **Используемые технологии**

- **Django**: Framework для создания веб-приложений.
- **Django REST Framework (DRF)**: Библиотека для создания RESTful API.
- **drf-yasg**: Инструмент для генерации документации API в формате Swagger/OpenAPI.
- **Requests**: Библиотека для выполнения HTTP-запросов к внешнему API.
- **Django Cache Framework**: Используется для кэширования результатов запросов.

---

## **Зависимости**

Проект зависит от следующих библиотек. Они должны быть установлены перед запуском:

- Django
- djangorestframework
- drf-yasg
- requests

Установите зависимости с помощью:
```bash
pip install -r requirements.txt
```

---

## **Примеры запросов**

### 1. Получение данных:
```bash
GET http://127.0.0.1:8000/api/v1/names/?name=Vadim
```

Ответ:
```json
{
  "count": 1585,
  "name": "Vadim",
  "country": [
    {
      "country_id": "MD",
      "probability": 0.245998500417504
    },
    {
      "country_id": "UA",
      "probability": 0.139403519561733
    },
    {
      "country_id": "RU",
      "probability": 0.0725337935694305
    },
    {
      "country_id": "BY",
      "probability": 0.0316087458637016
    },
    {
      "country_id": "RO",
      "probability": 0.0296615863616178
    }
  ]
}
```

---

### 2. Создание записи:
```bash
POST http://127.0.0.1:8000/api/v1/names/
Content-Type: application/json

{
  "count": 1585,
  "name": "Vadim",
  "country": [
    {
      "country_id": "MD",
      "probability": 0.245998500417504
    },
    {
      "country_id": "UA",
      "probability": 0.139403519561733
    },
    {
      "country_id": "RU",
      "probability": 0.0725337935694305
    },
    {
      "country_id": "BY",
      "probability": 0.0316087458637016
    },
    {
      "country_id": "RO",
      "probability": 0.0296615863616178
    }
  ]
}
```

Ответ:
```json
{
  "count": 1585,
  "name": "Vadim",
  "country": [
    {
      "country_id": "MD",
      "probability": 0.245998500417504
    },
    {
      "country_id": "UA",
      "probability": 0.139403519561733
    },
    {
      "country_id": "RU",
      "probability": 0.0725337935694305
    },
    {
      "country_id": "BY",
      "probability": 0.0316087458637016
    },
    {
      "country_id": "RO",
      "probability": 0.0296615863616178
    }
  ]
}
```

---

### 3. Полное обновление записи:
```bash
PUT http://127.0.0.1:8000/api/v1/names/
Content-Type: application/json

{
  "count": 1585,
  "name": "Vadim",
  "country": [
    {
      "country_id": "MD",
      "probability": 0.111111111
    },
    {
      "country_id": "UA",
      "probability": 0.22222222
    },
    {
      "country_id": "RU",
      "probability": 0.3333333
    },
    {
      "country_id": "BY",
      "probability": 0.444444
    },
    {
      "country_id": "RO",
      "probability": 0.55555555
    }
  ]
}
```

Ответ:
```json
{
  "count": 1585,
  "name": "Vadim",
  "country": [
    {
      "country_id": "MD",
      "probability": 0.111111111
    },
    {
      "country_id": "UA",
      "probability": 0.22222222
    },
    {
      "country_id": "RU",
      "probability": 0.3333333
    },
    {
      "country_id": "BY",
      "probability": 0.444444
    },
    {
      "country_id": "RO",
      "probability": 0.55555555
    }
  ]
}
```

---

### 4. Частичное обновление записи:
```bash
PATCH http://127.0.0.1:8000/api/v1/names/
Content-Type: application/json

{
  "count": 1585,
  "name": "Vadim",
  "country": [
    {
      "country_id": "MD",
      "probability": 0.77777777
    }
  ]
}
```

Ответ:
```json
{
  "count": 1585,
  "name": "Vadim",
  "country": [
    {
      "country_id": "MD",
      "probability": 0.77777777
    }
  ]
}
```

---

### 5. Удаление записи:
```bash
DELETE http://127.0.0.1:8000/api/v1/names/?name=Vadim
```

Ответ:
```json
{
    "message": "Запись удалена"
}
```

---

## **Автор**

Этот проект создан Годоборшевым Эльбердом для демонстрации работы с RESTful API, кэшированием и взаимодействием с внешними сервисами.
```
```

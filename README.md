# Описание проекта

API для работы с географическими точками и привязанными к ним сообщениями. Поддерживает JWT-аутентификацию, создание новых точек, поиск точек в радиусе и создание/просмотр сообщений.

Также в проекте реализовано отображение всех точек на карте, а также сообщений к ним (сообщения отображаются при нажатии на точку)

-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------

# Запуск:
Код  запущен на сервисе render.com.
Для проверки работы нужно перейти на сайт https://map-esdf.onrender.com/ и дождаться загрузки страницы (индикатором загрузки служат или возникновение формы с просьбой ввести токен для авторизации, который предварительно нужно получить через api запрос, или отображение карты)
После загрузки страницы можно тестировать работу.
(Просьба учитывать, что из-за выбора бесплатного плана на данном сервисе, если сайт не открывался никем в течении определённого времени - он "засыпает", поэтому при первом открытии проекта страница может загружаться несколько минут)

-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------

# Аутентификация

API использует JWT-аутентификацию. Для доступа к endpoint'ам необходимо получить токен.

-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------

# Запросы:

-----------------------------------------------------------------------------------------------
## Пользователь:

1. Регистрация:

**Формат запроса:**
curl -X POST https://map-esdf.onrender.com/api/register/ -H "Content-Type: application/json" -d "{\"username\":\"<Имя пользователя>\",\"email\":\"<Email пользователя>\",\"password\":\"<Пароль>\",\"password2\":\"<Пароль>\"}"

**Пример:**
curl -X POST https://map-esdf.onrender.com/api/register/ -H "Content-Type: application/json" -d "{\"username\":\"User1\",\"email\":\"User1@test.ru\",\"password\":\"testtesttest\",\"password2\":\"testtesttest\"}"

**Ответ:**
{"message":"Пользователь успешно создан"}


2. Получение токена (вход в учётную запись):

**Формат запроса:**
curl -X POST https://map-esdf.onrender.com/api/token/ -H "Content-Type: application/json" -d "{\"username\":\"<Имя пользователя>\",\"password\":\"<Пароль>\"}"

**Пример:**
curl -X POST https://map-esdf.onrender.com/api/token/ -H "Content-Type: application/json" -d "{\"username\":\"User1\",\"password\":\"testtesttest\"}"

**Ответ:**
{
  "refresh": "<refresh токен>",
  "access": "<access токен>"
}


Полученный access токен добавляется в заголовки запросов:
Authorization: Bearer <ваш_access_токен>

**Пример:**
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY4NjY2MTc4LCJpYXQiOjE3Njg2NjI1NzgsImp0aSI6IjA0ZWFiOTQ1ZjUxOTRjYWU4YWU5ZmExYzRmNGE0ZmNmIiwidXNlcl9pZCI6IjIifQ.oPauzC786N35l9gN4sgY6gKvLsQ8x1pfZwLYaQaNYP4

-----------------------------------------------------------------------------------------------

## Точки (Points)
1. Получить список всех точек

**Формат запроса:**
curl -X GET https://map-esdf.onrender.com/api/points/ -H "Authorization: Bearer <ваш_access_токен>"

**Пример:**
curl -X GET https://map-esdf.onrender.com/api/points/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY4NjY2MTc4LCJpYXQiOjE3Njg2NjI1NzgsImp0aSI6IjA0ZWFiOTQ1ZjUxOTRjYWU4YWU5ZmExYzRmNGE0ZmNmIiwidXNlcl9pZCI6IjIifQ.oPauzC786N35l9gN4sgY6gKvLsQ8x1pfZwLYaQaNYP4"

**Ответ:**
{"count":1,"next":null,"previous":null,"results":[{"id":1,"user":{"id":2,"username":"User1"},"name":"Point 1","latitude":55.75,"longitude":37.62,"created_at":"2026-01-17T15:30:31.004392Z","messages":[{"user":{"id":2,"username":"User1"},"text":"Test","created_at":"2026-01-17T15:35:09.124466Z"}]}]}

2. Создать новую точку

**Формат запроса:**
curl -X POST https://map-esdf.onrender.com/api/points/ -H "Authorization: Bearer <ваш_access_токен>" -H "Content-Type: application/json" -d "{\"latitude\":\"<Число>\",\"longitude\":\"<Число>\",\"name\":\"<Имя>\"}"

**Пример:**
curl -X POST https://map-esdf.onrender.com/api/points/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY4NjY2MTc4LCJpYXQiOjE3Njg2NjI1NzgsImp0aSI6IjA0ZWFiOTQ1ZjUxOTRjYWU4YWU5ZmExYzRmNGE0ZmNmIiwidXNlcl9pZCI6IjIifQ.oPauzC786N35l9gN4sgY6gKvLsQ8x1pfZwLYaQaNYP4" -H "Content-Type: application/json" -d "{\"latitude\":\"55.75\",\"longitude\":\"37.62\",\"name\":\"Point 1\"}"

**Ответ:**
{"id":1,"user":{"id":2,"username":"User1"},"name":"Point 1","latitude":55.75,"longitude":37.62,"created_at":"2026-01-17T15:30:31.004392Z","messages":[]}

3. Поиск точек в радиусе

**Формат запроса:**
curl -X GET "https://map-esdf.onrender.com/api/points/search/?latitude=<Число>&longitude=<Число>&radius=<Число>" -H "Authorization: Bearer <ваш_access_токен>"

**Параметры:**

    latitude (обязательный): широта (-90 до 90)

    longitude (обязательный): долгота (-180 до 180)

    radius (обязательный): радиус поиска в километрах (> 0)


**Пример:**
curl -X GET "https://map-esdf.onrender.com/api/points/search/?latitude=55.7&longitude=37.6&radius=1000" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY4NjY2MTc4LCJpYXQiOjE3Njg2NjI1NzgsImp0aSI6IjA0ZWFiOTQ1ZjUxOTRjYWU4YWU5ZmExYzRmNGE0ZmNmIiwidXNlcl9pZCI6IjIifQ.oPauzC786N35l9gN4sgY6gKvLsQ8x1pfZwLYaQaNYP4"

**Ответ:**
[{"id":1,"user":{"id":2,"username":"User1"},"name":"Point 1","latitude":55.75,"longitude":37.62,"created_at":"2026-01-17T15:30:31.004392Z","messages":[{"user":{"id":2,"username":"User1"},"text":"Test","created_at":"2026-01-17T15:35:09.124466Z"}],"distance_km":5.7}]

-----------------------------------------------------------------------------------------------

## Сообщения (Messages)
1. Получить сообщения по радиусу

**Формат запроса:**
curl -X GET "https://map-esdf.onrender.com/api/points/messages/?latitude=<Число>&longitude=<Число>&radius=<Число>" -H "Authorization: Bearer <ваш_access_токен>"

**Пример:**
curl -X GET "https://map-esdf.onrender.com/api/points/messages/?latitude=55.7&longitude=37.6&radius=1000" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY4NjY2MTc4LCJpYXQiOjE3Njg2NjI1NzgsImp0aSI6IjA0ZWFiOTQ1ZjUxOTRjYWU4YWU5ZmExYzRmNGE0ZmNmIiwidXNlcl9pZCI6IjIifQ.oPauzC786N35l9gN4sgY6gKvLsQ8x1pfZwLYaQaNYP4"

**Ответ:**
[{"id":1,"point":1,"user":{"id":2,"username":"User1"},"text":"Test","created_at":"2026-01-17T15:35:09.124466Z"}]



2. Получить сообщения конкретной точки

**Формат запроса:**
curl -X GET "https://map-esdf.onrender.com/api/points/messages/?point_id=<ID точки>" -H "Authorization: Bearer <ваш_access_токен>"

**Пример:**
curl -X GET "https://map-esdf.onrender.com/api/points/messages/?point_id=1" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY4NjY2MTc4LCJpYXQiOjE3Njg2NjI1NzgsImp0aSI6IjA0ZWFiOTQ1ZjUxOTRjYWU4YWU5ZmExYzRmNGE0ZmNmIiwidXNlcl9pZCI6IjIifQ.oPauzC786N35l9gN4sgY6gKvLsQ8x1pfZwLYaQaNYP4"

**Ответ:**
[{"id":1,"point":1,"user":{"id":2,"username":"User1"},"text":"Test","created_at":"2026-01-17T15:35:09.124466Z"}]



3. Создать новое сообщение

**Формат запроса:**
curl -X POST https://map-esdf.onrender.com/api/points/messages/ -H "Authorization: Bearer <ваш_access_токен>" -H "Content-Type: application/json" -d "{\"point_id\":<ID Точки>, \"text\": \"<Сообщение>\"}"

**Пример:**
curl -X POST https://map-esdf.onrender.com/api/points/messages/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY4NjY2MTc4LCJpYXQiOjE3Njg2NjI1NzgsImp0aSI6IjA0ZWFiOTQ1ZjUxOTRjYWU4YWU5ZmExYzRmNGE0ZmNmIiwidXNlcl9pZCI6IjIifQ.oPauzC786N35l9gN4sgY6gKvLsQ8x1pfZwLYaQaNYP4" -H "Content-Type: application/json" -d "{\"point_id\": 1, \"text\": \"Test\"}"

**Ответ:**
{"id":1,"point":1,"user":{"id":2,"username":"User1"},"text":"Test","created_at":"2026-01-17T15:35:09.124466Z"}


-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------

# Техническое описание:

**models.py**
В проекте используются:
Модель User - для хранения информации о пользователях
Модель Point - для хранения информации о точках
Модель Message - для хранения информации о сообщениях


**serializers.py**
В проекте используются:
UserSerializer - для данных о пользователях
MessageSerializer - для данных о сообщениях
MessagePointSerializer - для сокращённых данных о сообщениях (используется при просмотре точек и в отличие от MessageSerializer не включает в себя данные о самой точке)
PointSerializer - для данных о точках
PointSearchSerializer - для данных о точках (используется при поиске точек и проверяет значения latitude, longitude, radius)
UserRegistrationSerializer - для данных о пользователях (при регистрации нового пользователя)


**utils.py**
Функция haversine_distance - Рассчитывает расстояние между двумя точками на Земле с использованием формулы гаверсинусов. Возвращает расстояние в километрах.

**views.py:**
MapView - для отображения карты
PointApi - работа с точками и сообщениями
UserRegistrationView - регистрация пользователей

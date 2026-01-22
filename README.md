# Проект API-2042
Тестовое задание на стажировку Red Collar python-backend от Никиты Рушковского.
## Ручной деплой на персональный компьютер
* Клонируем репозиторий в текущую рабочую директорию.
```commandline
git clone git@github.com:Seamly71/API-2042.git
```
* Заполняем переменные окружения.
В репозитории есть шаблонный файл с необходимыми переменными окружения: template.env.
Значения переменных в нем необходимо записать, а затем переименовать в .env.
```commandline
mv template.env .env
```
* При отсутствии оных необходимо установить Docker.
```commandline
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
 
```
И Docker compose.
```commandline
sudo apt install docker-compose-plugin
```
* Запускаем проект.
```commandline
(amd64) sudo docker compose -f docker-compose.yml up
(arm64) sudo docker compose -f docker-compose.arm64.yml up
```
* Применяем миграции.
```commandline
docker compose run backend sh python manage.py migrate
```
* Проект доступен в сети устройства на 1111м порту.
```
localhost:1111
```
## Примеры запросов к API
```
POST /api/auth/register/: {
  "username": "us3rn@me",
  "password": "s3cr_tPwdd"
}

201: {
  "username": "us3rn@me"
}
```
```
POST /api/auth/login/: {
  "username": "us3rn@me",
  "password": "s3cr_tPwdd"
}

200: {
    "auth_token": "26545c4d7e7cc88130d8f2a94ac373e2684b52ca"
}
```
```
POST /api/points/: {
    "longitude": 37.620393,
    "latitude": 55.753960
}
Authorization: Bearer 26545c4d7e7cc88130d8f2a94ac373e2684b52ca

201: {
    "id": 1,
    "longitude": 37.620393,
    "latitude": 55.75396
}
```
## Структура проекта
* API задокументирован по стандарту OpenAPI 3.0.2.
Документация доступна в docs/openapi.
* Проект покрыт тестами.
Postman-коллекция доступна в backend/tests/API-2042.postman_collection.json.
Перед каждым исполнением тестов необходимо исполнить следующую команду.
```commandline
docker compose -f docker-compose.yml run backend sh tests/setup.sh
```
* Юнит тесты DRF TestCase.
```commandline
docker compose -f docker-compose.yml run backend python manage.py test -v 3
```

## Автор
Никита Seamly71 Рушковский

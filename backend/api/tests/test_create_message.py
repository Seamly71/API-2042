from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from django.contrib.gis.geos import Point as PointObject
from json import loads

from geomessages.models import Point


User = get_user_model()


class TestCreateMessage(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = '/api/points/messages/'
        cls.user = User.objects.create_user(
            username= 'us3rn@me',
            password= 's3cr_tPwdd'
        )
        cls.Moscow = Point.objects.create(
            point = PointObject(37.620393, 55.753960)
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.anon = APIClient()

    def testCorrectCreation(self):
        text = "Привет из Москвы!"
        data = {
            "point_id": self.Moscow.id,
            "text": text
        }

        response = self.client.post(self.url, data)

        self.assertEquals(
            response.status_code,
            201,
            'Статус-код ответа должен быть 201'
        )

        response_object = loads(response.text)

        self.assertIn(
            'point',
            response_object,
            'Ответ должен содержать ключ point_id'
        )
        self.assertIn(
            'text',
            response_object,
            'Ответ должен содержать ключ text'
        )
        self.assertEquals(
            response_object['point']['id'],
            self.Moscow.id,
            'Id точки должен быть равен вводимому'
        )
        self.assertEquals(
            response_object['text'],
            text,
            'Текст точки должен быть равен вводимому'
        )

    def testNoCreateWithoutText(self):
        data = {
            "point_id": self.Moscow.id
        }
        expected_data = {
            "text": [
                "Обязательное поле."
            ]
        }

        response = self.client.post(self.url, data)

        self.assertEquals(
            response.status_code,
            400,
            'Если в запросе на /api/points/messages/ нет текста, '
            'должен вернуться 400'
        )
        self.assertEquals(
            loads(response.text),
            expected_data,
            'Ответ в отчете поля текста должен содержать строку о необходимости поля'
        )

    def testNoCreateWithoutPointId(self):
        text = "Привет из Москвы!"
        data = {
            "text": text
        }
        expected_data = {
            "point_id": [
                "Обязательное поле."
            ]
        }

        response = self.client.post(self.url, data)

        self.assertEquals(
            response.status_code,
            400,
            'Если в запросе на /api/points/messages/ нет id точки, '
            'должен вернуться 400'
        )
        self.assertEquals(
            loads(response.text),
            expected_data,
            'Ответ в отчете поля текста id точки содержать '
            'строку о необходимости поля'
        )

    def testNoCreateWithNonExistentPoint(self):
        text = "Привет из Москвы!"
        data = {
            "point_id": 9999999,
            "text": text
        }
        expected_data = {
            "point_id": [
                "Недопустимый первичный ключ \"9999999\" - объект не существует."
            ]
        }

        response = self.client.post(self.url, data)

        self.assertEquals(
            response.status_code,
            400,
            'Если в запросе на /api/points/messages/ несуществующая '
            'id точки, должен вернуться 400'
        )
        self.assertEquals(
            loads(response.text),
            expected_data,
            'Ответ в отчете поля текста id точки содержать строку о '
            'плохом первичном ключе'
        )

    def testNoCreateWithoutAuth(self):
        text = "Привет из Москвы!"
        data = {
            "point_id": self.Moscow.id,
            "text": text
        }
        expected_data = {
            "detail": "Учетные данные не были предоставлены."
        }

        response = self.anon.post(self.url, data)

        self.assertEquals(
            response.status_code,
            401,
            'Если в запросе на добавление точки нет токена, '
            'то нужно вернуть 401'
        )
        self.assertEquals(
            loads(response.text),
            expected_data,
            'Отчет должен говорить об отсутствии токена'
        )

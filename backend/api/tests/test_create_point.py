from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from json import loads


User = get_user_model()


class TestCreatePoint(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = '/api/points/'

    def setUp(self):
        self.user = User.objects.create_user(
            username= 'us3rn@me',
            password= 's3cr_tPwdd'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.anon = APIClient()

    def testCorrectCreation(self):
        longitude = 37.620393
        latitude = 55.753960
        data = {
            'longitude': longitude,
            'latitude': latitude
        }

        response = self.client.post(self.url, data)

        self.assertEquals(
            response.status_code,
            201,
            'Статус-код ответа должен быть 201'
        )

        parsed_response = loads(response.text)

        self.assertIn(
            'longitude',
            parsed_response,
            'Ответ должен содержать ключ longitude'
        )
        self.assertIn(
            'latitude',
            parsed_response,
            'Ответ должен содержать ключ longitude'
        )
        self.assertEquals(
            parsed_response['longitude'],
            longitude,
            'Широта должна быть равна вводимой'
        )
        self.assertEquals(
            parsed_response['latitude'],
            latitude,
            'Долгота должна быть равна вводимой'
        )

    def testNoCreateWithoutLatitude(self):
        longitude = 37.620393
        data = {
            'longitude': longitude,
        }
        expected_data = {
            "latitude": [
                "Обязательное поле."
        ]
}

        response = self.client.post(self.url, data)

        self.assertEquals(
            response.status_code,
            400,
            'Если в запросе на /api/points/ нет широты, '
            'должен вернуться 400'
        )
        self.assertEquals(
            loads(response.text),
            expected_data,
            'Ответ в отчете поля широты должен '
            'содержать строку о необходимости поля'
        )

    def testNoCreateWithoutLongitude(self):
        latitude = 55.753960
        data = {
            'latitude': latitude,
        }
        expected_data = {
            "longitude": [
                "Обязательное поле."
        ]
        }

        response = self.client.post(self.url, data)

        self.assertEquals(
            response.status_code,
            400,
            'Если в запросе на /api/points/ нет долготы, '
            'должен вернуться 400'
        )
        self.assertEquals(
            loads(response.text),
            expected_data,
            'Ответ в отчете поля долготы должен содержать '
            'строку о необходимости поля'
        )

    def testNoCreateWithoutAuth(self):
        longitude = 37.620393
        latitude = 55.753960
        data = {
            'longitude': longitude,
            'latitude': latitude
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

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from django.contrib.gis.geos import Point as PointObject
from json import loads

from geomessages.models import Point, Message


User = get_user_model()


class TestGetMessages(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = '/api/points/search/'
        cls.user = User.objects.create_user(
            username= 'us3rn@me',
            password= 's3cr_tPwdd'
        )
        cls.Moscow = Point.objects.create(
            point = PointObject(37.620393, 55.753960)
        )
        cls.Ryazan = Point.objects.create(
            point=PointObject(39.6916, 54.6269)
        )
        cls.Peter = Point.objects.create(
            point=PointObject(30.3141, 59.9386)
        )
        cls.Moscow_message = Message.objects.create(
            point=cls.Moscow,
            author=cls.user,
            text='Привет из Москвы!'
        )
        cls.Ryazan_message = Message.objects.create(
            point=cls.Ryazan,
            author=cls.user,
            text='Привет из Москвы!'
        )
        cls.Peter_message = Message.objects.create(
            point=cls.Peter,
            author=cls.user,
            text='Привет из Москвы!'
        )
        cls.Vladimir_longitude = 40.41787,
        cls.Vladimir_latitude = 56.1446,
        cls.Vladimir_radius = 250.67

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.anon = APIClient()

    def testCorrectQuery(self):
        query_params = {
            'longitude': self.Vladimir_longitude,
            'latitude': self.Vladimir_latitude,
            'radius': self.Vladimir_radius
        }

        response = self.client.get(self.url, query_params=query_params)

        self.assertEquals(
            response.status_code,
            200,
            'Статус-код ответа должен быть 200'
        )

        response_object = loads(response.text)

        self.assertIn(
            'results',
            response_object,
            'Ответ должен содержать ключ results'
        )
        self.assertEquals(
            len(response_object['results']),
            2,
            'В выборку должно попасть 2 сообщения'
        )

    def testNoQueryWithoutLatitude(self):
        query_params = {
            'longitude': self.Vladimir_longitude,
            'radius': self.Vladimir_radius
        }
        expected_data = {
            "latitude": "Обязательный параметр."
        }

        response = self.client.get(self.url, query_params=query_params)
        response_object = loads(response.text)

        self.assertEquals(
            response.status_code,
            400,
            'Если в запросе на /api/points/search/ нет параметра широты, '
            'должен вернуться 40'
        )
        self.assertEquals(
            response_object,
            expected_data,
            'Ответ в отчете параметра широты должен содержать '
            'строку о необходимости параметра'
        )

    def testNoQueryWithoutLongitude(self):
        query_params = {
            'latitude': self.Vladimir_latitude,
            'radius': self.Vladimir_radius
        }
        expected_data = {
            "longitude": "Обязательный параметр."
        }

        response = self.client.get(self.url, query_params=query_params)
        response_object = loads(response.text)

        self.assertEquals(
            response.status_code,
            400,
            'Если в запросе на /api/points/search/ нет параметра '
            'долготы, должен вернуться 400'
        )
        self.assertEquals(
            response_object,
            expected_data,
            'Ответ в отчете параметра долготы должен содержать '
            'строку о необходимости параметра'
        )

    def testNoQueryWithoutRadius(self):
        query_params = {
            'longitude': self.Vladimir_longitude,
            'latitude': self.Vladimir_latitude
        }
        expected_data = {
            "radius": "Обязательный параметр."
        }

        response = self.client.get(self.url, query_params=query_params)
        response_object = loads(response.text)

        self.assertEquals(
            response.status_code,
            400,
            'Если в запросе на /api/points/search/ нет параметра '
            'радиуса, должен вернуться 400'
        )
        self.assertEquals(
            response_object,
            expected_data,
            'Ответ в отчете параметра радиуса должен содержать '
            'строку о необходимости параметра'
        )

    def testNoQueryWithoutAuth(self):
        query_params = {
            'longitude': self.Vladimir_longitude,
            'latitude': self.Vladimir_latitude,
            'radius': self.Vladimir_radius
        }
        expected_data = {
            "detail": "Учетные данные не были предоставлены."
        }

        response = self.anon.get(self.url, query_params=query_params)

        self.assertEquals(
            response.status_code,
            401,
            'Если в запросе на получение сообщений нет токена, '
            'то нужно вернуть 401'
        )
        self.assertEquals(
            loads(response.text),
            expected_data,
            'Отчет должен говорить об отсутствии токена'
        )

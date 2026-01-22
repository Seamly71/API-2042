from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from json import loads


User = get_user_model()


class TestLogin(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = '/api/auth/login/'
        cls.credentials = {
            'username': 'us3rn@me',
            'password': 's3cr_tPwdd'
        }

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(**self.credentials)

    def testCorrectLogin(self):
        data = {
            'username': 'us3rn@me',
            'password': 's3cr_tPwdd'
        }
        expected_key = 'auth_token'

        response = self.client.post(self.url, data, format='multipart')

        self.assertEquals(
            response.status_code,
            200,
            'Корректный запроc на получение токена должен возвращать 200'
        )
        self.assertIn(
            expected_key,
            loads(response.text).keys(),
            'Ответ должен содержать ключ "token"'
        )

    def testLoginNonExistentUser(self):
        data = {
            'username': 'idonot',
            'password': 'exist'
        }
        expected_data = {
            'non_field_errors': [
                'Невозможно войти с предоставленными учетными данными.'
            ]
        }

        response = self.client.post(self.url, data)

        self.assertEquals(
            response.status_code,
            400,
            'Если в запросе на /api/auth/login/ указаны данные не '
            'существующего юзера, должен вернуться 400'
        )
        self.assertEquals(
            loads(response.text),
            expected_data,
            'Отчет должен указывать на причину отказа'
        )

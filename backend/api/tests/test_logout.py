from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class TestLogout(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = '/api/auth/logout/'
        cls.credentials = {
            'username': 'us3rn@me',
            'password': 's3cr_tPwdd'
        }

    def setUp(self):
        self.user = User.objects.create_user(self.credentials)
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.anon = APIClient()

    def testCorrectLogout(self):
        response = self.client.post(self.url)
        self.assertEquals(
            response.status_code,
            204,
            'При успешном логауте должен быть возвращен 204'
        )

    def testNonLoggedInLogout(self):
        response = self.anon.post(self.url)
        self.assertEquals(
            response.status_code,
            401,
            'Если в запросе на логаут неверный токен, '
            'то нужно вернуть 401'
        )
